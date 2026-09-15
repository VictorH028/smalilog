"""Planificación de registros frescos para inyección."""
from __future__ import annotations

from ._smali_model import SmaliMethod, count_parameter_registers

def plan_hook_registers(method: SmaliMethod, need: int = 2) -> dict:
    param_regs = count_parameter_registers(method)

    if method.directive == "locals":
        orig_locals = method.registers_value
        first_free = orig_locals            # params van después, implícitos
        new_total_regs = orig_locals + need + param_regs
        expand_to = orig_locals + need
    else:
        # .registers N: params están al final. Temps van DESPUÉS de N.
        new_total_regs = method.registers_value + need
        orig_locals = max(0, method.registers_value - param_regs)
        first_free = method.registers_value
        expand_to = new_total_regs

    temps = [f"v{first_free + k}" for k in range(need)]

    return {
        "expand_to": expand_to,
        "new_total_regs": new_total_regs,
        "temps": temps,
        "param_regs": param_regs,
        "orig_locals": orig_locals,
        "map_p0_to_v": f"v{new_total_regs - param_regs}" if param_regs > 0 else None,
    }
