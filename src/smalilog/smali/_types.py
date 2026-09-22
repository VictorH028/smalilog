"""Utilidades de tipos Smali."""
from __future__ import annotations

import re


def _type_size(desc: str) -> int:
    """J (long) y D (double) ocupan 2 registros."""
    return 2 if desc in ("J", "D") else 1


def is_reference(desc: str) -> bool:
    return desc[:1] in ("L", "[")


def parse_type_list(params_str: str) -> list[str]:
    params: list[str] = []
    i = 0
    while i < len(params_str):
        c = params_str[i]
        if c == "L":
            end = params_str.index(";", i)
            params.append(params_str[i:end + 1]); i = end + 1
        elif c == "[":
            start = i
            while i < len(params_str) and params_str[i] == "[":
                i += 1
            if i < len(params_str) and params_str[i] == "L":
                end = params_str.index(";", i)
                params.append(params_str[start:end + 1]); i = end + 1
            else:
                params.append(params_str[start:i + 1]); i += 1
        else:
            params.append(c); i += 1
    return params


def params_raw(signature: str) -> str:
    m = re.search(r"\((.*?)\)", signature)
    return m.group(1) if m else ""


def return_raw(signature: str) -> str:
    m = re.search(r"\)(.+)$", signature)
    return m.group(1) if m else "V"
