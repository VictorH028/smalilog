"""Instalación y control del agente Renef embebido en una APK."""
from __future__ import annotations

import base64
import filecmp
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path

from smalilog.manifest._manifest import (
    INTERNET,
    ManifestError,
    _add_permission,
    _patch_cleartext,
    parse_manifest,
)

ACTION = "com.smalilog.agent.ACTION"
RECEIVER = "com.smalilog.agent.AgentReceiver"
PACKAGE = "com.smalilog.agent"
MAX_SCRIPT_BYTES = 256 * 1024

PAYLOAD_DIR = Path(__file__).resolve().parent / "payload"
DEFAULT_AGENT_SO = PAYLOAD_DIR / "lib" / "arm64-v8a" / "libagent.so"


class AgentError(Exception):
    """Error de instalación o control del agente."""


@dataclass
class InstallReport:
    """Cambios realizados por :func:`install_payload`."""

    app_dir: Path
    manifest: Path
    smali_dir: Path
    lib_dir: Path
    changed: bool = False
    installed: list[str] = field(default_factory=list)
    updated: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    added_permissions: list[str] = field(default_factory=list)
    cleartext_changed: bool = False
    warnings: list[str] = field(default_factory=list)

    def summary(self) -> str:
        parts = [f"instalados={len(self.installed)}"]
        if self.updated:
            parts.append(f"actualizados={len(self.updated)}")
        if self.skipped:
            parts.append(f"sin cambios={len(self.skipped)}")
        if self.added_permissions:
            parts.append("permisos=" + ",".join(self.added_permissions))
        if self.cleartext_changed:
            parts.append("cleartext=true")
        return " · ".join(parts)


def _is_binary_manifest(raw: bytes) -> bool:
    head = raw[:64]
    return (
        head.startswith(b"\x03\x00\x08\x00")
        or head.startswith(b"\xff\xfe")
        or b"\x00" in head
    )


def read_manifest_text(path: str | Path) -> str:
    """Lee un manifiesto en texto y rechaza AXML binario."""
    manifest_path = Path(path)
    if not manifest_path.is_file():
        raise AgentError(f"No existe el manifiesto: {manifest_path}")
    raw = manifest_path.read_bytes()
    if _is_binary_manifest(raw):
        raise AgentError(
            "AndroidManifest.xml está en binario (AXML). Descompila la APK "
            "primero con: apkeditor d -i app.apk -o ./apk")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise AgentError("AndroidManifest.xml no está en UTF-8") from exc


def detect_manifest(app_dir: str | Path) -> Path:
    """Localiza el manifiesto dentro de un APK descompilado."""
    root = Path(app_dir)
    for candidate in (root / "AndroidManifest.xml",
                      root / "root" / "AndroidManifest.xml"):
        if candidate.is_file():
            return candidate
    raise AgentError(
        f"No se encontró AndroidManifest.xml en {root}. "
        "¿Descompilaste la APK con apkeditor d?")


def detect_smali_root(app_dir: str | Path) -> Path:
    """Devuelve el directorio donde se añaden las clases Smali."""
    root = Path(app_dir)
    classes = root / "smali" / "classes"
    if classes.is_dir():
        return classes
    if (root / "smali" / "com").is_dir():
        return root / "smali"
    return classes


def detect_lib_root(app_dir: str | Path) -> Path:
    """Devuelve el directorio de librerías nativas del APK descompilado."""
    root = Path(app_dir)
    for candidate in (root / "root" / "lib", root / "lib"):
        if candidate.is_dir():
            return candidate
    if (root / "root").is_dir():
        return root / "root" / "lib"
    return root / "lib"


def detect_package(app_dir: str | Path) -> str:
    """Lee el package del manifiesto descompilado."""
    manifest = detect_manifest(app_dir)
    try:
        package = parse_manifest(manifest).package
    except ManifestError as exc:
        raise AgentError(str(exc)) from exc
    if not package or package == "(sin package)":
        raise AgentError(f"No se pudo leer el package en {manifest}")
    return package


def _receiver_xml(indent: str) -> str:
    pad = indent + "    "
    inner = indent + "        "
    action = indent + "            "
    return (
        f"{pad}<receiver android:name=\"{RECEIVER}\" "
        "android:exported=\"true\">\n"
        f"{inner}<intent-filter>\n"
        f"{action}<action android:name=\"{ACTION}\" />\n"
        f"{inner}</intent-filter>\n"
        f"{pad}</receiver>\n"
    )


def patch_agent_manifest(
    text: str,
    *,
    permissions: list[str] | None = None,
    internet: bool = True,
    cleartext: bool = True,
) -> tuple[str, list[str], bool, list[str]]:
    """Inserta el receptor del agente y los permisos necesarios."""
    if not re.search(r"<application\b", text):
        raise AgentError(
            "El manifiesto no contiene <application>; no se puede instalar "
            "el receptor del agente")

    warnings: list[str] = []
    added: list[str] = []
    to_add = list(permissions or [])
    if internet and INTERNET not in to_add:
        to_add.insert(0, INTERNET)

    for permission in to_add:
        text, changed = _add_permission(text, permission)
        if changed:
            added.append(permission)

    cleartext_changed = False
    if cleartext:
        if re.search(r"android:networkSecurityConfig\s*=", text):
            warnings.append(
                "El manifiesto usa android:networkSecurityConfig; "
                "puede ignorar usesCleartextTraffic.")
        try:
            text, cleartext_changed = _patch_cleartext(text)
        except ManifestError as exc:
            raise AgentError(str(exc)) from exc

    if RECEIVER not in text:
        close = text.rfind("</application>")
        if close < 0:
            application = re.search(r"<application\b[^>]*?/>", text, re.S)
            if not application:
                raise AgentError(
                    "El manifiesto no tiene </application>; no se puede "
                    "insertar el receptor del agente")
            line_start = text.rfind("\n", 0, application.start()) + 1
            indent_match = re.match(r"[ \t]*", text[line_start:application.start()])
            indent = indent_match.group(0) if indent_match else ""
            opening = application.group(0)[:-2].rstrip()
            text = (
                text[:application.start()]
                + opening + ">\n"
                + indent + "</application>"
                + text[application.end():]
            )
            close = text.rfind("</application>")
        line_start = text.rfind("\n", 0, close) + 1
        indent_match = re.match(r"[ \t]*", text[line_start:close])
        indent = indent_match.group(0) if indent_match else ""
        receiver = _receiver_xml(indent)
        if text[line_start:close].strip():
            text = text[:close] + "\n" + receiver + text[close:]
        else:
            text = text[:line_start] + receiver + text[line_start:]

    return text, added, cleartext_changed, warnings


def _backup(path: Path, root: Path, backup_dir: Path) -> None:
    try:
        relative = path.relative_to(root)
    except ValueError:
        relative = Path(path.name)
    backup = backup_dir / relative
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup)


def _same_bytes(left: Path, right: Path) -> bool:
    return left.is_file() and filecmp.cmp(left, right, shallow=False)


def _copy_file(
    source: Path,
    destination: Path,
    report: InstallReport,
    *,
    force: bool,
    backup: bool,
    backup_dir: Path | None,
    root: Path,
    dry_run: bool,
    label: str,
) -> None:
    if destination.exists():
        if _same_bytes(source, destination):
            report.skipped.append(label)
            return
        if not force:
            raise AgentError(
                f"Ya existe {destination} con otro contenido; usa --force "
                "para reemplazarlo")
        if backup and backup_dir is not None and not dry_run:
            _backup(destination, root, backup_dir)
        if not dry_run:
            shutil.copy2(source, destination)
        report.updated.append(label)
        return
    if not dry_run:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    report.installed.append(label)


def install_payload(
    app_dir: str | Path,
    *,
    agent_so: str | Path | None = None,
    payload_dir: str | Path | None = None,
    force: bool = False,
    backup: bool = True,
    dry_run: bool = False,
    internet: bool = True,
    cleartext: bool = True,
    permissions: list[str] | None = None,
) -> InstallReport:
    """Instala el agente Renef en un APK ya descompilado.

    Copia ``libagent.so``, añade las clases Smali del puente y parchea el
    manifiesto con el receptor, INTERNET y tráfico HTTP en claro.
    """
    root = Path(app_dir)
    if not root.is_dir():
        raise AgentError(f"No existe el directorio: {root}")
    if not (root / "smali").is_dir():
        raise AgentError(
            f"{root} no parece una APK descompilada (falta smali/). "
            "Descompílala con: apkeditor d -i app.apk -o ./apk")

    payload = Path(payload_dir) if payload_dir else PAYLOAD_DIR
    smali_source = payload / "smali" / PACKAGE.replace(".", "/")
    if agent_so:
        lib_source = Path(agent_so)
    elif payload_dir:
        lib_source = payload / "lib" / "arm64-v8a" / "libagent.so"
    else:
        lib_source = DEFAULT_AGENT_SO

    if not smali_source.is_dir():
        raise AgentError(f"No se encontraron las clases Smali en {smali_source}")
    if not lib_source.is_file():
        raise AgentError(
            f"No se encontró libagent.so en {lib_source}. "
            "Compílala con `make native` o copia el agente de Renef.")

    manifest = detect_manifest(root)
    smali_root = detect_smali_root(root)
    lib_dir = detect_lib_root(root) / "arm64-v8a"
    report = InstallReport(
        app_dir=root,
        manifest=manifest,
        smali_dir=smali_root,
        lib_dir=lib_dir,
    )
    backup_dir = None
    if backup and not dry_run:
        backup_name = root.name or "apk"
        backup_dir = root.parent / f".{backup_name}.smalilog-backup"

    text = read_manifest_text(manifest)
    patched, added, cleartext_changed, warnings = patch_agent_manifest(
        text, permissions=permissions, internet=internet, cleartext=cleartext)
    manifest_changed = bool(added) or cleartext_changed or (
        RECEIVER not in text)
    report.added_permissions = added
    report.cleartext_changed = cleartext_changed
    report.warnings.extend(warnings)

    for source in sorted(smali_source.glob("*.smali")):
        destination = smali_root / PACKAGE.replace(".", "/") / source.name
        _copy_file(
            source, destination, report,
            force=force, backup=backup, backup_dir=backup_dir,
            root=root, dry_run=dry_run,
            label=str(destination.relative_to(root)),
        )

    _copy_file(
        lib_source, lib_dir / "libagent.so", report,
        force=force, backup=backup, backup_dir=backup_dir,
        root=root, dry_run=dry_run,
        label=str((lib_dir / "libagent.so").relative_to(root)),
    )

    report.changed = manifest_changed or bool(report.installed or report.updated)
    if report.changed and not dry_run:
        if backup and backup_dir is not None and manifest_changed:
            _backup(manifest, root, backup_dir)
        if manifest_changed:
            manifest.write_text(patched, encoding="utf-8")

    return report


def encode_script(source: str | Path | bytes) -> str:
    """Codifica un script Lua en base64 y valida el tamaño."""
    if isinstance(source, bytes):
        data = source
    else:
        path = Path(source)
        if not path.is_file():
            raise AgentError(f"No existe el script: {path}")
        data = path.read_bytes()
    if len(data) > MAX_SCRIPT_BYTES:
        raise AgentError(
            f"Script demasiado grande: {len(data)} bytes "
            f"(máximo {MAX_SCRIPT_BYTES})")
    return base64.b64encode(data).decode("ascii")


def build_broadcast_argv(
    package: str,
    op: str,
    *,
    b64: str | None = None,
    name: str | None = None,
    host: str | None = None,
    port: int | None = None,
    action: str = ACTION,
    receiver: str = RECEIVER,
    adb: bool = False,
    serial: str | None = None,
) -> list[str]:
    """Construye el comando ``am broadcast`` para controlar el agente."""
    component = f"{package}/{receiver}"
    cmd = ["adb"] if adb else []
    if adb and serial:
        cmd.extend(["-s", serial])
    if adb:
        cmd.append("shell")
    cmd.extend(["am", "broadcast", "-f", "0x20", "-a", action, "-n",
                component, "--es", "op", op])
    if b64 is not None:
        cmd.extend(["--es", "b64", b64])
    if name is not None:
        cmd.extend(["--es", "name", name])
    if host:
        cmd.extend(["--es", "host", host])
    if port:
        cmd.extend(["--es", "port", str(port)])
    return cmd
