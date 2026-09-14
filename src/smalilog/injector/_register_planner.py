"""Planificación de registros frescos para inyección."""
from __future__ import annotations

from ._smali_model import SmaliMethod, count_parameter_registers


def plan_hook_registers(method: SmaliMethod, need: int = 2) -> dict:
    param_regs = count_parameter_registers(method)

    if method.directive == "locals":
        orig_locals = method.registers_value
    else:
        # En .registers N, las variables locales originales son N - param_regs
        orig_locals = max(0, method.total_regs - param_regs)

    # Los registros temporales frescos SE TOMAN justo después de las locales originales:
    # Ejemplo: si orig_locals=1 y need=2 -> ['v1', 'v2']
    temps = [f"v{orig_locals + k}" for k in range(need)]

    new_locals = orig_locals + need
    new_total_regs = new_locals + param_regs

    expand_to = new_locals if method.directive == "locals" else new_total_regs

    return {
        "expand_to": expand_to,
        "new_total_regs": new_total_regs,
        "temps": temps,
        "param_regs": param_regs,
        "orig_locals": orig_locals,
        "map_p0_to_v": f"v{new_total_regs - param_regs}" if param_regs > 0 else None,
    }

