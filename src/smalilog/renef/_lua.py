"""Lector mínimo de scripts Lua de Renef.

No interpreta Lua: localiza llamadas a ``hook``/``safe_hook`` y extrae sus
argumentos literales. El objetivo es obtener recetas estáticas para Smali,
no ejecutar código del usuario.
"""
from __future__ import annotations

import re
from typing import Iterator


_STRING_QUOTES = ("'", '"')


def strip_comments(source: str) -> str:
    """Elimina comentarios de Lua preservando strings y saltos de línea."""
    out: list[str] = []
    i = 0
    n = len(source)
    while i < n:
        c = source[i]

        if c in _STRING_QUOTES:
            quote = c
            out.append(c)
            i += 1
            while i < n:
                ch = source[i]
                out.append(ch)
                if ch == "\\" and i + 1 < n:
                    out.append(source[i + 1])
                    i += 2
                    continue
                i += 1
                if ch == quote:
                    break
            continue

        if c == "-" and i + 1 < n and source[i + 1] == "-":
            if source.startswith("--[[", i):
                end = source.find("]]", i + 4)
                end = n if end == -1 else end + 2
                out.append("".join("\n" if ch == "\n" else " "
                                   for ch in source[i:end]))
                i = end
                continue
            end = source.find("\n", i)
            end = n if end == -1 else end
            out.append(" " * (end - i))
            i = end
            continue

        out.append(c)
        i += 1
    return "".join(out)


def _read_balanced(source: str, start: int,
                   open_ch: str = "(", close_ch: str = ")") -> tuple[str, int]:
    """Devuelve el contenido entre paréntesis y el índice posterior."""
    assert source[start] == open_ch
    depth = 0
    i = start
    n = len(source)
    while i < n:
        c = source[i]
        if c in _STRING_QUOTES:
            quote = c
            i += 1
            while i < n:
                if source[i] == "\\":
                    i += 2
                    continue
                if source[i] == quote:
                    i += 1
                    break
                i += 1
            continue
        if c == open_ch:
            depth += 1
        elif c == close_ch:
            depth -= 1
            if depth == 0:
                return source[start + 1:i], i + 1
        i += 1
    return source[start + 1:], n


def iter_calls(source: str, names: set[str]) -> Iterator[tuple[str, str, int]]:
    """Itera ``(nombre, argumentos, posición)`` de las llamadas encontradas."""
    clean = strip_comments(source)
    i = 0
    n = len(clean)
    while i < n:
        c = clean[i]
        if c in _STRING_QUOTES:
            # Avance manual sobre el string.
            quote = c
            i += 1
            while i < n:
                if clean[i] == "\\":
                    i += 2
                    continue
                if clean[i] == quote:
                    i += 1
                    break
                i += 1
            continue

        if c.isalpha() or c == "_":
            j = i
            while j < n and (clean[j].isalnum() or clean[j] == "_"):
                j += 1
            word = clean[i:j]
            k = j
            while k < n and clean[k].isspace():
                k += 1
            if word in names and k < n and clean[k] == "(":
                args, end = _read_balanced(clean, k)
                yield word, args, i
                i = end
                continue
            i = j
            continue

        i += 1


def split_args(args: str) -> list[str]:
    """Separa argumentos de nivel superior por comas."""
    parts: list[str] = []
    current: list[str] = []
    depth = 0
    i = 0
    n = len(args)
    while i < n:
        c = args[i]
        if c in _STRING_QUOTES:
            quote = c
            current.append(c)
            i += 1
            while i < n:
                ch = args[i]
                current.append(ch)
                if ch == "\\" and i + 1 < n:
                    current.append(args[i + 1])
                    i += 2
                    continue
                i += 1
                if ch == quote:
                    break
            continue
        if c in "([{":
            depth += 1
            current.append(c)
        elif c in ")]}":
            depth -= 1
            current.append(c)
        elif c == "," and depth == 0:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(c)
        i += 1
    tail = "".join(current).strip()
    if tail:
        parts.append(tail)
    return parts


def parse_string(expr: str) -> str | None:
    """Convierte un literal de string Lua en ``str``; ``None`` si no lo es."""
    expr = expr.strip()
    if len(expr) < 2 or expr[0] not in _STRING_QUOTES:
        return None
    quote = expr[0]
    if expr[-1] != quote:
        return None
    body = expr[1:-1]
    out: list[str] = []
    i = 0
    while i < len(body):
        c = body[i]
        if c == "\\" and i + 1 < len(body):
            nxt = body[i + 1]
            mapping = {"n": "\n", "r": "\r", "t": "\t",
                       "\\": "\\", '"': '"', "'": "'", "0": "\0"}
            out.append(mapping.get(nxt, nxt))
            i += 2
            continue
        out.append(c)
        i += 1
    return "".join(out)


def is_string_literal(expr: str) -> bool:
    return parse_string(expr) is not None


_RETURN_RE = re.compile(
    r"\breturn\s+"
    r"(?P<value>"
    r"JNI\.string\(\s*(?P<jni>[\"'])(?P<jni_text>.*?)(?P=jni)\s*\)"
    r"|[\"'][^\"']*[\"']"
    r"|-?0x[0-9a-fA-F]+"
    r"|-?\d+"
    r"|true|false|nil"
    r"|[A-Za-z_][\w.]*(?:\.[A-Za-z_]\w*)*"
    r")"
)


def last_return_literal(text: str) -> tuple[bool, object, bool, bool]:
    """Devuelve ``(encontrado, valor, constante, es_nil)``.

    ``constante`` indica si el valor es un literal traducible a Smali.
    Las expresiones no constantes se devuelven como ``str`` y ``es_nil``
    distingue ``return nil`` (sin cambio) de ``return 0``.
    """
    matches = list(_RETURN_RE.finditer(text))
    if not matches:
        return False, None, False, False
    raw = matches[-1].group("value").strip()

    jni = matches[-1].group("jni_text")
    if jni is not None:
        return True, jni, True, False

    if raw in ("true", "false"):
        return True, raw == "true", True, False
    if raw == "nil":
        return True, None, True, True
    if re.fullmatch(r"-?0x[0-9a-fA-F]+", raw):
        return True, int(raw, 16), True, False
    if re.fullmatch(r"-?\d+", raw):
        return True, int(raw), True, False
    if raw[:1] in _STRING_QUOTES:
        return True, parse_string(raw), True, False
    return True, raw, False, False


def section_after(text: str, key: str) -> str:
    """Devuelve el texto desde ``key`` hasta el siguiente ``onEnter/onLeave``."""
    match = re.search(rf"\b{key}\b", text)
    if not match:
        return ""
    rest = text[match.end():]
    other = "onLeave" if key == "onEnter" else "onEnter"
    stop = re.search(rf"\b{other}\b", rest)
    return rest[:stop.start()] if stop else rest
