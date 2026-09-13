#!/usr/bin/env python3
"""
CLI de smalilog.

Ejemplos:
    smalilog                          # arranca con valores por defecto
    smalilog --host 0.0.0.0 -p 8080   # escucha en todas las interfaces
    smalilog -l DEBUG -v              # nivel DEBUG y modo verboso
    smalilog --no-blocking            # arranca en segundo plano
    smalilog --version
"""

from __future__ import annotations

import argparse
import logging
import sys

from . import config
from .server import LogServer


LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="smalilog",
        description=(
            "Comando principal que se encarga de (hook,analisis,server)"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--host",
        default=config.DEFAULT_HOST,
        help="Dirección IP o hostname donde escuchar (por defecto: %(default)s).",
    )
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=config.DEFAULT_PORT,
        help="Puerto TCP donde escuchar (por defecto: %(default)s).",
    )
    parser.add_argument(
        "-f", "--log-file",
        default=config.DEFAULT_LOG_FILE,
        help="Archivo donde se guardan los logs (por defecto: %(default)s).",
    )
    parser.add_argument(
        "-l", "--log-level",
        default=config.DEFAULT_LOG_LEVEL,
        choices=sorted(LOG_LEVELS.keys()),
        type=str.upper,
        help="Nivel mínimo de log a registrar (por defecto: %(default)s).",
    )
    parser.add_argument(
        "--max-headers",
        type=int,
        default=config.MAX_HEADERS,
        help="Tamaño máximo de cabeceras HTTP en bytes (por defecto: %(default)s).",
    )
    parser.add_argument(
        "--max-body",
        type=int,
        default=config.MAX_BODY,
        help="Tamaño máximo del cuerpo HTTP en bytes (por defecto: %(default)s).",
    )
    parser.add_argument(
        "--no-blocking",
        action="store_true",
        help="Arranca el servidor en un hilo aparte (no bloquea la consola).",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Muestra información adicional por consola.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {config.VERSION}",
    )

    return parser


def cli(argv: list[str] | None = None) -> int:
    """Punto de entrada del CLI (usado por el entry point `smalilog`)."""
    parser = _build_parser()
    args = parser.parse_args(argv)

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
    # Overrides del protocolo HTTP
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


# Alias retro-compatible por si algo importa `main` en lugar de `cli`
main = cli


if __name__ == "__main__":
    sys.exit(cli())
