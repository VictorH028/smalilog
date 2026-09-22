"""UI de smalilog: colores, logging y resaltado de smali."""
from __future__ import annotations

from ._colors import (
    Color,
    _c,
    log_error,
    log_header,
    log_info,
    log_ok,
    log_warn,
    use_color_default,
    set_use_color,
)

from ._highlight import (
    has_pygments,
    highlight_line,
)

__all__ = [
    "Color",
    "_c",
    "log_info",
    "log_ok",
    "log_warn",
    "log_error",
    "log_header",
    "set_use_color",
    "use_color_default",
    "highlight_line",
    "has_pygments",
]
