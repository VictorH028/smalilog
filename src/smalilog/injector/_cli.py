"""CLI del inyector de hooks (subcomandos estilo git)."""
from __future__ import annotations

import argparse

from smalilog.smali import analyze_method
from smalilog.ui import Color, log_error, log_header, log_ok, log_warn, _c, log_info
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
    p.add_argument(
        "--logger-class", default="Lcom/deadnote/RemoteLog;",
        help="Descriptor Smali de la clase logger "
             "(por defecto: Lcom/deadnote/RemoteLog;)")



def build_hook_parser(prog: str = "smalilog hook") -> argparse.ArgumentParser:
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
  smalilog hook info       app.smali -m Sf --tag APP --message "hola"
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

    # enter / exit
    p = sub.add_parser("enter", help="Inyecta hook de entrada")
    _add_common(p)
    p = sub.add_parser("exit", help="Inyecta hook de salida")
    _add_common(p)

    # both / lifecycle
    for name, help_ in [
        ("both",      "Inyecta enter + exit"),
        ("lifecycle", "Inyecta LifecycleTracker en Application.onCreate"),
    ]:
        p = sub.add_parser(name, help=help_)
        _add_common(p)

    # Niveles d/i/w/e de RemoteLog.
    for lvl in ("debug", "info", "warn", "error"):
        p = sub.add_parser(lvl, help=f"Log nivel {lvl.upper()}")
        _add_common(p)
        p.add_argument("--tag", default="APP")
        p.add_argument("--message", "--msg", dest="message", default="")

    return parser


def run_hooker(argv: list[str] | None = None,
               prog: str = "smalilog hook",
               remote_logger_class: str = "Lcom/deadnote/RemoteLog;"
               ) -> int:
    parser = build_hook_parser(prog=prog)
    args = parser.parse_args(argv)

    logger_class = getattr(args, "logger_class", remote_logger_class)
    inj = HookInjector(args.file, logger_class)
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
    if inj.target is None:                          # narrowing para el checker
        log_error("Método no resuelto")
        return 1

    target = inj.target
    if args.cmd == "analyze":
        analyze_method(target, inj.class_name, lines=inj.lines)
        return 0

    log_info(f"Archivo: {args.file}")
    log_info(f"Método:  {args.method}{inj.target.signature}")
    if args.verbose:
        log_info(f"Clase: {inj.class_name} · regs: {target.total_regs} · "
                 f"params: {len(target.parameters)}")

    # ---- inyección ----
    ok = False
    if args.cmd == "enter":
        ok = inj.inject_enter()
    elif args.cmd == "exit":
        ok = inj.inject_exit()
    elif args.cmd == "both":
        ok = inj.inject_both()
    elif args.cmd in ("debug", "info", "warn", "error"):
        ok = inj.inject_log_level(args.cmd, args.tag, args.message)
    elif args.cmd == "lifecycle":
        ok = inj.inject_lifecycle_tracker()
    else:
        parser.error(f"subcomando desconocido: {args.cmd}")
        return 2

    if not ok:
        log_error("La inyección falló")
        return 1

    inj.save(output=args.output, backup=not args.no_backup)
    log_ok("Inyección completada")
    return 0

