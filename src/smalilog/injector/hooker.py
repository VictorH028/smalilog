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

from ._analyze import analyze_method
from ._cli import build_hook_parser, run_hooker, show_method_source
from ._codegen import generate_d_log, generate_hook_enter, generate_hook_exit
from ._colors import Color, _c, log_error, log_header, log_info, log_ok, log_warn
from ._emit import box_scalar, const_null, indent, invoke_static, move_object
from ._injector import HookInjector
from ._register_planner import plan_hook_registers
from ._smali_model import (
    SmaliMethod,
    count_parameter_registers,
    normalize_reg,
    param_register_offsets,
)
from ._smali_parser import parse_class_name, parse_smali_file
from ._smali_types import (
    _type_size,
    is_reference,
    parse_type_list,
    params_raw,
    return_raw,
)

REMOTE_LOGGER_CLASS = "Lcom/deadnote/RemoteLogger;"

# Alias retro-compatibles (nombres privados originales)
_parse_method_line = None  # ver _smali_parser
_invoke_static = invoke_static
_move_object = move_object
_const_null = const_null
_box_scalar = box_scalar

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
    "show_method_source",
]


if __name__ == "__main__":
    sys.exit(run_hooker())
