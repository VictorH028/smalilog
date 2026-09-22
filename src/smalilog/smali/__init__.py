"""Modelo, parser y codegen de Smali."""
from __future__ import annotations

from ._codegen import generate_d_log, generate_hook_enter, generate_hook_exit
from ._model import (
    SmaliMethod,
    count_parameter_registers,
    normalize_reg,
    param_register_offsets,
)
from ._parser import parse_class_name, parse_smali_file
from ._types import is_reference, parse_type_list, params_raw, return_raw
from ._analyze import analyze_method 

__all__ = [
    "SmaliMethod",
    "analyze_method",
    "count_parameter_registers",
    "normalize_reg",
    "param_register_offsets",
    "parse_class_name",
    "parse_smali_file",
    "generate_hook_enter",
    "generate_hook_exit",
    "generate_d_log",
    "is_reference",
    "parse_type_list",
    "params_raw",
    "return_raw",
]
