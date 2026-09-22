"""Colores ANSI y helpers de smalilog."""
from __future__ import annotations

import os
import sys


class Color:
    RED = "\033[91m"; GREEN = "\033[92m"; YELLOW = "\033[93m"
    MAGENTA = "\033[95m"; BLUE = "\033[94m"; CYAN = "\033[96m"
    BOLD = "\033[1m"; RESET = "\033[0m"; DIM = "\033[2m"; GRAY = "\033[90m"


_USE_COLOR = sys.stdout.isatty() and not os.environ.get("NO_COLOR")


def _c(code: str, msg: str) -> str:
    return f"{code}{msg}{Color.RESET}" if _USE_COLOR else str(msg)


def log_info(msg):  print(f"{_c(Color.BLUE, '[INFO]')} {msg}")
def log_ok(msg):    print(f"{_c(Color.GREEN, '[OK]')} {msg}")
def log_warn(msg):  print(f"{_c(Color.YELLOW, '[WARN]')} {msg}")
def log_error(msg): print(f"{_c(Color.RED, '[ERROR]')} {msg}")


def log_header(msg: str) -> None:
    bar = "=" * 60
    print(f"\n{_c(Color.BOLD + Color.CYAN, bar)}")
    print(_c(Color.BOLD + Color.CYAN, msg))
    print(_c(Color.BOLD + Color.CYAN, bar) + "\n")


def use_color_default() -> bool:
    return _USE_COLOR


def set_use_color(value: bool | None = None) -> bool:
    global _USE_COLOR
    if value is not None:
        _USE_COLOR = value
    return _USE_COLOR
