#!/usr/bin/env python3
"""
CLI de smalilog.

Subcomandos:
    smalilog server [opciones]    Arranca el servidor de logs.
    smalilog hook   [opciones]    Inyecta hooks en un archivo Smali.

Si no se especifica subcomando, se asume `server`.

Ejemplos:
    smalilog                                  # servidor por defecto
    smalilog server --host 0.0.0.0 -p 8080
    smalilog hook archivo.smali --list
    smalilog hook archivo.smali -m Sf -a both
    smalilog hook archivo.smali -m Sf -a d --tag APP --message "hola"
"""

from __future__ import annotations

import argparse
import logging
import sys

from . import config
from .server import LogServer
from .injector.hooker import run_hooker


LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


# --------------------------------------------------------------------------- #
#  Subparser: server
# --------------------------------------------------------------------------- #
def _add_server_parser(subparsers) -> None:
    p = subparsers.add_parser(
        "server",
        help="Arranca el servidor de logs (POST /log).",
        description="Arranca el servidor HTTP que recibe logs JSON.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Ejemplo de petición:\n"
            "  curl -X POST http://127.0.0.1:9999/log \\\n"
            "       -H 'Content-Type: application/json' \\\n"
            "       -d '{\"level\":\"INFO\",\"tag\":\"APP\",\"message\":\"hola\"}'\n"
        ),
    )
    p.add_argument("--host", default=config.DEFAULT_HOST,
                   help="Host donde escuchar (por defecto: %(default)s).")
    p.add_argument("-p", "--port", type=int, default=config.DEFAULT_PORT,
                   help="Puerto TCP (por defecto: %(default)s).")
    p.add_argument("-f", "--log-file", default=config.DEFAULT_LOG_FILE,
                   help="Archivo de logs (por defecto: %(default)s).")
    p.add_argument("-l", "--log-level", default=config.DEFAULT_LOG_LEVEL,
                   choices=sorted(LOG_LEVELS.keys()), type=str.upper,
                   help="Nivel mínimo de log (por defecto: %(default)s).")
    p.add_argument("--max-headers", type=int, default=config.MAX_HEADERS,
                   help="Tamaño máximo de cabeceras HTTP (por defecto: %(default)s).")
    p.add_argument("--max-body", type=int, default=config.MAX_BODY,
                   help="Tamaño máximo del cuerpo HTTP (por defecto: %(default)s).")
    p.add_argument("--no-blocking", action="store_true",
                   help="Arranca en un hilo aparte.")
    p.add_argument("-v", "--verbose", action="store_true",
                   help="Muestra información adicional.")


# --------------------------------------------------------------------------- #
#  Subparser: hook
# --------------------------------------------------------------------------- #
def _add_hook_parser(subparsers) -> None:
    """
    Reutilizamos el parser del propio hooker para no duplicar opciones.
    """
    from .injector.hooker import build_hook_parser
    hook_parser = build_hook_parser(prog="smalilog hook")
    # Lo registramos como subparser del principal
    subparsers._name_parser_map["hook"] = hook_parser
    # Y lo exponemos para que aparezca en `--help`
    hook_parser.prog = "smalilog hook"


# --------------------------------------------------------------------------- #
#  Parser principal
# --------------------------------------------------------------------------- #
def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="smalilog",
        description=(
            "Herramienta para instrumentar aplicaciones Android con log "
            "remoto vía Smali + JNI + servidor HTTP."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Ejemplos:\n"
            "  smalilog server --host 0.0.0.0 -p 8080\n"
            "  smalilog hook archivo.smali --list\n"
            "  smalilog hook archivo.smali -m Sf -a both\n"
            "  smalilog hook archivo.smali -m Sf -a d --tag APP --message 'hola'\n"
        ),
    )

    parser.add_argument("--version", action="version",
                        version=f"%(prog)s {config.VERSION}")

    subparsers = parser.add_subparsers(dest="command", metavar="<comando>")
    _add_server_parser(subparsers)
    _add_hook_parser(subparsers)

    return parser


# --------------------------------------------------------------------------- #
#  Handlers
# --------------------------------------------------------------------------- #
def _cmd_server(args: argparse.Namespace) -> int:
    log_level = LOG_LEVELS[args.log_level]

    if args.verbose:
        print(f"Host        : {args.host}")
        print(f"Puerto      : {args.port}")
        print(f"Log file    : {args.log_file}")
        print(f"Log level   : {args.log_level}")
        print(f"Max headers : {args.max_headers} bytes")
        print(f"Max body    : {args.max_body} bytes")
        print(f"Blocking    : {not args.no_blocking}")

    server = LogServer(
        host=args.host,
        port=args.port,
        log_file=args.log_file,
        log_level=log_level,
    )
    server.MAX_HEADERS = args.max_headers
    server.MAX_BODY = args.max_body

    try:
        server.start(blocking=not args.no_blocking)
        if args.no_blocking:
            print("Presiona Ctrl+C para detener el servidor...")
            while server.is_running:
                try:
                    assert server._thread is not None
                    server._thread.join(timeout=0.5)
                except KeyboardInterrupt:
                    break
    except KeyboardInterrupt:
        print("\nInterrupción recibida, cerrando...")
    except OSError as exc:
        print(f"Error al iniciar el servidor: {exc}", file=sys.stderr)
        return 1
    finally:
        server.stop()
    return 0


# --------------------------------------------------------------------------- #
#  Entry point
# --------------------------------------------------------------------------- #
def cli(argv: list[str] | None = None) -> int:
    """
    Punto de entrada del CLI (usado por el entry point `smalilog`).

    - Si el primer argumento es `server` o `hook`, se despacha al subcomando.
    - Si no, se asume `server` (compatibilidad).
    """
    if argv is None:
        argv = sys.argv[1:]

    # Compatibilidad: si no hay subcomando, inyectamos "server"
    if not argv or argv[0] not in ("server", "hook", "-h", "--help", "--version"):
        argv = ["server", *argv]

    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "hook":
        # `run_hooker` reparsea sus propios argumentos.
        # Le pasamos solo lo que va después de "hook".
        hook_argv = sys.argv[2:] if len(sys.argv) > 1 else []
        # Pero si venimos de `cli(argv)`, reconstruimos:
        if argv and argv[0] == "hook":
            hook_argv = argv[1:]
        return run_hooker(hook_argv, prog="smalilog hook")

    if args.command == "server" or args.command is None:
        return _cmd_server(args)

    parser.print_help()
    return 1


# Alias retro-compatible
main = cli


if __name__ == "__main__":
    sys.exit(cli())
