"""Modelo de método Smali y mapeo de registros de parámetros."""
from __future__ import annotations

from dataclasses import dataclass, field

from ._colors import log_warn
from ._smali_types import _type_size, parse_type_list, params_raw, return_raw


@dataclass
class SmaliMethod:
    name: str
    signature: str
    access: str
    directive: str            # 'registers' | 'locals'
    registers_value: int
    start_line: int
    end_line: int
    has_body: bool = True

    parameters: list[str] = field(init=False)
    return_type: str = field(init=False)

    def __post_init__(self):
        self.parameters = parse_type_list(params_raw(self.signature))
        self.return_type = return_raw(self.signature)

    def is_static(self) -> bool:
        return "static" in self.access.split()

    @property
    def n_param_regs(self) -> int:
        return count_parameter_registers(self)

    @property
    def total_regs(self) -> int:
        if self.directive == "locals":
            return self.registers_value + self.n_param_regs
        return self.registers_value

    def __repr__(self):
        return f"<SmaliMethod {self.name}{self.signature}>"


def count_parameter_registers(method: SmaliMethod) -> int:
    total = 0 if method.is_static() else 1
    for p in method.parameters:
        total += _type_size(p)
    return total


def param_register_offsets(method: SmaliMethod) -> list[tuple[int, int, int]]:
    """[(p_index, v_inicial, tamaño), ...] — respeta anchos wide."""
    base = method.total_regs - count_parameter_registers(method)
    out, cur = [], base
    if not method.is_static():
        out.append((0, cur, 1))
        cur += 1
    for i, p in enumerate(method.parameters):
        size = _type_size(p)
        out.append((i + (0 if method.is_static() else 1), cur, size))
        cur += size
    return out


def normalize_reg(reg: str, method: SmaliMethod) -> str:
    reg = reg.strip()
    if reg.startswith("v") and reg[1:].isdigit():
        return reg
    if reg.startswith("p") and reg[1:].isdigit():
        idx = int(reg[1:])
        base = method.total_regs - count_parameter_registers(method)
        if not method.is_static():
            if idx == 0:
                return f"v{base}"
            idx -= 1
        if 0 <= idx < len(method.parameters):
            offs = param_register_offsets(method)
            for (pi, start, size) in offs:
                if pi == idx:
                    return f"v{start}"
        log_warn(f"p{idx} fuera de rango en {method.name}")
    return reg
