"""
CLI de smalilog.

Subcomandos:
    smalilog server [opciones]    Arranca el servidor de logs.
    smalilog hook   [opciones]    Inyecta hooks en un archivo Smali.

Si no se especifica subcomando, se muestra la ayuda principal.

Ejemplos:
    smalilog
    smalilog server                          # valores por defecto
    smalilog server --host 0.0.0.0 -p 8080
    smalilog hook archivo.smali --list
    smalilog hook archivo.smali -m Sf -a both
    smalilog hook archivo.smali -m Sf -a d --tag APP --message "hola"
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
EXIT_OK = 0       # éxito
EXIT_ERROR = 1    # fallo de ejecución
EXIT_USAGE = 2    # uso incorrecto (convención de argparse)

LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


# --------------------------------------------------------------------------- #
#  Tipos validadores de argparse
# --------------------------------------------------------------------------- #
def _port_type(value: str) -> int:
    """FIX (6): antes se aceptaban puertos como -1 o 99999 sin avisar."""
    try:
        port = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"puerto inválido: {value!r}") from None
    if not 0 <= port <= 65535:
        raise argparse.ArgumentTypeError(
            f"el puerto debe estar entre 0 y 65535 (recibido: {port})")
    return port


def _positive_int(value: str) -> int:
    """FIX (6): límites de tamaño <= 0 rompían el servidor en silencio."""
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"entero inválido: {value!r}") from None
    if number <= 0:
        raise argparse.ArgumentTypeError(
            f"debe ser un entero > 0 (recibido: {number})")
    return number


def _log_level_type(value: str) -> str:
    """
    Normaliza a mayúsculas y valida el nivel de log.

    FIX (5): argparse NO aplica `type` (ni comprueba `choices`) sobre el
    `default`; si config.DEFAULT_LOG_LEVEL fuese "info", el handler
    original moría con KeyError. Esta función garantiza la forma
    normalizada; `_cmd_server` además normaliza el default de forma
    defensiva.
    """
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
#  Parser principal
# --------------------------------------------------------------------------- #
def _build_parser() -> argparse.ArgumentParser:
    """
    FIX (2): `hook` ya no se registra vía `subparsers._name_parser_map`
    (API privada: no aparecía en `--help` y causaba parseo doble). Ahora
    se despacha manualmente en `cli()` y solo se anuncia aquí.
    """
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
            "  smalilog hook archivo.smali --list\n"
            "  smalilog hook archivo.smali -m Sf -a both\n"
            "  smalilog hook archivo.smali -m Sf -a d --tag APP --message 'hola'\n"
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
    """
    Espera mientras el servidor corre en su hilo.

    FIX (3): sin `assert` ni acceso directo a `_thread`.
    FIX (4): se comprueba `is_alive()` para no colgarse si el hilo murió.
    """
    print("Servidor en segundo plano. Presiona Ctrl+C para detenerlo...",
          file=sys.stderr)

    # `_thread` es API privada de LogServer: acceder con getattr por si
    # cambia de nombre o no existe.
    thread = getattr(server, "_thread", None)
    try:
        while True:
            # Sin `is_running` se asume vivo (default=True) para no salir antes.
            if getattr(server, "is_running", True) is False:
                break
            # Hilo muerto (excepción interna incluida): no esperar eternamente.
            if thread is not None and not thread.is_alive():
                break
            # `join(timeout=...)` en vez de `join()` a secas: en Windows un
            # join bloqueante impide que llegue Ctrl+C de forma fiable.
            if thread is not None:
                thread.join(timeout=0.5)
            else:
                time.sleep(0.5)
    except KeyboardInterrupt:
        pass  # el `finally` de `_cmd_server` detiene el servidor


# --------------------------------------------------------------------------- #
#  Handler: server
# --------------------------------------------------------------------------- #
def _cmd_server(args: argparse.Namespace) -> int:
    # FIX (5): normalización defensiva; el `default` no pasa por `type`.
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
        # FIX (7): pasar los límites por constructor para que se apliquen
        # desde el inicio; asignarlos como atributos después se ignora en
        # silencio si LogServer los lee en __init__.
        server = LogServer(max_headers=args.max_headers,
                           max_body=args.max_body, **common)
    except TypeError:
        # Compatibilidad con versiones antiguas de LogServer.
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
        # FIX (9): un fallo al detener no debe enmascarar la salida real.
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
    Punto de entrada del CLI (usado por el entry point `smalilog`).

    - `hook` se despacha antes que argparse (tiene su propio parser en
      el módulo hooker; así no se duplican opciones ni se reparsea).
    - Sin subcomando, se muestra la ayuda principal.
    - Devuelve un código de salida; nunca lanza SystemExit.

    FIX (1): `smalilog server` ahora sí arranca con los valores por defecto.
    FIX (8): argparse ya no escapa como SystemExit; se devuelven códigos
             consistentes (0 ok, 1 error, 2 uso incorrecto).
    """
    if argv is None:
        argv = sys.argv[1:]
    else:
        argv = list(argv)

    # Delegar `hook` completo al hooker (con su propia ayuda y validación).
    if argv and argv[0] == "hook":
        return run_hooker(argv[1:] or ["--help"], prog="smalilog hook")

    parser = _build_parser()

    if not argv:
        parser.print_help()
        return EXIT_OK

    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        # argparse usa SystemExit(0) para --help/--version y (2) para
        # errores de uso; se convierte al contrato `-> int` de `cli`.
        code = exc.code
        return code if isinstance(code, int) else EXIT_OK

    if args.command == "server":
        return _cmd_server(args)

    # Solo alcanzable si algún día se añade un subcomando sin handler.
    parser.print_help()
    return EXIT_USAGE


# Alias retro-compatible
main = cli


if __name__ == "__main__":
    sys.exit(cli())
