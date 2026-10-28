"""Modelo de recetas Renef traducibles a instrumentación Smali."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from ._lua import (
    is_string_literal,
    iter_calls,
    last_return_literal,
    parse_string,
    section_after,
    split_args,
    strip_comments,
)


class Action(str, Enum):
    """Acción estática que se puede aplicar sobre un método."""

    STUB = "stub"
    LOG_ENTER = "log_enter"
    LOG_EXIT = "log_exit"
    LOG_BOTH = "log_both"
    NATIVE = "native"
    UNSUPPORTED = "unsupported"


@dataclass
class Recipe:
    """Una llamada a ``hook``/``safe_hook`` ya clasificada."""

    action: Action
    class_name: str | None = None
    method: str | None = None
    signature: str | None = None
    label: str = ""
    return_value: object = None
    reason: str = ""
    line: int = 0

    @property
    def target(self) -> str:
        if not self.class_name:
            return self.label or "?"
        return f"{self.class_name}->{self.method}{self.signature}"

    @property
    def applicable(self) -> bool:
        return self.action in {
            Action.STUB, Action.LOG_ENTER, Action.LOG_EXIT, Action.LOG_BOTH,
        }


@dataclass
class ScriptReport:
    """Resultado de analizar un script Renef."""

    recipes: list[Recipe] = field(default_factory=list)
    runtime_features: list[str] = field(default_factory=list)
    path: Path | None = None

    @property
    def applicable(self) -> list[Recipe]:
        return [r for r in self.recipes if r.applicable]


_RUNTIME_PATTERNS = {
    "Module.": "Module.* (módulos, símbolos y offsets)",
    "Memory.": "Memory.* (lectura/escritura/escaneo de memoria)",
    "Syscall.": "Syscall.* (trazado de syscalls)",
    "Java.use(": "Java.use (invocación Java en runtime)",
    "Java.registerClass(": "Java.registerClass (clases dinámicas)",
    "Java.array(": "Java.array (arrays JNI en runtime)",
    "Java.cast(": "Java.cast (casteo JNI en runtime)",
    "Thread.": "Thread.* (hilos/backtrace)",
    "File.": "File.* (acceso a archivos del proceso)",
    "OS.": "OS.* (señales/procesos)",
    "KCov.": "KCov.* (cobertura en runtime)",
}


def runtime_features(source: str) -> list[str]:
    """Detecta APIs de Renef que solo existen en runtime."""
    clean = strip_comments(source)
    found = [label for token, label in _RUNTIME_PATTERNS.items()
             if token in clean]
    return sorted(set(found))


def _line_of(source: str, position: int) -> int:
    return source.count("\n", 0, position) + 1


def _classify(options: str) -> tuple[Action, object, str]:
    """Decide la acción estática a partir de la tabla de opciones."""
    skip = bool(re.search(r"\bargs\.skip\s*=\s*true", options))
    has_enter = bool(re.search(r"\bonEnter\b", options))
    has_leave = bool(re.search(r"\bonLeave\b", options))

    on_enter = section_after(options, "onEnter") if has_enter else ""
    on_leave = section_after(options, "onLeave") if has_leave else ""

    found, value, constant, is_nil = (
        last_return_literal(on_leave) if has_leave
        else (False, None, False, False)
    )
    if found and not constant and value == "retval":
        found, value = False, None

    if skip:
        if found and not constant:
            return (Action.UNSUPPORTED, None,
                    f"args.skip con retorno no constante: {value!r}")
        return (Action.STUB, value if found and not is_nil else None,
                "args.skip")

    if found and constant and not is_nil:
        return Action.STUB, value, "onLeave devuelve una constante"

    if found and not constant:
        return (Action.UNSUPPORTED, None,
                f"retorno no constante: {value!r}")

    if re.search(r"\bargs\s*\[\s*\d+\s*\]\s*=", on_enter or options):
        return (Action.UNSUPPORTED, None,
                "reescribe argumentos (args[n] = ...) en runtime")

    if has_enter and has_leave:
        return Action.LOG_BOTH, None, "observación de entrada y salida"
    if has_enter:
        return Action.LOG_ENTER, None, "observación de entrada"
    if has_leave:
        return Action.LOG_EXIT, None, "observación de salida"
    return Action.UNSUPPORTED, None, "hook sin acción reconocible"


def _add(recipes: list[Recipe], recipe: Recipe) -> None:
    """Añade una receta evitando duplicados del mismo destino."""
    if recipe.class_name and recipe.method:
        for existing in recipes:
            if (existing.class_name == recipe.class_name
                    and existing.method == recipe.method
                    and existing.signature == recipe.signature):
                if existing.action == Action.STUB:
                    return
                if recipe.action == Action.STUB:
                    existing.action = Action.STUB
                    existing.return_value = recipe.return_value
                    existing.reason = recipe.reason
                return
    recipes.append(recipe)


def parse_script(source: str, path: Path | None = None) -> ScriptReport:
    """Analiza un script Renef y devuelve sus recetas estáticas."""
    report = ScriptReport(
        runtime_features=runtime_features(source),
        path=path,
    )

    for name, args_text, position in iter_calls(source, {"hook", "safe_hook"}):
        args = split_args(args_text)
        if len(args) < 3:
            continue

        class_name = parse_string(args[0])
        method = parse_string(args[1])
        signature = parse_string(args[2])

        # Hook nativo: hook("libfoo.so", 0x1234, {...}).
        if (name == "hook" and class_name and class_name.endswith(".so")
                and not is_string_literal(args[1])):
            report.recipes.append(Recipe(
                action=Action.NATIVE,
                label=class_name,
                reason=(f"hook nativo en {class_name} "
                        f"(offset {args[1].strip()}); requiere agente Renef"),
                line=_line_of(source, position),
            ))
            continue

        if not (class_name and method and signature):
            continue
        if not signature.startswith("("):
            continue

        label = ""
        if len(args) >= 5:
            label = parse_string(args[4]) or ""
        options = args[3] if len(args) >= 4 else ""

        if not options.strip().startswith("{"):
            report.recipes.append(Recipe(
                action=Action.UNSUPPORTED,
                class_name=class_name, method=method, signature=signature,
                label=label,
                reason="opciones dinámicas (no es una tabla literal)",
                line=_line_of(source, position),
            ))
            continue

        action, value, reason = _classify(options)
        if action == Action.STUB and method.startswith("<"):
            action, value = Action.UNSUPPORTED, None
            reason = "no se permiten stubs en constructores/<clinit>"
        _add(report.recipes, Recipe(
            action=action,
            class_name=class_name, method=method, signature=signature,
            label=label, return_value=value, reason=reason,
            line=_line_of(source, position),
        ))

    return report
