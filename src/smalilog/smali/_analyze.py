"""Análisis descriptivo de métodos Smali."""
from __future__ import annotations

from copy import copy

from smalilog.ui._colors import Color, _c, log_header
from ._register_planner import plan_hook_registers
from ._model import (
    SmaliMethod,
    count_parameter_registers,
    param_register_offsets,
)
from ._types import is_reference


def _enter_need(method: SmaliMethod) -> int:
    """Temps que necesitará inject_enter (2 si el primer arg es referencia, 3 si no)."""
    if not method.parameters:
        return 3
    return 2 if is_reference(method.parameters[0]) else 3


def analyze_method(method: SmaliMethod, class_name: str | None = None,
                   lines: list[str] | None = None) -> None:
    log_header(f"Método: {method.name}"
               + ("" if method.has_body else "  (SIN CUERPO)"))
    print(f"  {_c(Color.CYAN, 'Clase:')}     {class_name or '?'}")
    print(f"  {_c(Color.CYAN, 'Signature:')} {method.signature}")
    print(f"  {_c(Color.CYAN, 'Access:')}    {method.access}")
    print(f"  {_c(Color.CYAN, 'Directiva:')} "
          f".{method.directive} {method.registers_value}"
          + (f"  (total real: {method.total_regs})"
             if method.directive == "locals" else ""))

    n = count_parameter_registers(method)
    base = method.total_regs - n
    print(f"  {_c(Color.CYAN, 'Params:')}     {n} regs "
          f"(v{base}..v{method.total_regs - 1})")

    # ---- hooks ya presentes ----
    if lines is not None:
        body = lines[method.start_line:method.end_line + 1]
        hooks = [
            ("ENTER", any("Hook ENTER inyectado" in l for l in body)),
            ("EXIT",  any("Hook EXIT inyectado" in l for l in body)),
            ("D",     any("Log D inyectado" in l for l in body)),
        ]
        present = [name for name, ok in hooks if ok]
        if present:
            print(f"  {_c(Color.YELLOW, '⚠ Hooks presentes:')} "
                  f"{', '.join(present)}")
            print(f"  {_c(Color.DIM, 'El plan de abajo asume un método limpio.')}")

    all_params = []
    if "static" not in method.access:
        all_params.append(class_name or "this")
    all_params.extend(method.parameters)

    if all_params:
        print(f"  {_c(Color.CYAN, 'Mapeo p → v:')} (respeta anchos wide)")
        for (i, start, size), p in zip(param_register_offsets(method), all_params):
            span = f"v{start}" if size == 1 else f"v{start}-v{start + 1}"
            print(f"    p{i} → {span:<11} {p}")

    # ---- planes de inyección ----
    enter_need = _enter_need(method)
    exit_need = 2

    plan_e = plan_hook_registers(method, need=enter_need)
    plan_x = plan_hook_registers(method, need=exit_need)

    print(f"  {_c(Color.CYAN, 'Plan (enter):')} expandir a "
          f".registers {plan_e['new_total_regs']}, "
          f"temps frescos {plan_e['temps']}")
    print(f"  {_c(Color.CYAN, 'Plan (exit):')}  expandir a "
          f".registers {plan_x['new_total_regs']}, "
          f"temps frescos {plan_x['temps']}")

    # ---- mapeo tras expandir (usamos el plan de enter como referencia) ----
    if all_params:
        print(f"  {_c(Color.CYAN, 'Mapeo tras expandir:')}")
        m2 = copy(method)
        if method.directive == "locals":
            m2.registers_value = method.registers_value + plan_e["needed"]
        else:
            m2.registers_value = plan_e["new_total_regs"]
        for (i, start, size), p in zip(param_register_offsets(m2), all_params):
            span = f"v{start}" if size == 1 else f"v{start}-v{start + 1}"
            print(f"    p{i} → {span:<11} {p}")
    print()

