"""Helpers de emisión de instrucciones Dalvik."""
from __future__ import annotations


def _regnum(r: str) -> int:
    return int(r[1:])


def invoke_static(regs: list[str], target: str) -> str:
    nums = [_regnum(r) for r in regs]
    if len(regs) == 1:
        if nums[0] <= 15:
            return f"invoke-static {{{regs[0]}}}, {target}"
        return f"invoke-static/range {{{regs[0]} .. {regs[0]}}}, {target}"
    if max(nums) <= 15:
        return f"invoke-static {{{', '.join(regs)}}}, {target}"
    if nums == list(range(nums[0], nums[0] + len(nums))):
        return f"invoke-static/range {{{regs[0]} .. {regs[-1]}}}, {target}"
    raise ValueError(f"Registros no contiguos para /range: {regs}")


def move_object(dst: str, src: str) -> str:
    if _regnum(dst) > 15 or _regnum(src) > 15:
        return f"move-object/16 {dst}, {src}"
    return f"move-object {dst}, {src}"


def const_null(reg: str) -> str:
    if _regnum(reg) <= 15:
        return f"const/4 {reg}, 0x0"
    return f"const/16 {reg}, 0x0"


_WIDE_BOX = {
    "J": "Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;",
    "D": "Ljava/lang/Double;->valueOf(D)Ljava/lang/Double;",
}


def box_scalar(desc: str, src: str, dst: str) -> list[str]:
    """Boxea un escalar smali a Object."""
    if desc == "F":
        target = "Ljava/lang/Float;->valueOf(F)Ljava/lang/Float;"
    elif desc in _WIDE_BOX:
        target = _WIDE_BOX[desc]
    else:
        target = "Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;"
    return [invoke_static([src], target), f"move-result-object {dst}"]


def indent(code: str, spaces: int = 4) -> str:
    prefix = " " * spaces
    return "\n".join(
        prefix + ln if ln.strip() else ln for ln in code.split("\n")
    )
