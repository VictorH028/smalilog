"""Análisis descriptivo de métodos Smali."""
from __future__ import annotations

from smalilog.ui._colors import Color, _c, log_header
from smalilog.injector._register_planner import plan_hook_registers
from smalilog.smali._model import (
    SmaliMethod,
    count_parameter_registers,
    param_register_offsets,
)


def analyze_method(method: SmaliMethod, class_name: str | None = None) -> None:
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

   
    all_params = []
    if "static" not in method.access:
        all_params.append(class_name or "this")
    all_params.extend(method.parameters)

    if all_params:
        print(f"  {_c(Color.CYAN, 'Mapeo p → v:')} (respeta anchos wide)")
        for (i, start, size), p in zip(param_register_offsets(method), all_params):
            span = f"v{start}" if size == 1 else f"v{start}-v{start + 1}"
            print(f"    p{i} → {span:<11} {p}")
    
    plan = plan_hook_registers(method, need=3)
    new_total = plan["expand_to"]
    new_base = new_total - n

    print(f"  {_c(Color.CYAN, 'Plan:')}       expandir a "
          f".registers {new_total}, temps frescos {plan['temps']}")
    
    if all_params:
        print(f"  {_c(Color.CYAN, 'Mapeo tras expandir:')}")
        for (i, _, size), p in zip(param_register_offsets(method), all_params):
            # Recalcular posición tras expansión
            start = new_base + (i if method.is_static() else i) # El offset dinámico
            span = f"v{start}" if size == 1 else f"v{start}-v{start + 1}"
            print(f"    p{i} → {span:<11} {p}")
    print()

