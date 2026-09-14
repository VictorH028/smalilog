"""Planificación de registros frescos para inyección."""
from __future__ import annotations

from ._smali_model import SmaliMethod, count_parameter_registers


def plan_hook_registers(method: SmaliMethod, need: int = 3) -> dict:
    param_regs = count_parameter_registers(method)

    if method.directive == "locals":
        # Con .locals X, expandir a .locals (X + need)
        # Los nuevos temporales son los últimos locales añadidos: v{X} .. v{X + need - 1}
        new_locals = method.registers_value + need
        expand_to = new_locals
        temps = [f"v{method.registers_value + k}" for k in range(need)]
    else:
        # Con .registers N, expandir a .registers (N + need)
        # Al aumentar N, los parámetros se desplazan al final (v{N} .. v{N + param_regs - 1}).
        # Los temporales frescos quedan en el hueco v{N - param_regs + k} hasta v{N - 1}.
        expand_to = method.total_regs + need
        base_temp_index = method.total_regs - param_regs
        temps = [f"v{base_temp_index + k}" for k in range(need)]

    return {
        "expand_to": expand_to,
        "temps": temps,
    }

