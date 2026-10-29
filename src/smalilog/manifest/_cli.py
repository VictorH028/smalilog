"""CLI del subcomando ``smalilog manifest``."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from smalilog.ui import Color, _c, log_error, log_header, log_info, log_ok, log_warn

from ._manifest import (
    INTERNET,
    Component,
    ManifestError,
    ManifestInfo,
    SmaliEntry,
    parse_manifest,
    patch_manifest,
    scan_smali_entries,
)


def _add_manifest_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "manifest",
        metavar="ANDROIDMANIFEST",
        help="Ruta a AndroidManifest.xml ya descompilado (texto).",
    )


def _add_json_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--json", action="store_true",
        help="Muestra el resultado en JSON para automatizar.",
    )


def _add_smali_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--smali-dir", metavar="RUTA",
        help="Raíz del APK descompilado o archivo .smali para buscar "
             "clases que heredan directamente de Application/Activity/Service/Receiver.",
    )


def build_manifest_parser(
    prog: str = "smalilog manifest",
) -> argparse.ArgumentParser:
    """Construye el parser del subcomando ``manifest``."""
    parser = argparse.ArgumentParser(
        prog=prog,
        description=(
            "Analiza y modifica AndroidManifest.xml:\n"
            "  - agrega permisos (INTERNET por defecto);\n"
            "  - habilita tráfico HTTP en claro (localhost);\n"
            "  - lista puntos de entrada declarados y clases Smali."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Ejemplos:
  smalilog manifest info apk/AndroidManifest.xml
  smalilog manifest entrypoints apk/AndroidManifest.xml --smali-dir apk
  smalilog manifest fix apk/AndroidManifest.xml
  smalilog manifest fix apk/AndroidManifest.xml --permission android.permission.ACCESS_NETWORK_STATE
  smalilog manifest fix apk/AndroidManifest.xml --no-cleartext --dry-run
  smalilog manifest permissions apk/AndroidManifest.xml --json

El manifiesto debe estar en texto. Si está en binario (AXML), descompila
la APK primero, por ejemplo: apkeditor d -i app.apk -o ./apk
""",
    )
    sub = parser.add_subparsers(dest="cmd", metavar="<cmd>", required=True)

    p = sub.add_parser(
        "info",
        help="Resumen del manifiesto y puntos de entrada",
        description="Muestra paquete, aplicación, permisos y componentes.",
    )
    _add_manifest_arg(p)
    _add_smali_arg(p)
    _add_json_arg(p)

    p = sub.add_parser(
        "entrypoints",
        help="Lista actividades, servicios, receivers y providers",
        description=(
            "Lista los puntos de entrada declarados. Con --smali-dir "
            "también busca clases Smali que heredan directamente de componentes Android."
        ),
    )
    _add_manifest_arg(p)
    _add_smali_arg(p)
    _add_json_arg(p)

    p = sub.add_parser(
        "permissions",
        help="Lista los permisos declarados",
        description="Muestra los permisos de la aplicación.",
    )
    _add_manifest_arg(p)
    _add_json_arg(p)

    p = sub.add_parser(
        "fix",
        help="Agrega INTERNET y habilita tráfico en claro",
        description=(
            "Agrega android.permission.INTERNET y "
            "android:usesCleartextTraffic=\"true\" si faltan. "
            "Crea una copia .bak salvo que uses --no-backup o --output."
        ),
    )
    _add_manifest_arg(p)
    p.add_argument(
        "--permission", action="append", default=[], metavar="PERMISO",
        help="Permiso adicional a agregar (repetible).",
    )
    p.add_argument(
        "--no-internet", action="store_true",
        help="No agrega android.permission.INTERNET.",
    )
    p.add_argument(
        "--no-cleartext", action="store_true",
        help="No modifica android:usesCleartextTraffic.",
    )
    p.add_argument(
        "-o", "--output", metavar="ARCHIVO",
        help="Escribe el resultado en otro archivo en vez de modificar el original.",
    )
    p.add_argument(
        "--dry-run", action="store_true",
        help="Muestra los cambios sin escribir archivos.",
    )
    p.add_argument(
        "--no-backup", action="store_true",
        help="No crea AndroidManifest.xml.bak.",
    )

    return parser


def _format_component(component: Component) -> str:
    flags: list[str] = []
    if component.launcher:
        flags.append("launcher")
    if component.exported is True:
        flags.append("exported")
    elif component.exported is False:
        flags.append("no-exported")
    else:
        flags.append("exported=?")
    if component.enabled is False:
        flags.append("disabled")
    if component.target_activity:
        flags.append(f"target={component.target_activity}")

    detail = ""
    if flags:
        detail = f"  {_c(Color.DIM, ' '.join(flags))}"
    return f"  [{component.kind}] {component.name}{detail}"


def _print_info(info: ManifestInfo) -> None:
    log_header(f"Manifiesto: {info.path}")
    print(f"Paquete          : {info.package}")
    if info.version_name or info.version_code:
        print(f"Versión          : {info.version_name or '?'} "
              f"({info.version_code or '?'})")
    print(f"Aplicación       : {info.application or '(sin android:name)'}")
    print(f"debuggable       : {_format_optional_bool(info.debuggable)}")
    print(f"cleartextTraffic : {_format_optional_bool(info.cleartext)}")
    if info.network_security_config:
        print(f"networkSecurity  : {info.network_security_config}")

    launchers = info.launchers
    if launchers:
        print("Launcher         : " + ", ".join(c.name for c in launchers))
    else:
        print("Launcher         : (no declarado)")

    print()
    print(f"Permisos ({len(info.permissions)}):")
    if info.permissions:
        for permission in info.permissions:
            print(f"  - {permission}")
    else:
        print("  (ninguno)")

    print()
    _print_components(info.components)
    if info.smali_entries:
        print()
        _print_smali_entries(info.smali_entries)


def _print_components(components: list[Component]) -> None:
    print(f"Puntos de entrada declarados ({len(components)}):")
    if not components:
        print("  (ninguno)")
        return
    for component in components:
        print(_format_component(component))
        if component.permission:
            print(f"       permiso: {component.permission}")
        links = component.deep_links()
        for link in links:
            print(f"       {_c(Color.CYAN, link)}")


def _print_smali_entries(entries: list[SmaliEntry]) -> None:
    print(f"Clases Smali de entrada ({len(entries)}):")
    for entry in entries:
        details = []
        if entry.attach_base_context:
            details.append("attachBaseContext")
        if entry.on_create:
            details.append("onCreate")
        suffix = f"  {_c(Color.DIM, ', '.join(details))}" if details else ""
        print(f"  [{entry.kind}] {entry.name}{suffix}")
        print(f"       {_c(Color.DIM, entry.path)}")


def _format_optional_bool(value: bool | None) -> str:
    if value is None:
        return "(no definido)"
    return "true" if value else "false"


def _load_info(args: argparse.Namespace) -> ManifestInfo:
    info = parse_manifest(args.manifest)
    if args.smali_dir:
        info.smali_entries = scan_smali_entries(args.smali_dir)
    return info


def _cmd_info(args: argparse.Namespace) -> int:
    info = _load_info(args)
    if args.json:
        print(json.dumps(info.to_dict(), ensure_ascii=False, indent=2))
        return 0
    _print_info(info)
    return 0


def _cmd_entrypoints(args: argparse.Namespace) -> int:
    info = _load_info(args)
    if args.json:
        payload = info.to_dict()
        print(json.dumps({
            "path": payload["path"],
            "package": payload["package"],
            "launchers": payload["launchers"],
            "components": payload["components"],
            "smali_entries": payload["smali_entries"],
        }, ensure_ascii=False, indent=2))
        return 0

    log_header(f"Puntos de entrada: {info.path}")
    print(f"Paquete: {info.package}")
    if info.launchers:
        print("Launcher: " + ", ".join(c.name for c in info.launchers))
    print()
    _print_components(info.components)
    if info.smali_entries:
        print()
        _print_smali_entries(info.smali_entries)
    return 0


def _cmd_permissions(args: argparse.Namespace) -> int:
    info = parse_manifest(args.manifest)
    if args.json:
        print(json.dumps({"permissions": info.permissions},
                         ensure_ascii=False, indent=2))
        return 0
    log_header(f"Permisos: {info.path}")
    if not info.permissions:
        print("(ninguno)")
    for permission in info.permissions:
        print(f"  - {permission}")
    return 0


def _cmd_fix(args: argparse.Namespace) -> int:
    permissions: list[str] = []
    if not args.no_internet:
        permissions.append(INTERNET)
    for permission in args.permission:
        permission = permission.strip()
        if permission and permission not in permissions:
            permissions.append(permission)

    result = patch_manifest(
        args.manifest,
        permissions=permissions,
        cleartext=not args.no_cleartext,
        output=args.output,
        dry_run=args.dry_run,
        no_backup=args.no_backup,
    )

    if result.warning:
        log_warn(result.warning)

    if not result.changed:
        log_info("Sin cambios: el manifiesto ya tenía lo necesario.")
        return 0

    for permission in result.added_permissions:
        log_ok(f"Permiso agregado: {permission}")
    if result.cleartext_changed:
        log_ok('Agregado android:usesCleartextTraffic="true"')

    if args.dry_run:
        log_info("dry-run: no se escribió ningún archivo.")
    else:
        destination = result.output or result.path
        log_ok(f"Escrito: {destination}")
        if args.output is None and not args.no_backup:
            backup = Path(str(result.path) + ".bak")
            log_info(f"Copia de seguridad: {backup}")
    return 0


def run_manifest(argv: list[str] | None = None,
                 prog: str = "smalilog manifest") -> int:
    """Punto de entrada del subcomando ``smalilog manifest``."""
    parser = build_manifest_parser(prog=prog)
    args = parser.parse_args(argv)

    try:
        if args.cmd == "info":
            return _cmd_info(args)
        if args.cmd == "entrypoints":
            return _cmd_entrypoints(args)
        if args.cmd == "permissions":
            return _cmd_permissions(args)
        if args.cmd == "fix":
            return _cmd_fix(args)
    except ManifestError as exc:
        log_error(str(exc))
        return 1

    parser.error(f"subcomando desconocido: {args.cmd}")
    return 2
