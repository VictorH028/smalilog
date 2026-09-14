"""Resaltado de sintaxis Smali (Pygments con fallback propio)."""
from __future__ import annotations

import re
from functools import lru_cache

from ._colors import Color, _c, log_info


try:
    from pygments import highlight as _pg_highlight
    from pygments.formatters import Terminal256Formatter
    from pygments.lexers import SmaliLexer
    _HAS_PYGMENTS = True
except ImportError:
    _HAS_PYGMENTS = False


_FALLBACK_NOTED = False


_FALLBACK_TOKEN_RE = re.compile(
    r"""
      (?P<comment>\#.*)
    | (?P<string>"(?:\\.|[^"\\])*")
    | (?P<memberref>L[^\s]*;->[^\s]*)
    | (?P<directive>\.[\w\-]+)
    | (?P<label>:[\w$\-]+)
    | (?P<opcode>^[ \t]*[A-Za-z][\w\-/]*)
    | (?P<reg>[vp]\d+\b)
    | (?P<number>-?0x[0-9a-fA-F]+|-?\d+)
    | (?P<type>\[?L[\w/$\-]+;|\[[IJSZBCDF]\b)
    """,
    re.VERBOSE,
)

_FB_COLORS = {
    "comment":   Color.DIM,
    "string":    Color.GREEN,
    "directive": Color.MAGENTA,
    "label":     Color.CYAN,
    "opcode":    Color.BOLD + Color.BLUE,
    "reg":       Color.YELLOW,
    "number":    Color.RED,
    "type":      Color.CYAN,
}


def _color_memberref(tok: str) -> str:
    arrow = tok.find("->")
    if arrow == -1:
        return tok
    cls, rest = tok[:arrow + 2], tok[arrow + 2:]
    cuts = [i for i in (rest.find("("), rest.find(":")) if i != -1]
    cut = min(cuts) if cuts else -1
    name, sig = (rest, "") if cut == -1 else (rest[:cut], rest[cut:])
    return (f"{Color.CYAN}{cls}{Color.RESET}"
            f"{Color.BOLD}{name}{Color.RESET}"
            f"{Color.DIM}{sig}{Color.RESET}")


def _highlight_fallback(line: str) -> str:
    s = line.strip()
    if not s:
        return line
    if s.startswith("#"):
        return f"{Color.DIM}{line}{Color.RESET}"
    if s.startswith(".method") or s == ".end method":
        return f"{Color.BOLD}{Color.MAGENTA}{line}{Color.RESET}"
    out, last = [], 0
    for m in _FALLBACK_TOKEN_RE.finditer(line):
        out.append(line[last:m.start()])
        kind = m.lastgroup
        tok = m.group()
        out.append(_color_memberref(tok) if kind == "memberref"
                   else f"{_FB_COLORS[kind]}{tok}{Color.RESET}")
        last = m.end()
    out.append(line[last:])
    return "".join(out)


@lru_cache(maxsize=None)
def _pg_formatter(style: str):
    return Terminal256Formatter(style=style)


def _notify_fallback_once() -> None:
    global _FALLBACK_NOTED
    if not _HAS_PYGMENTS and not _FALLBACK_NOTED:
        log_info("pygments no instalado: resaltado básico "
                 "(pip install pygments para el completo)")
        _FALLBACK_NOTED = True


def highlight_line(line: str, color: bool = True, style: str = "default") -> str:
    if not color:
        return line
    if _HAS_PYGMENTS:
        return _pg_highlight(line, SmaliLexer(),
                             _pg_formatter(style)).rstrip("\n")
    _notify_fallback_once()
    return _highlight_fallback(line)


def has_pygments() -> bool:
    return _HAS_PYGMENTS
