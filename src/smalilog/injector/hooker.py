"""Fachada de compatibilidad para la API histórica del inyector.

La implementación real está separada en ``_cli`` e ``_injector``; este
módulo conserva imports antiguos sin duplicar lógica.
"""
from __future__ import annotations

import sys

from smalilog.smali import (
    SmaliMethod,
    analyze_method,
    count_parameter_registers,
    generate_d_log,
    generate_hook_enter,
    generate_hook_exit,
    normalize_reg,
    param_register_offsets,
    parse_class_name,
    parse_smali_file,
    parse_type_list,
    plan_hook_registers,
)
from smalilog.ui import Color
from ._cli import build_hook_parser, run_hooker
from ._injector import HookInjector

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
]

if __name__ == "__main__":
    raise SystemExit(run_hooker())
