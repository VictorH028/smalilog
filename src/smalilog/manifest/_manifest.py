"""Lectura, análisis y parcheo de AndroidManifest.xml."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from xml.etree import ElementTree as ET

ANDROID_NS = "http://schemas.android.com/apk/res/android"
ANDROID = f"{{{ANDROID_NS}}}"
INTERNET = "android.permission.INTERNET"
CLEARTEXT = "android:usesCleartextTraffic"

COMPONENT_TAGS = {"activity", "activity-alias", "service", "receiver", "provider"}

BASE_TYPES = {
    "Landroid/app/Application;": "application",
    "Landroidx/multidex/MultiDexApplication;": "application",
    "Landroid/app/Activity;": "activity",
    "Landroid/app/ListActivity;": "activity",
    "Landroid/app/TabActivity;": "activity",
    "Landroid/preference/PreferenceActivity;": "activity",
    "Landroidx/activity/ComponentActivity;": "activity",
    "Landroidx/fragment/app/FragmentActivity;": "activity",
    "Landroidx/appcompat/app/AppCompatActivity;": "activity",
    "Landroid/app/Service;": "service",
    "Landroid/app/IntentService;": "service",
    "Landroid/app/job/JobService;": "service",
    "Landroidx/core/app/JobIntentService;": "service",
    "Landroid/content/BroadcastReceiver;": "receiver",
    "Landroid/content/ContentProvider;": "provider",
}


class ManifestError(Exception):
    """Error de lectura, análisis o escritura del manifiesto."""


@dataclass
class IntentFilter:
    """Intent-filter declarado por un componente."""

    actions: list[str] = field(default_factory=list)
    categories: list[str] = field(default_factory=list)
    data: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, list[str]]:
        return {
            "actions": list(self.actions),
            "categories": list(self.categories),
            "data": list(self.data),
        }


@dataclass
class Component:
    """Componente de Android declarado en el manifiesto."""

    kind: str
    name: str
    exported: bool | None = None
    enabled: bool | None = None
    permission: str | None = None
    process: str | None = None
    target_activity: str | None = None
    intent_filters: list[IntentFilter] = field(default_factory=list)

    @property
    def launcher(self) -> bool:
        """Indica si el componente es un launcher (MAIN + LAUNCHER)."""
        for intent_filter in self.intent_filters:
            if ("android.intent.action.MAIN" in intent_filter.actions and
                    any(cat.startswith("android.intent.category.")
                        and cat.endswith("LAUNCHER")
                        for cat in intent_filter.categories)):
                return True
        return False

    def deep_links(self) -> list[str]:
        """Devuelve los enlaces profundos declarados en los intent-filter."""
        links: list[str] = []
        for intent_filter in self.intent_filters:
            links.extend(intent_filter.data)
        return links

    def to_dict(self) -> dict[str, object]:
        return {
            "kind": self.kind,
            "name": self.name,
            "exported": self.exported,
            "enabled": self.enabled,
            "permission": self.permission,
            "process": self.process,
            "target_activity": self.target_activity,
            "launcher": self.launcher,
            "deep_links": self.deep_links(),
            "intent_filters": [f.to_dict() for f in self.intent_filters],
        }


@dataclass
class SmaliEntry:
    """Clase Smali que hereda de un tipo de entrada Android."""

    kind: str
    name: str
    path: str
    attach_base_context: bool = False
    on_create: bool = False

    def to_dict(self) -> dict[str, object]:
        return {
            "kind": self.kind,
            "name": self.name,
            "path": self.path,
            "attach_base_context": self.attach_base_context,
            "on_create": self.on_create,
        }


@dataclass
class ManifestInfo:
    """Resumen del AndroidManifest.xml."""

    path: Path
    package: str
    version_name: str | None = None
    version_code: str | None = None
    application: str | None = None
    debuggable: bool | None = None
    cleartext: bool | None = None
    network_security_config: str | None = None
    permissions: list[str] = field(default_factory=list)
    components: list[Component] = field(default_factory=list)
    smali_entries: list[SmaliEntry] = field(default_factory=list)

    @property
    def launchers(self) -> list[Component]:
        return [component for component in self.components if component.launcher]

    def to_dict(self) -> dict[str, object]:
        return {
            "path": str(self.path),
            "package": self.package,
            "version_name": self.version_name,
            "version_code": self.version_code,
            "application": self.application,
            "debuggable": self.debuggable,
            "cleartext": self.cleartext,
            "network_security_config": self.network_security_config,
            "permissions": list(self.permissions),
            "launchers": [c.name for c in self.launchers],
            "components": [c.to_dict() for c in self.components],
            "smali_entries": [e.to_dict() for e in self.smali_entries],
        }


@dataclass
class PatchResult:
    """Resultado de modificar el manifiesto."""

    path: Path
    output: Path | None = None
    changed: bool = False
    added_permissions: list[str] = field(default_factory=list)
    cleartext_changed: bool = False
    warning: str | None = None


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _attr(element: ET.Element, name: str) -> str | None:
    value = element.get(ANDROID + name)
    if value is not None:
        return value
    for key, candidate in element.attrib.items():
        if _local_name(key) == name:
            return candidate
    return None


def _plain_attr(element: ET.Element, name: str) -> str | None:
    value = element.get(name)
    if value is not None:
        return value
    for key, candidate in element.attrib.items():
        if _local_name(key) == name:
            return candidate
    return None


def _as_bool(value: str | None) -> bool | None:
    if value is None:
        return None
    return value.strip().lower() == "true"


def _find_child(parent: ET.Element, name: str) -> ET.Element | None:
    for child in parent:
        if _local_name(child.tag) == name:
            return child
    return None


def _parse_intent_filter(element: ET.Element) -> IntentFilter:
    intent_filter = IntentFilter()
    for child in element:
        tag = _local_name(child.tag)
        if tag == "action":
            value = _attr(child, "name")
            if value:
                intent_filter.actions.append(value)
        elif tag == "category":
            value = _attr(child, "name")
            if value:
                intent_filter.categories.append(value)
        elif tag == "data":
            intent_filter.data.append(_format_data(child))
    return intent_filter


def _format_data(element: ET.Element) -> str:
    scheme = _attr(element, "scheme")
    host = _attr(element, "host")
    port = _attr(element, "port")
    path = _attr(element, "path")
    path_prefix = _attr(element, "pathPrefix")
    path_pattern = _attr(element, "pathPattern")
    mime_type = _attr(element, "mimeType")

    if scheme or host:
        result = f"{scheme or '?'}://{host or '?'}"
        if port:
            result += f":{port}"
        result += path or path_prefix or path_pattern or ""
        return result
    if mime_type:
        return f"mime:{mime_type}"
    return "data"


def _parse_component(element: ET.Element, kind: str) -> Component:
    component = Component(
        kind=kind,
        name=_attr(element, "name") or "(sin nombre)",
        exported=_as_bool(_attr(element, "exported")),
        enabled=_as_bool(_attr(element, "enabled")),
        permission=_attr(element, "permission"),
        process=_attr(element, "process"),
        target_activity=_attr(element, "targetActivity"),
    )
    for child in element:
        if _local_name(child.tag) == "intent-filter":
            component.intent_filters.append(_parse_intent_filter(child))
    return component


def parse_manifest(path: str | Path) -> ManifestInfo:
    """Lee un AndroidManifest.xml en texto y extrae su estructura."""
    manifest_path = Path(path)
    if not manifest_path.is_file():
        raise ManifestError(f"No existe el manifiesto: {manifest_path}")

    try:
        tree = ET.parse(manifest_path)
    except ET.ParseError as exc:
        raise ManifestError(
            "No se pudo leer el AndroidManifest.xml. Si es binario (AXML), "
            "descompila la APK primero (por ejemplo: apkeditor d)."
        ) from exc

    root = tree.getroot()
    if _local_name(root.tag) != "manifest":
        raise ManifestError(
            f"El archivo no parece un AndroidManifest.xml: {manifest_path}")

    package = _plain_attr(root, "package") or "(sin package)"
    info = ManifestInfo(
        path=manifest_path,
        package=package,
        version_name=_attr(root, "versionName"),
        version_code=_attr(root, "versionCode"),
    )

    for child in root:
        tag = _local_name(child.tag)
        if tag in {"uses-permission", "uses-permission-sdk-23"}:
            name = _attr(child, "name")
            if name and name not in info.permissions:
                info.permissions.append(name)

    application = _find_child(root, "application")
    if application is not None:
        info.application = _attr(application, "name")
        info.debuggable = _as_bool(_attr(application, "debuggable"))
        info.cleartext = _as_bool(_attr(application, "usesCleartextTraffic"))
        info.network_security_config = _attr(application, "networkSecurityConfig")
        for child in application:
            kind = _local_name(child.tag)
            if kind in COMPONENT_TAGS:
                info.components.append(_parse_component(child, kind))

    return info


def _compute_indent(text: str, position: int) -> str:
    line_start = text.rfind("\n", 0, position) + 1
    match = re.match(r"[ \t]*", text[line_start:position])
    return match.group(0) if match else ""


def _has_permission(text: str, permission: str) -> bool:
    pattern = re.compile(
        r"<uses-permission(?:-sdk-23)?\b[^>]*\bandroid:name\s*=\s*"
        rf"[\"']{re.escape(permission)}[\"']",
        re.S,
    )
    return bool(pattern.search(text))


def _add_permission(text: str, permission: str) -> tuple[str, bool]:
    if _has_permission(text, permission):
        return text, False

    permission_line = f'<uses-permission android:name="{permission}" />'
    application = re.search(r"<application\b[^>]*>", text, re.S)
    if application:
        position = application.start()
        line_start = text.rfind("\n", 0, position) + 1
        if not text[line_start:position].strip():
            indent = _compute_indent(text, position)
            insertion = f"{indent}{permission_line}\n"
            return text[:line_start] + insertion + text[line_start:], True

    manifest = re.search(r"<manifest\b[^>]*>", text, re.S)
    if not manifest:
        raise ManifestError("El manifiesto no contiene la etiqueta <manifest>.")
    indent = _compute_indent(text, manifest.start())
    insertion = f"\n{indent}    {permission_line}\n"
    position = manifest.end()
    if position < len(text) and text[position] == "\n":
        position += 1
    return text[:position] + insertion + text[position:], True


def _patch_cleartext(text: str) -> tuple[str, bool]:
    application = re.search(r"<application\b[^>]*>", text, re.S)
    if not application:
        raise ManifestError("El manifiesto no contiene la etiqueta <application>.")

    tag = application.group(0)
    attribute = re.compile(
        r"(android:usesCleartextTraffic\s*=\s*)([\"'])([^\"']*)\2", re.S)
    existing = attribute.search(tag)
    if existing:
        if existing.group(3).strip().lower() == "true":
            return text, False
        new_tag = attribute.sub(r"\1\2true\2", tag, count=1)
    elif tag.rstrip().endswith("/>"):
        new_tag = tag[:-2].rstrip() + f' {CLEARTEXT}="true" />'
    else:
        new_tag = tag[:-1].rstrip() + f' {CLEARTEXT}="true">'

    return text[:application.start()] + new_tag + text[application.end():], True


def patch_manifest(
    path: str | Path,
    permissions: list[str] | None = None,
    cleartext: bool = True,
    output: str | Path | None = None,
    dry_run: bool = False,
    no_backup: bool = False,
) -> PatchResult:
    """Agrega permisos y habilita tráfico HTTP en claro.

    Args:
        path: AndroidManifest.xml de entrada.
        permissions: Permisos a agregar. Si es ``None``, agrega solo
            ``android.permission.INTERNET``.
        cleartext: Agrega ``android:usesCleartextTraffic="true"``.
        output: Archivo de salida; si se omite, modifica ``path``.
        dry_run: No escribe archivos, solo calcula los cambios.
        no_backup: No crea ``AndroidManifest.xml.bak``.

    Returns:
        El resultado de la modificación.

    Raises:
        ManifestError: Si el archivo no existe o no es un manifiesto válido.
    """
    manifest_path = Path(path)
    if not manifest_path.is_file():
        raise ManifestError(f"No existe el manifiesto: {manifest_path}")

    text = manifest_path.read_text(encoding="utf-8")
    to_add = [INTERNET] if permissions is None else permissions
    added: list[str] = []
    for permission in to_add:
        text, changed = _add_permission(text, permission)
        if changed:
            added.append(permission)

    cleartext_changed = False
    warning = None
    if cleartext:
        if re.search(r"android:networkSecurityConfig\s*=", text):
            warning = (
                "El manifiesto usa android:networkSecurityConfig; puede "
                "ignorar usesCleartextTraffic. Revisa la configuración de red."
            )
        text, cleartext_changed = _patch_cleartext(text)

    output_path = Path(output) if output else None
    changed = bool(added) or cleartext_changed
    if changed and not dry_run:
        if output_path is None and not no_backup:
            backup = manifest_path.with_name(manifest_path.name + ".bak")
            backup.write_text(
                manifest_path.read_text(encoding="utf-8"), encoding="utf-8")
        destination = output_path or manifest_path
        destination.write_text(text, encoding="utf-8")

    return PatchResult(
        path=manifest_path,
        output=output_path,
        changed=changed,
        added_permissions=added,
        cleartext_changed=cleartext_changed,
        warning=warning,
    )


def scan_smali_entries(path: str | Path) -> list[SmaliEntry]:
    """Busca clases Smali que heredan de componentes Android."""
    root = Path(path)
    if not root.exists():
        raise ManifestError(f"No existe la ruta Smali: {root}")

    files = [root] if root.is_file() else sorted(root.rglob("*.smali"))
    entries: list[SmaliEntry] = []
    class_re = re.compile(r"^\.class\s+.*?(L[^;\s]+;)", re.M)
    super_re = re.compile(r"^\.super\s+(L[^;\s]+;)", re.M)

    for smali_file in files:
        try:
            text = smali_file.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        super_match = super_re.search(text)
        if not super_match:
            continue
        kind = BASE_TYPES.get(super_match.group(1))
        if kind is None:
            continue
        class_match = class_re.search(text)
        if not class_match:
            continue
        entries.append(SmaliEntry(
            kind=kind,
            name=class_match.group(1),
            path=str(smali_file),
            attach_base_context=(
                "attachBaseContext(Landroid/content/Context;)V" in text),
            on_create=bool(re.search(
                r"^\.method\s+.*\bonCreate\(", text, re.M)),
        ))
    return entries
