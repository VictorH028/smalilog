"""CLI del puente Renef → Smali."""
from __future__ import annotations

import argparse
from pathlib import Path

from smalilog.ui import _c, Color, log_error, log_header, log_info

from ._apply import (
    DEFAULT_LOGGER_CLASS,
    DEFAULT_TAG,
    apply_report,
    print_summary,
)
from ._recipe import parse_script
from ._agent_cli import add_agent_subparsers, run_agent_command

PRESETS_DIR = Path(__file__).resolve().parent / "presets"
PRESETS = {
    "ssl": ("ssl_unpin.lua", "Anula pinning SSL en TrustManagers/OkHttp/WebView"),
    "root": ("root_bypass.lua", "Evita comprobaciones Java de root (RootBeer)"),
}


def _add_source(p: argparse.ArgumentParser) -> None:
    p.add_argument("script", nargs="?",
                   help="Script Lua de Renef a analizar")
    p.add_argument("--preset", choices=sorted(PRESETS),
                   help="Usa un preset incluido en smalilog")


def _add_apply_options(p: argparse.ArgumentParser) -> None:
    p.add_argument("--smali-dir", required=True, metavar="RUTA",
                   help="Raíz del APK descompilado (contiene smali*/) "
                        "o un archivo .smali")
    p.add_argument("--logger-class", default=DEFAULT_LOGGER_CLASS,
                   metavar="DESCRIPTOR",
                   help="Clase del logger Smali (por defecto: %(default)s)")
    p.add_argument("--tag", default=DEFAULT_TAG,
                   help="Tag usado en los logs de observación "
                        "(por defecto: %(default)s)")
    p.add_argument("--only", metavar="CLASE#MÉTODO",
                   help="Aplica solo las recetas que contengan este texto")
    p.add_argument("--dry-run", action="store_true",
                   help="No escribe archivos; solo muestra qué haría")
    p.add_argument("--no-backup", action="store_true",
                   help="No crear archivos .smali.bak")


def build_renef_parser(prog: str = "smalilog renef") -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=prog,
        description=(
            "Puente estático entre los scripts Lua de Renef y Smali.\n"
            "Traduce hooks Java (skip/return constante) y observación a\n"
            "instrumentación Smali que no requiere root."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Ejemplos:
  smalilog renef presets
  smalilog renef parse --preset ssl
  smalilog renef parse mi_hook.lua
  smalilog renef apply --preset ssl --smali-dir ./apk --dry-run
  smalilog renef apply mi_hook.lua --smali-dir ./apk/smali
  smalilog renef apply --preset root --smali-dir ./apk --only RootBeer
  smalilog renef install ./apk --build
  smalilog renef runtime exec hook.lua --apk-dir ./apk
  smalilog renef runtime status --package com.demo

`apply` traduce hooks Java a Smali sin root. `install` y `runtime` usan el
agente dinámico Renef embebido en la APK y se controlan por broadcast,
también sin root.
""",
    )
    sub = parser.add_subparsers(dest="cmd", metavar="<cmd>", required=True)

    p = sub.add_parser("parse", help="Analiza un script y muestra las recetas")
    _add_source(p)

    p = sub.add_parser("apply", help="Aplica las recetas sobre un árbol Smali")
    _add_source(p)
    _add_apply_options(p)

    p = sub.add_parser("presets", help="Lista los presets incluidos")
    p.add_argument("--show", metavar="NOMBRE",
                   help="Muestra la ruta y el contenido de un preset")

    add_agent_subparsers(sub)
    return parser


def _resolve_source(args: argparse.Namespace) -> Path:
    if bool(args.script) == bool(args.preset):
        raise SystemExit(
            "error: indica un script .lua o --preset (no ambos)")
    if args.preset:
        filename, _desc = PRESETS[args.preset]
        return PRESETS_DIR / filename
    return Path(args.script)


def _print_presets() -> int:
    log_header("Presets Renef incluidos")
    for name, (filename, desc) in sorted(PRESETS.items()):
        path = PRESETS_DIR / filename
        print(f"  {_c(Color.GREEN, name):<8} {desc}")
        print(f"           {_c(Color.DIM, str(path))}")
    print()
    log_info("Úsalos con: smalilog renef apply --preset <nombre> "
             "--smali-dir <ruta>")
    return 0


def _print_report(report) -> int:
    log_header(f"Recetas en {report.path}")
    for recipe in report.recipes:
        color = Color.GREEN if recipe.applicable else Color.YELLOW
        print(f"  {_c(color, f'[{recipe.action.value}]'):<14} "
              f"{recipe.target}")
        if recipe.reason:
            print(f"               {_c(Color.DIM, recipe.reason)}")

    if not report.recipes:
        log_error("No se encontraron llamadas a hook/safe_hook")

    if report.runtime_features:
        print()
        log_info("APIs de runtime detectadas (no traducibles sin root/agente):")
        for feature in report.runtime_features:
            print(f"    - {feature}")

    print()
    log_info(f"Total: {len(report.recipes)} · "
             f"aplicables: {len(report.applicable)}")
    return 0 if report.recipes else 1


def _cmd_parse(args: argparse.Namespace) -> int:
    path = _resolve_source(args)
    if not path.exists():
        log_error(f"Script no encontrado: {path}")
        return 1
    source = path.read_text(encoding="utf-8", errors="ignore")
    return _print_report(parse_script(source, path))


def _cmd_apply(args: argparse.Namespace) -> int:
    path = _resolve_source(args)
    if not path.exists():
        log_error(f"Script no encontrado: {path}")
        return 1

    source = path.read_text(encoding="utf-8", errors="ignore")
    report = parse_script(source, path)
    if not report.recipes:
        log_error("No se encontraron llamadas a hook/safe_hook")
        return 1

    log_header(f"Aplicando {path.name} en {args.smali_dir}")
    result = apply_report(
        report,
        args.smali_dir,
        logger_class=args.logger_class,
        tag=args.tag,
        dry_run=args.dry_run,
        backup=not args.no_backup,
        only=args.only,
    )
    print_summary(report, result)
    return 0 if result.ok else 1


def _cmd_presets(args: argparse.Namespace) -> int:
    if args.show:
        if args.show not in PRESETS:
            log_error(f"Preset desconocido: {args.show}")
            return 1
        filename, _desc = PRESETS[args.show]
        path = PRESETS_DIR / filename
        print(path)
        print()
        print(path.read_text(encoding="utf-8"))
        return 0
    return _print_presets()


def run_renef(argv: list[str] | None = None,
              prog: str = "smalilog renef") -> int:
    """Punto de entrada del subcomando ``smalilog renef``."""
    parser = build_renef_parser(prog=prog)
    args = parser.parse_args(argv)

    if args.cmd == "parse":
        return _cmd_parse(args)
    if args.cmd == "apply":
        return _cmd_apply(args)
    if args.cmd == "presets":
        return _cmd_presets(args)
    if args.cmd in {"install", "runtime"}:
        return run_agent_command(args)

    parser.error(f"subcomando desconocido: {args.cmd}")
    return 2
