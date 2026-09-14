"""Parser de archivos Smali."""
from __future__ import annotations

import re

from ._smali_model import SmaliMethod


def _parse_method_line(line: str):
    """Devuelve (access, name, signature) o None."""
    rest = line[len(".method"):].strip()
    p = rest.find("(")
    if p == -1:
        return None
    head = rest[:p].split()
    if not head:
        return None
    return " ".join(head[:-1]), head[-1], rest[p:]


def parse_smali_file(content: str):
    lines = content.splitlines()
    methods: list[SmaliMethod] = []
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped.startswith(".method"):
            parsed = _parse_method_line(stripped)
            start = i
            j = i + 1
            end = len(lines) - 1
            has_body = False
            directive, reg_val = "registers", 0
            while j < len(lines):
                s = lines[j].strip()
                if s.startswith(".end method"):
                    has_body, end = True, j
                    break
                if s.startswith(".method"):
                    end = j - 1
                    break
                mm = re.match(r"\.(registers|locals)\s+(\d+)", s)
                if mm:
                    directive, reg_val = mm.group(1), int(mm.group(2))
                j += 1
            if parsed:
                access, name, signature = parsed
                methods.append(SmaliMethod(
                    name, signature, access, directive, reg_val,
                    start, end, has_body,
                ))
            i = end
        i += 1
    return lines, methods


def parse_class_name(content: str) -> str | None:
    for line in content.splitlines():
        s = line.strip()
        if s.startswith(".class"):
            parts = s.split()
            if parts:
                return parts[-1]
    return None
