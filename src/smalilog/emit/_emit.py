"""Helpers de emisión de instrucciones Dalvik."""


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
    d, s = _regnum(dst), _regnum(src)
    if d <= 15 and s <= 15:
        return f"move-object {dst}, {src}"
    if d <= 255 and s <= 65535:
        return f"move-object/from16 {dst}, {src}"
    raise ValueError(f"move-object no soporta {dst}, {src}")

def move_result_object(dst: str) -> str:
    if _regnum(dst) > 255:
        raise ValueError(f"move-result-object solo v0..v255, no {dst}")
    return f"move-result-object {dst}"

def const_null(reg: str) -> str:
    n = _regnum(reg)
    if n <= 15:
        return f"const/4 {reg}, 0x0"
    if n <= 255:
        return f"const/16 {reg}, 0x0"
    return f"const {reg}, 0x0"


_WIDE_BOX = {
    "J": "Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;",
    "D": "Ljava/lang/Double;->valueOf(D)Ljava/lang/Double;",
}


def box_scalar(desc: str, src: str, dst: str) -> list[str]:
    """Boxea un escalar smali a Object."""
    if _regnum(dst) > 255:
        raise ValueError(f"move-result-object solo acepta v0..v255, no {dst}")
    if desc == "F":
        target = "Ljava/lang/Float;->valueOf(F)Ljava/lang/Float;"
    elif desc in _WIDE_BOX:
        target = _WIDE_BOX[desc]
    else:
        target = "Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;"
    return [invoke_static([src], target), f"move-result-object {dst}"]


def indent(code: str, spaces: int = 4) -> str:
    pad = " " * spaces
    return "\n".join(pad + ln if ln.strip() else ln for ln in code.splitlines())

