"""CLI del inyector de hooks (subcomandos estilo git)."""
from __future__ import annotations

import argparse

from smalilog.smali import analyze_method
from smalilog.ui import Color, log_error, log_header, log_info, log_ok, log_warn
from ._injector import HookInjector


def _add_common(p: argparse.ArgumentParser) -> None:
    p.add_argument("file", help="Archivo Smali a procesar")
    p.add_argument("-m", "--method", help="Nombre del método objetivo")
    p.add_argument("--sig", "--signature", dest="signature",
                   help="Subcadena de firma para desambiguar sobrecargas")
    p.add_argument("--no-color", action="store_true",
                   help="Desactivar resaltado")
    p.add_argument("--style", default="default",
                   help='Estilo Pygments (p.ej. "monokai")')
    p.add_argument("--no-backup", action="store_true", help="No crear backup")
    p.add_argument("-o", "--output", help="Archivo de salida")
    p.add_argument("-v", "--verbose", action="store_true")


def build_hook_parser(prog: str = "smalilog hook",
                      remote_logger_class: str = "Lcom/deadnote/RemoteLogger;"
                      ) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=prog,
        description="Inyecta hooks de observación en archivos Smali.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Ejemplos:
  smalilog hook list       app.smali
  smalilog hook show       app.smali -m Sf
  smalilog hook analyze    app.smali -m Sf --sig "(I)V"
  smalilog hook enter      app.smali -m Sf
  smalilog hook exit       app.smali -m Sf
  smalilog hook both       app.smali -m Sf
  smalilog hook log        app.smali -m Sf --tag APP --message "hola"
  smalilog hook lifecycle  Application.smali -m onCreate
""",
    )
    sub = parser.add_subparsers(dest="cmd", metavar="<cmd>", required=True)

    # list
    p = sub.add_parser("list", help="Lista los métodos del archivo")
    p.add_argument("file")

    # show
    p = sub.add_parser("show", help="Muestra el código de un método")
    _add_common(p)
    p.add_argument("--all", action="store_true",
                   help="Muestra todos los métodos con cuerpo")

    # analyze
    p = sub.add_parser("analyze", help="Analiza registros y plan de inyección")
    _add_common(p)

    # enter / exit / both / lifecycle
    for name, help_ in [
        ("enter",     "Inyecta hook de entrada"),
        ("exit",      "Inyecta hook de salida"),
        ("both",      "Inyecta enter + exit"),
        ("lifecycle", "Inyecta LifecycleTracker en Application.onCreate"),
    ]:
        p = sub.add_parser(name, help=help_)
        _add_common(p)

    # log (antes "d")
    p = sub.add_parser("log", help="Inyecta un log simple tag/mensaje")
    _add_common(p)
    p.add_argument("--tag", default="LOG")
    p.add_argument("--message", "--msg", dest="message",
                   default="Mensaje de log")

    return parser


def run_hooker(argv: list[str] | None = None,
               prog: str = "smalilog hook",
               remote_logger_class: str = "Lcom/deadnote/RemoteLogger;"
               ) -> int:
    parser = build_hook_parser(prog=prog,
                               remote_logger_class=remote_logger_class)
    args = parser.parse_args(argv)

    inj = HookInjector(args.file, remote_logger_class)
    if not inj.load():
        return 1

    # ---- subcomandos que no inyectan ----
        
    if args.cmd == "list":
        log_header(f"Métodos en {args.file}")
        for m in inj.methods:
            flags = []
            if m.is_static():     flags.append("static")
            if not m.has_body:    flags.append("sin cuerpo")
            extra = f"  [{' '.join(flags)}]" if flags else ""
            print(f"  {_c(Color.GREEN, m.name)}{m.signature}  "
                  f"({m.total_regs} regs){extra}")
        return 0

    if args.cmd == "show":
        color = not args.no_color
        if args.all:
            shown = sum(1 for m in inj.methods
                        if m.has_body and inj.show_method(
                            method=m, color=color, style=args.style))
            if not shown:
                log_warn("Ningún método con cuerpo")
                return 1
            log_ok(f"{shown} método(s) mostrados")
            return 0
        if not args.method:
            log_error("show requiere -m <método> (o --all)")
            return 1
        if not inj.resolve_method(args.method, args.signature):
            return 1
        inj.show_method(color=color, style=args.style)
        return 0

    # ---- subcomandos que resuelven método ----

    if not args.method:
        log_error(f"{args.cmd} requiere -m <método>")
        return 1
    if not inj.resolve_method(args.method, args.signature):
        return 1
    if args.verbose:
        analyze_method(inj.target, inj.class_name)
    if args.cmd == "analyze":
        analyze_method(inj.target, inj.class_name)
        return 0

    log_info(f"Archivo: {args.file}")
    log_info(f"Método:  {args.method}{inj.target.signature}")

    # ---- inyección ----

    if args.cmd == "enter":
        ok = inj.inject_enter()
    elif args.cmd == "exit":
        ok = inj.inject_exit()
    elif args.cmd == "both":
        log_info("Por ahora no disponible...")
        # ok_e = inj.inject_enter()
        # ok_x = inj.inject_exit()
        # ok = ok_e and ok_x
        # if not ok and (ok_e or ok_x):
        #     log_warn("Inyección parcial")
        return 1
    elif args.cmd == "log":
        # ok = inj.inject_d(args.tag, args.message)
        log_info("Por ahora no disponible...")
        return 1
    elif args.cmd == "lifecycle":
        ok = inj.inject_lifecycle_tracker()
    else:
        parser.error(f"subcomando desconocido: {args.cmd}")
        return 2

    if not ok:
        log_error("No se pudo completar la inyección")
        return 1

    inj.save(output=args.output, backup=not args.no_backup)
    log_ok("Inyección completada")
    return 0
