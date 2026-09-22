"""
smalilog.injector.hooker
Inyecta hooks de observación en archivos Smali.

API programática:
    from smalilog.injector.hooker import run_hooker
    run_hooker(["archivo.smali", "--method", "Sf", "--action", "both"])

Fachada pública: reexporta los símbolos más usados para compatibilidad.
La implementación vive en los submódulos `_*.py`.
"""
from __future__ import annotations

import sys

from smalilog.smali import analyze_method
from ._cli import build_hook_parser, run_hooker
from smalilog.smali  import generate_d_log, generate_hook_enter, generate_hook_exit
from smalilog.ui import Color
from ._injector import HookInjector
from ._register_planner import plan_hook_registers
from smalilog.smali import (
    SmaliMethod,
    count_parameter_registers,
    normalize_reg,
    param_register_offsets,
)
from smalilog.smali import parse_class_name, parse_smali_file
from smalilog.smali import (
    parse_type_list,
)

REMOTE_LOGGER_CLASS = "Lcom/deadnote/RemoteLogger;"


__all__ = [
    "REMOTE_LOGGER_CLASS",
    "Color",
    "HookInjector",
    "SmaliMethod",
    "analyze_method",
    "build_hook_parser",
    "count_parameter_registers",
    "generate_d_log",
    "generate_hook_enter",
    "generate_hook_exit",
    "normalize_reg",
    "param_register_offsets",
    "parse_class_name",
    "parse_smali_file",
    "parse_type_list",
    "plan_hook_registers",
    "run_hooker",
    # "show_method_source",
]


if __name__ == "__main__":
    sys.exit(run_hooker())
