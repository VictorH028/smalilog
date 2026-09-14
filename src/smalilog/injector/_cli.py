"""CLI del inyector de hooks."""
from __future__ import annotations

import argparse
import sys

from ._analyze import analyze_method
from ._colors import Color, _c, log_error, log_header, log_info, log_ok, log_warn
from ._injector import HookInjector


def build_hook_parser(prog: str = "smalilog hook",
                      remote_logger_class: str = "Lcom/deadnote/RemoteLogger;"
                      ) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=prog,
        description="Inyecta hooks de observación en archivos Smali",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  smalilog hook archivo.smali --list
  smalilog hook archivo.smali --method Sf --analyze
  smalilog hook archivo.smali --method Sf --action show
  smalilog hook archivo.smali --all
  smalilog hook archivo.smali --method Sf --action enter
  smalilog hook archivo.smali --method Sf --action both
  smalilog hook archivo.smali --method Sf --action d --tag MiTag --message "Hola"
  smalilog hook archivo.smali --method Sf --signature "(I)V" --action both
        """,
    )
    parser.add_argument("file", nargs="?", help="Archivo Smali a procesar")
    parser.add_argument("--method", "-m", help="Nombre del método objetivo")
    parser.add_argument("--signature",
                        help="Subcadena de firma para desambiguar sobrecargas")
    parser.add_argument("--action", "-a",
                        choices=["enter", "exit", "both", "observ",
                                 "analyze", "d", "show"],
                        help="Acción ")
    parser.add_argument("--tag", default="LOG", help='Tag para acción "d"')
    parser.add_argument("--message", "--msg", default="Mensaje de log",
                        help='Mensaje para acción "d"')
    parser.add_argument("--analyze", action="store_true", help="Solo analizar")
    parser.add_argument("--list", "-l", action="store_true",
                        help="Listar métodos")
    parser.add_argument("--all", action="store_true",
                        help='Con "show": mostrar todos los métodos '
                             "(implica --action show)")
    parser.add_argument("--no-color", action="store_true",
                        help="Desactivar resaltado de sintaxis")
    parser.add_argument("--style", default="default",
                        help='Estilo Pygments (p.ej. "monokai")')
    parser.add_argument("--no-backup", action="store_true",
                        help="No crear backup")
    parser.add_argument("--output", "-o", help="Archivo de salida")
    return parser


def show_method_source(file_path, method_name, signature=None,
                       remote_logger_class="Lcom/deadnote/RemoteLogger;",
                       **kwargs) -> bool:
    """Ver el código completo de un método con resaltado de sintaxis."""
    inj = HookInjector(file_path, remote_logger_class)
    if not inj.load():
        return False
    if not inj.resolve_method(method_name, signature):
        return False
    return inj.show_method(**kwargs)


def run_hooker(argv: list[str] | None = None,
               prog: str = "smalilog hook",
               remote_logger_class: str = "Lcom/deadnote/RemoteLogger;"
               ) -> int:
    parser = build_hook_parser(prog=prog,
                               remote_logger_class=remote_logger_class)
    args = parser.parse_args(argv)

    if not args.file:
        parser.error("se requiere la ruta del archivo .smali")

    log_header("smalilog hook - Inyector de hooks")

    injector = HookInjector(args.file, remote_logger_class)
    if not injector.load():
        return 1

    if args.list:
        log_header(f"Métodos en {args.file}")
        for m in injector.methods:
            flags = []
            if m.is_static():
                flags.append("static")
            if not m.has_body:
                flags.append("sin cuerpo")
            extra = f" [{' '.join(flags)}]" if flags else ""
            print(f"  {_c(Color.GREEN, m.name)}{m.signature} "
                  f"({m.total_regs} regs){extra}")
        return 0

    if args.action is None and not (args.list or args.analyze or args.all):
        log_error("Debes especificar --action (o --list/--analyze/--all/--show)")
        return 1

    if args.analyze or args.action == "analyze":
        if not args.method:
            log_error("--analyze requiere --method")
            return 1
        if not injector.resolve_method(args.method, args.signature):
            return 1
        analyze_method(injector.target, injector.class_name)
        return 0

    if args.all and args.action != "show":
        args.action = "show"

    if args.action == "show":
        color = not args.no_color
        if args.all:
            shown = sum(
                1 for m in injector.methods
                if m.has_body and injector.show_method(method=m,
                                                       color=color,
                                                       style=args.style)
            )
            if not shown:
                log_warn("Ningún método con cuerpo que mostrar")
                return 1
            log_ok(f"{shown} método(s) mostrados")
            return 0
        if not args.method:
            log_error("--action show requiere --method (o --all)")
            return 1
        if not injector.resolve_method(args.method, args.signature):
            return 1
        injector.show_method(color=color, style=args.style)
        return 0

    if not args.method:
        log_error("Debes especificar --method (o usar --list / --analyze)")
        return 1
    if not injector.resolve_method(args.method, args.signature):
        return 1

    log_info(f"Archivo: {args.file}")
    log_info(f"Método:  {args.method}{injector.target.signature}")
    log_info(f"Acción:  {args.action}")
    analyze_method(injector.target, injector.class_name)

    if args.action == "d":
        success = injector.inject_d(args.tag, args.message)
    elif args.action == "enter":
        success = injector.inject_enter()
    elif args.action == "exit":
        success = injector.inject_exit()
    else:
        ok_enter = injector.inject_enter()
        ok_exit = injector.inject_exit()
        success = ok_enter and ok_exit
        if not success and (ok_enter or ok_exit):
            log_warn("Inyección parcial: revisa los mensajes anteriores")

    if not success:
        log_error("No se pudo completar la inyección")
        return 1

    injector.save(output=args.output, backup=not args.no_backup)
    log_header("INYECCIÓN COMPLETADA")
    return 0
