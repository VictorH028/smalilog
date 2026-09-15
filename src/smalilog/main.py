"""
CLI de smalilog.

Subcomandos:
    smalilog server [opciones]    Arranca el servidor de logs.
    smalilog hook   <cmd> [...]   Inyecta hooks en un archivo Smali.

Ejemplos:
    smalilog
    smalilog server
    smalilog server --host 0.0.0.0 -p 8080
    smalilog hook list       app.smali
    smalilog hook enter      app.smali -m Sf
    smalilog hook lifecycle  Application.smali -m onCreate
"""

from __future__ import annotations

import argparse
import logging
import sys
import time

from . import config
from .injector.hooker import run_hooker
from .server import LogServer

# --------------------------------------------------------------------------- #
#  Constantes
# --------------------------------------------------------------------------- #
EXIT_OK = 0
EXIT_ERROR = 1
EXIT_USAGE = 2

LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

# --------------------------------------------------------------------------- #
#  Colores ANSI (fallback mínimo si el usuario tiene NO_COLOR)
# --------------------------------------------------------------------------- #
import os
_USE_COLOR = sys.stdout.isatty() and not os.environ.get("NO_COLOR")

def _c(code: str, s: str) -> str:
    return f"{code}{s}\033[0m" if _USE_COLOR else s

_BOLD   = "\033[1m"
_CYAN   = "\033[96m"
_GREEN  = "\033[92m"
_YELLOW = "\033[93m"
_DIM    = "\033[2m"


# --------------------------------------------------------------------------- #
#  Menú de subcomandos estilo git
# --------------------------------------------------------------------------- #
# (nombre, resumen, args típicos, es_hook)
_COMMANDS = [
    ("server",     "Arranca el servidor HTTP que recibe los logs.",
     "smalilog server [--host H] [-p PORT]", False),

    # --- hook: subcomandos ---
    ("hook list",       "Lista los métodos del archivo Smali.",
     "smalilog hook list <file>", True),
    ("hook show",       "Muestra el código smali de un método.",
     "smalilog hook show <file> -m <m> [--all]", True),
    ("hook analyze",    "Analiza registros y plan de inyección.",
     "smalilog hook analyze <file> -m <m> [--sig S]", True),
    ("hook enter",      "Inyecta hook de entrada.",
     "smalilog hook enter <file> -m <m>", True),
    ("hook exit",       "Inyecta hook de salida.",
     "smalilog hook exit <file> -m <m>", True),
    ("hook both",       "Inyecta enter + exit.",
     "smalilog hook both <file> -m <m>", True),
    ("hook log",        "Inyecta un log tag/mensaje.",
     'smalilog hook log <file> -m <m> --tag T --message MSG', True),
    ("hook lifecycle",  "LifecycleTracker en Application.onCreate.",
     "smalilog hook lifecycle <file> -m onCreate", True),
]


def _print_main_help() -> None:
    """Ayuda principal con subcomandos agrupados al estilo git."""
    prog = "smalilog"
    print()
    print(_c(_BOLD, f"Uso: {prog} <comando> [opciones]"))
    print(_c(_BOLD, f"     {prog} --version"))
    print(_c(_BOLD, f"     {prog} -h | --help"))
    print()
    print("Herramienta para instrumentar aplicaciones Android con log remoto")
    print("vía Smali + JNI + servidor HTTP.")
    print()
    print(_c(_BOLD, "Comandos:"))

    # Ancho para alinear la segunda columna
    width = max(len(name) for name, *_ in _COMMANDS) + 2

    for name, summary, _example, is_hook in _COMMANDS:
        if is_hook:
            label = "  " + _c(_DIM, "└─ ") + _c(_GREEN, name)
        else:
            label = _c(_CYAN, name)
        pad = " " * (width - len(name))
        print(f"  {label}{pad}{summary}")

    print()
    print(_c(_BOLD, "Opciones globales:"))
    print(f"  {_c(_CYAN, '-h, --help'):<28} Muestra esta ayuda.")
    print(f"  {_c(_CYAN, '--version'):<28} Muestra la versión.")
    print()
    print(_c(_BOLD, "Ejemplos:"))
    for name, _s, example, _h in _COMMANDS:
        print(f"  {_c(_DIM, '$')} {example}")
    print()
    print(_c(_DIM, "Usa 'smalilog hook <cmd> -h' para ver opciones de un subcomando."))
    print()


# --------------------------------------------------------------------------- #
#  Tipos validadores de argparse
# --------------------------------------------------------------------------- #
def _port_type(value: str) -> int:
    try:
        port = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"puerto inválido: {value!r}") from None
    if not 0 <= port <= 65535:
        raise argparse.ArgumentTypeError(
            f"el puerto debe estar entre 0 y 65535 (recibido: {port})")
    return port


def _positive_int(value: str) -> int:
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"entero inválido: {value!r}") from None
    if number <= 0:
        raise argparse.ArgumentTypeError(
            f"debe ser un entero > 0 (recibido: {number})")
    return number


def _log_level_type(value: str) -> str:
    level = value.upper()
    if level not in LOG_LEVELS:
        raise argparse.ArgumentTypeError(
            f"nivel inválido: {value!r} "
            f"(opciones: {', '.join(sorted(LOG_LEVELS))})")
    return level


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
    p.add_argument("-p", "--port", type=_port_type, default=config.DEFAULT_PORT,
                   metavar="PUERTO",
                   help="Puerto TCP 0-65535 (por defecto: %(default)s).")
    p.add_argument("-f", "--log-file", default=config.DEFAULT_LOG_FILE,
                   metavar="ARCHIVO",
                   help="Archivo de logs (por defecto: %(default)s).")
    p.add_argument("-l", "--log-level", type=_log_level_type,
                   default=str(config.DEFAULT_LOG_LEVEL).upper(),
                   choices=sorted(LOG_LEVELS),
                   help="Nivel mínimo de log (por defecto: %(default)s).")
    p.add_argument("--max-headers", type=_positive_int, default=config.MAX_HEADERS,
                   metavar="BYTES",
                   help="Tamaño máximo de cabeceras HTTP (por defecto: %(default)s).")
    p.add_argument("--max-body", type=_positive_int, default=config.MAX_BODY,
                   metavar="BYTES",
                   help="Tamaño máximo del cuerpo HTTP (por defecto: %(default)s).")
    p.add_argument("--no-blocking", action="store_true",
                   help="Arranca en un hilo aparte.")
    p.add_argument("-v", "--verbose", action="store_true",
                   help="Muestra la configuración antes de arrancar.")


# --------------------------------------------------------------------------- #
#  Parser principal (solo server; hook se delega)
# --------------------------------------------------------------------------- #
def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="smalilog",
        description=(
            "Herramienta para instrumentar aplicaciones Android con log "
            "remoto vía Smali + JNI + servidor HTTP.\n"
            "\n"
            "subcomandos:\n"
            "  server    Arranca el servidor HTTP que recibe los logs.\n"
            "  hook      Inyecta hooks de logging en archivos Smali\n"
            "            (ver ayuda con: smalilog hook -h)"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Ejemplos:\n"
            "  smalilog server\n"
            "  smalilog server --host 0.0.0.0 -p 8080\n"
            "  smalilog hook list app.smali\n"
            "  smalilog hook enter app.smali -m Sf\n"
            "  smalilog hook lifecycle Application.smali -m onCreate\n"
        ),
    )
    parser.add_argument("--version", action="version",
                        version=f"%(prog)s {config.VERSION}")

    subparsers = parser.add_subparsers(dest="command", metavar="<comando>")
    _add_server_parser(subparsers)
    return parser


# --------------------------------------------------------------------------- #
#  Espera del servidor en segundo plano
# --------------------------------------------------------------------------- #
def _wait_background_server(server: LogServer) -> None:
    print("Servidor en segundo plano. Presiona Ctrl+C para detenerlo...",
          file=sys.stderr)
    thread = getattr(server, "_thread", None)
    try:
        while True:
            if getattr(server, "is_running", True) is False:
                break
            if thread is not None and not thread.is_alive():
                break
            if thread is not None:
                thread.join(timeout=0.5)
            else:
                time.sleep(0.5)
    except KeyboardInterrupt:
        pass


# --------------------------------------------------------------------------- #
#  Handler: server
# --------------------------------------------------------------------------- #
def _cmd_server(args: argparse.Namespace) -> int:
    log_level = LOG_LEVELS.get(str(args.log_level).upper())
    if log_level is None:
        print(f"Nivel de log desconocido: {args.log_level!r}", file=sys.stderr)
        return EXIT_USAGE

    if args.verbose:
        print(f"Host        : {args.host}")
        print(f"Puerto      : {args.port}")
        print(f"Log file    : {args.log_file}")
        print(f"Log level   : {args.log_level}")
        print(f"Max headers : {args.max_headers} bytes")
        print(f"Max body    : {args.max_body} bytes")
        print(f"Modo        : "
              f"{'hilo aparte' if args.no_blocking else 'bloqueante'}")

    common = {
        "host": args.host,
        "port": args.port,
        "log_file": args.log_file,
        "log_level": log_level,
    }
    try:
        server = LogServer(max_headers=args.max_headers,
                           max_body=args.max_body, **common)
    except TypeError:
        server = LogServer(**common)
        server.MAX_HEADERS = args.max_headers
        server.MAX_BODY = args.max_body

    try:
        server.start(blocking=not args.no_blocking)
        if args.no_blocking:
            _wait_background_server(server)
    except KeyboardInterrupt:
        print("\nInterrupción recibida, cerrando...", file=sys.stderr)
    except OSError as exc:
        print(f"Error al iniciar el servidor: {exc}", file=sys.stderr)
        return EXIT_ERROR
    finally:
        try:
            server.stop()
        except Exception as exc:
            print(f"Aviso: no se pudo detener limpiamente: {exc}",
                  file=sys.stderr)
    return EXIT_OK


# --------------------------------------------------------------------------- #
#  Entry point
# --------------------------------------------------------------------------- #
def cli(argv: list[str] | None = None) -> int:
    """
    Punto de entrada del CLI.

    - `hook` se delega al hooker con su propio parser.
    - Sin subcomando → menú principal (bonito).
    - Devuelve un código de salida; nunca lanza SystemExit.
    """
    if argv is None:
        argv = sys.argv[1:]
    else:
        argv = list(argv)

    # Delegar `hook` completo (con su subparser interno y su propia ayuda).
    if argv and argv[0] == "hook":
        return run_hooker(argv[1:] or ["--help"], prog="smalilog hook")

    # Sin argumentos → menú bonito
    if not argv:
        _print_main_help()
        return EXIT_OK

    # -h/--help a secas → menú bonito también (en vez del argparse feo)
    if argv in (["-h"], ["--help"]):
        _print_main_help()
        return EXIT_OK

    parser = _build_parser()

    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        code = exc.code
        return code if isinstance(code, int) else EXIT_OK

    if args.command == "server":
        return _cmd_server(args)

    parser.print_help()
    return EXIT_USAGE


# Alias retro-compatible
main = cli


if __name__ == "__main__":
    sys.exit(cli())
