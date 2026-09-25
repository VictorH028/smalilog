"""Planificación de registros frescos para inyección."""
from __future__ import annotations

from ._model import SmaliMethod, count_parameter_registers

def plan_hook_registers(method: SmaliMethod, need: int = 2) -> dict:
    param_regs = count_parameter_registers(method)

    if method.directive == "locals":
        orig_locals = method.registers_value
        first_free = orig_locals
        expand_to = orig_locals + need
        new_total_regs = expand_to + param_regs
    else:
        orig_total = method.registers_value
        orig_locals = max(0, orig_total - param_regs)
        # Tras expandir, los params se mueven al final.
        # Los registros originales de params (v[orig_locals..orig_total-1])
        # quedan libres y son contiguos → primeros temps frescos.
        first_free = orig_locals
        expand_to = orig_total + need
        new_total_regs = expand_to

    temps = [f"v{first_free + k}" for k in range(need)]

    return {
        "expand_to": expand_to,
        "new_total_regs": new_total_regs,
        "temps": temps,
        "needed": need,
        "param_regs": param_regs,
        "orig_locals": orig_locals,
        "map_p0_to_v": f"v{new_total_regs - param_regs}" if param_regs > 0 else None,
    }
