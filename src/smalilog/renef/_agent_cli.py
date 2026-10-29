"""CLI para instalar y controlar el agente Renef embebido."""
from __future__ import annotations

import argparse
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

from smalilog.manifest._manifest import ManifestError
from smalilog.ui import log_error, log_header, log_info, log_ok, log_warn

from ._agent import (
    ACTION,
    RECEIVER,
    AgentError,
    build_broadcast_argv,
    detect_package,
    encode_script,
    install_payload,
)

TOOLZ = Path(os.environ.get("PREFIX", "/data/data/com.termux/files/usr")) / \
    "lib" / "termux-apk-make" / "toolz"


def _add_runtime_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--package", metavar="APP",
                        help="Package de la APK instrumentada.")
    parser.add_argument("--apk-dir", default=".", metavar="DIR",
                        help="APK descompilada para leer el package "
                             "(por defecto: directorio actual).")
    parser.add_argument("--manifest", metavar="XML",
                        help="AndroidManifest.xml concreto.")
    parser.add_argument("--adb", action="store_true",
                        help="Ejecuta el broadcast con adb (dispositivo externo).")
    parser.add_argument("--serial", metavar="SERIE",
                        help="Serie de adb (implica --adb).")
    parser.add_argument("--host", metavar="IP",
                        help="Host del servidor smalilog para los logs.")
    parser.add_argument("--port", type=int, metavar="PUERTO",
                        help="Puerto del servidor smalilog.")
    parser.add_argument("--action", default=ACTION,
                        help="Action del receptor (por defecto: %(default)s).")
    parser.add_argument("--receiver", default=RECEIVER,
                        help="Clase del receptor (por defecto: %(default)s).")
    parser.add_argument("--dry-run", action="store_true",
                        help="Muestra el comando sin ejecutarlo.")


def add_agent_subparsers(sub: argparse._SubParsersAction) -> None:
    """Añade ``install`` y ``runtime`` al parser de ``smalilog renef``."""
    p = sub.add_parser(
        "install",
        help="Instala el agente embebido en una APK descompilada",
        description=(
            "Copia libagent.so, añade el puente Smali y parchea el manifiesto "
            "con el receptor exportado, INTERNET y tráfico HTTP en claro.\n"
            "No requiere root: el agente se ejecuta dentro del proceso de la app."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Ejemplos:
  smalilog renef install ./apk
  smalilog renef install ./apk --build -o app-instrumentada.apk
  smalilog renef install ./apk --no-cleartext --dry-run

Después del parcheo:
  apkeditor b -i ./apk -o ./app-unsigned.apk
  apksigner sign --ks clave.jks --out ./app.apk ./app-unsigned.apk
""",
    )
    p.add_argument("apk_dir", metavar="APK_DESCOMPILADA",
                   help="Directorio con AndroidManifest.xml y smali/.")
    p.add_argument("--agent-so", metavar="RUTA",
                   help="libagent.so alternativo (arm64-v8a).")
    p.add_argument("--payload-dir", metavar="RUTA",
                   help="Directorio payload alternativo (para pruebas).")
    p.add_argument("--permission", action="append", default=[],
                   metavar="PERMISO",
                   help="Permiso adicional que agregar (repetible).")
    p.add_argument("--no-internet", action="store_true",
                   help="No agregar android.permission.INTERNET.")
    p.add_argument("--no-cleartext", action="store_true",
                   help="No habilitar usesCleartextTraffic.")
    p.add_argument("--force", action="store_true",
                   help="Reemplaza clases o libagent.so existentes.")
    p.add_argument("--no-backup", action="store_true",
                   help="No crear el respaldo externo.")
    p.add_argument("--dry-run", action="store_true",
                   help="No escribe archivos; solo muestra el plan.")
    p.add_argument("--build", action="store_true",
                   help="Compila la APK con apkeditor después de parchear.")
    p.add_argument("-o", "--output", metavar="APK",
                   help="APK de salida para --build.")
    p.add_argument("--ks", metavar="KEYSTORE",
                   help="Keystore para firmar (por defecto: el de termux-apk-make).")
    p.add_argument("--ks-pass", default="password", metavar="CLAVE",
                   help="Clave del keystore (por defecto: password).")

    p = sub.add_parser(
        "runtime",
        help="Controla la APK instrumentada sin root (broadcast + agente)",
        description=(
            "Envía órdenes al receptor del agente mediante am broadcast. "
            "El agente ejecuta Lua dentro del proceso de la app y devuelve "
            "los logs al servidor smalilog."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Ejemplos:
  smalilog renef runtime status --apk-dir ./apk
  smalilog renef runtime exec script.lua --apk-dir ./apk
  smalilog renef runtime exec --code 'print("hola")' --package com.demo
  smalilog renef runtime push hook.lua --apk-dir ./apk
  smalilog renef runtime unhook --apk-dir ./apk
  smalilog renef runtime status --adb --serial emulator-5554
""",
    )
    rsub = p.add_subparsers(dest="runtime_cmd", metavar="<cmd>", required=True)

    p = rsub.add_parser("exec", help="Ejecuta un script Lua en la app")
    _add_runtime_common(p)
    p.add_argument("script", nargs="?", help="Archivo .lua a ejecutar.")
    p.add_argument("--code", help="Código Lua en línea (alternativa a script).")

    p = rsub.add_parser("push", help="Guarda y ejecuta un script Lua")
    _add_runtime_common(p)
    p.add_argument("script", help="Archivo .lua a guardar y ejecutar.")
    p.add_argument("--name", help="Nombre del script en la app.")

    p = rsub.add_parser("status", help="Comprueba el agente y el hook activo")
    _add_runtime_common(p)

    p = rsub.add_parser("ping", help="Comprueba solo el receptor")
    _add_runtime_common(p)

    p = rsub.add_parser("unhook", help="Cierra la sesión y restaura los hooks")
    _add_runtime_common(p)


def _resolve_package(args: argparse.Namespace) -> str:
    if args.package:
        return args.package
    try:
        if args.manifest:
            from smalilog.manifest._manifest import ManifestError, parse_manifest
            package = parse_manifest(args.manifest).package
            if package and package != "(sin package)":
                return package
        return detect_package(args.apk_dir)
    except (AgentError, ManifestError) as exc:
        raise AgentError(
            f"{exc}\nIndica --package o ejecuta desde la APK descompilada.") from exc


def _run(argv: list[str], *, timeout: int = 30) -> int:
    try:
        result = subprocess.run(
            argv, capture_output=True, text=True, timeout=timeout)
    except FileNotFoundError:
        log_error(f"Comando no encontrado: {argv[0]}")
        return 127
    except subprocess.TimeoutExpired:
        log_error(f"Tiempo agotado ejecutando: {argv[0]}")
        return 124
    output = (result.stdout or "").strip()
    error = (result.stderr or "").strip()
    if output:
        print(output)
    if error:
        print(error, file=sys.stderr)
    return result.returncode


def _broadcast(args: argparse.Namespace, op: str, **kwargs) -> int:
    package = _resolve_package(args)
    argv = build_broadcast_argv(
        package, op,
        b64=kwargs.get("b64"),
        name=kwargs.get("name"),
        host=args.host,
        port=args.port,
        action=args.action,
        receiver=args.receiver,
        adb=args.adb or bool(args.serial),
        serial=args.serial,
    )
    if args.dry_run:
        print(shlex.join(argv))
        return 0
    return _run(argv)


def _cmd_install(args: argparse.Namespace) -> int:
    log_header(f"Instalando agente Renef en {args.apk_dir}")
    try:
        report = install_payload(
            args.apk_dir,
            agent_so=args.agent_so,
            payload_dir=args.payload_dir,
            force=args.force,
            backup=not args.no_backup,
            dry_run=args.dry_run,
            internet=not args.no_internet,
            cleartext=not args.no_cleartext,
            permissions=args.permission,
        )
    except (AgentError, ManifestError) as exc:
        log_error(str(exc))
        return 1

    if args.dry_run:
        log_warn("Dry-run: no se escribieron archivos")
    print()
    log_info(report.summary())
    if report.warnings:
        for warning in report.warnings:
            log_warn(warning)
    if not report.changed:
        log_ok("El payload ya estaba instalado; no hay cambios")
    print()
    try:
        package = detect_package(args.apk_dir)
    except AgentError:
        package = "<package>"
    log_info("Control sin root:")
    log_info(f"  smalilog renef runtime status --package {package}")
    log_info(f"  smalilog renef runtime exec hook.lua --package {package}")
    if not args.no_cleartext:
        log_info("  (inicia `smalilog server` para recibir los logs)")

    if args.build:
        if args.dry_run:
            log_warn("--dry-run no compila la APK")
            return 0
        return _build_apk(args)
    return 0


def _find_tool(name: str) -> str | None:
    found = shutil.which(name)
    if found:
        return found
    candidate = TOOLZ / name
    if candidate.is_file():
        return str(candidate)
    return None


def _build_apk(args: argparse.Namespace) -> int:
    apkeditor = _find_tool("apkeditor")
    if not apkeditor:
        log_error("No se encontró apkeditor para --build")
        return 1
    app = Path(args.apk_dir).resolve()
    if args.output:
        signed = Path(args.output)
    else:
        signed = app.with_name(app.name + "-smalilog.apk")
    unsigned = signed.with_name(signed.stem + "-unsigned.apk")
    unsigned.parent.mkdir(parents=True, exist_ok=True)
    log_header(f"Compilando APK con apkeditor → {unsigned}")
    rc = _run([apkeditor, "b", "-i", str(args.apk_dir), "-o", str(unsigned),
               "-f"], timeout=600)
    if rc != 0:
        return rc

    apksigner = _find_tool("apksigner")
    if not apksigner:
        log_warn(f"APK sin firmar: {unsigned}")
        return 0
    ks = Path(args.ks) if args.ks else TOOLZ / "key.keystore"
    if not ks.is_file():
        log_warn(f"No existe el keystore {ks}; APK sin firmar: {unsigned}")
        return 0
    log_header(f"Firmando APK → {signed}")
    rc = _run([
        apksigner, "sign", "--ks", str(ks), "--ks-pass", f"pass:{args.ks_pass}",
        "--min-sdk-version", "24", "--out", str(signed), str(unsigned),
    ], timeout=300)
    if rc == 0:
        log_ok(f"APK firmada: {signed}")
    return rc


def run_agent_command(args: argparse.Namespace) -> int:
    """Ejecuta un subcomando ``install`` o ``runtime``."""
    if args.cmd == "install":
        return _cmd_install(args)

    op = {
        "exec": "EXEC",
        "push": "PUSH",
        "status": "STATUS",
        "ping": "PING",
        "unhook": "UNHOOK",
    }[args.runtime_cmd]

    if args.runtime_cmd == "exec":
        if bool(args.script) == bool(args.code):
            log_error("Indica un script .lua o --code (no ambos)")
            return 2
        try:
            b64 = encode_script(
                args.code.encode("utf-8") if args.code else args.script)
        except AgentError as exc:
            log_error(str(exc))
            return 1
        return _broadcast(args, op, b64=b64)

    if args.runtime_cmd == "push":
        try:
            b64 = encode_script(args.script)
        except AgentError as exc:
            log_error(str(exc))
            return 1
        name = args.name or Path(args.script).name
        return _broadcast(args, op, b64=b64, name=name)

    return _broadcast(args, op)
