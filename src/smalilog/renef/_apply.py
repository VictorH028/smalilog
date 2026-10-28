"""Aplicación de recetas Renef sobre un árbol Smali descompilado."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from smalilog.injector._injector import HookInjector
from smalilog.smali import parse_class_name
from smalilog.ui import log_info, log_ok, log_warn

from ._recipe import Action, Recipe, ScriptReport

DEFAULT_LOGGER_CLASS = "Lcom/deadnote/RemoteLog;"
DEFAULT_TAG = "RENEF"


@dataclass
class AppliedItem:
    recipe: Recipe
    status: str                       # applied | skipped | failed
    detail: str = ""


@dataclass
class ApplyResult:
    items: list[AppliedItem] = field(default_factory=list)

    @property
    def applied(self) -> int:
        return sum(1 for i in self.items if i.status == "applied")

    @property
    def skipped(self) -> int:
        return sum(1 for i in self.items if i.status == "skipped")

    @property
    def failed(self) -> int:
        return sum(1 for i in self.items if i.status == "failed")

    @property
    def ok(self) -> bool:
        return self.failed == 0 and self.applied > 0


def _normalize_class(name: str) -> str:
    """Acepta ``com/foo/Bar`` o ``Lcom/foo/Bar;`` y devuelve el descriptor."""
    name = name.strip().replace(".", "/")
    if name.startswith("L") and name.endswith(";"):
        return name
    return f"L{name};"


class SmaliLocator:
    """Busca el archivo .smali de una clase en un APK descompilado."""

    def __init__(self, root: str | Path):
        self.root = Path(root)
        if self.root.is_file():
            self.dirs = [self.root.parent]
            self.single_file = self.root
        else:
            self.single_file = None
            dirs = sorted(p for p in self.root.glob("smali*") if p.is_dir())
            self.dirs = dirs or [self.root]
        self._index: dict[str, Path] | None = None

    def _build_index(self) -> None:
        index: dict[str, Path] = {}
        for base in self.dirs:
            for path in base.rglob("*.smali"):
                try:
                    content = path.read_text(encoding="utf-8-sig",
                                             errors="ignore")
                except OSError:
                    continue
                class_name = parse_class_name(content)
                if class_name:
                    index.setdefault(class_name, path)
        self._index = index

    def find(self, class_name: str) -> Path | None:
        descriptor = _normalize_class(class_name)

        if self.single_file is not None:
            try:
                content = self.single_file.read_text(encoding="utf-8-sig",
                                                    errors="ignore")
            except OSError:
                return None
            return (self.single_file
                    if parse_class_name(content) == descriptor else None)

        relative = descriptor[1:-1] + ".smali"
        for base in self.dirs:
            candidate = base / relative
            if candidate.exists():
                return candidate

        if self._index is None:
            self._build_index()
        return (self._index or {}).get(descriptor)


def _label(recipe: Recipe) -> str:
    if recipe.label:
        return recipe.label
    return recipe.target


def apply_report(
    report: ScriptReport,
    smali_root: str | Path,
    *,
    logger_class: str = DEFAULT_LOGGER_CLASS,
    tag: str = DEFAULT_TAG,
    dry_run: bool = False,
    backup: bool = True,
    only: str | None = None,
) -> ApplyResult:
    """Aplica las recetas aplicables del reporte.

    ``only`` filtra por ``clase#método`` (subcadena, sin distinguir mayúsculas).
    Devuelve un resumen con el estado de cada receta.
    """
    locator = SmaliLocator(smali_root)
    result = ApplyResult()
    only_norm = only.lower() if only else None

    for recipe in report.recipes:
        key = f"{recipe.class_name or recipe.label}#{recipe.method or ''}"
        if only_norm and only_norm not in key.lower():
            continue

        if not recipe.applicable:
            result.items.append(AppliedItem(
                recipe, "skipped", recipe.reason or "no traducible",
            ))
            continue

        assert recipe.class_name and recipe.method and recipe.signature
        path = locator.find(recipe.class_name)
        if path is None:
            result.items.append(AppliedItem(
                recipe, "skipped", "clase no encontrada en el árbol Smali",
            ))
            continue

        injector = HookInjector(str(path), logger_class)
        if not injector.load():
            result.items.append(AppliedItem(
                recipe, "failed", "no se pudo leer el archivo Smali",
            ))
            continue

        if not injector.resolve_method(recipe.method, recipe.signature):
            result.items.append(AppliedItem(
                recipe, "skipped", "método/firma no encontrados",
            ))
            continue

        ok = False
        if recipe.action == Action.STUB:
            ok = injector.inject_stub(recipe.return_value, _label(recipe))
        elif recipe.action == Action.LOG_ENTER:
            ok = injector.inject_log_level(
                "info", tag, f"Renef: {_label(recipe)}")
        elif recipe.action == Action.LOG_EXIT:
            ok = injector.inject_exit()
        elif recipe.action == Action.LOG_BOTH:
            ok = injector.inject_both()

        if not ok:
            result.items.append(AppliedItem(
                recipe, "failed", "la inyección Smali falló",
            ))
            continue

        if not dry_run:
            injector.save(backup=backup)

        detail = path.name if not dry_run else f"(dry-run) {path.name}"
        result.items.append(AppliedItem(
            recipe, "applied", detail,
        ))

    return result


def report_lines(result: ApplyResult) -> list[str]:
    """Genera líneas legibles del resultado de aplicación."""
    lines: list[str] = []
    for item in result.items:
        r = item.recipe
        prefix = {
            "applied": "[aplicado]",
            "skipped": "[omitido] ",
            "failed": "[fallido] ",
        }[item.status]
        detail = f" — {item.detail}" if item.detail else ""
        lines.append(f"{prefix} {r.action.value:<11} {r.target}{detail}")
    return lines


def print_summary(report: ScriptReport, result: ApplyResult) -> None:
    """Imprime un resumen en español para el CLI."""
    if report.runtime_features:
        log_info("APIs de runtime detectadas (no ejecutables sin root/agente):")
        for feature in report.runtime_features:
            print(f"    - {feature}")

    for line in report_lines(result):
        print(f"  {line}")

    log_ok(f"Aplicadas: {result.applied} · "
           f"omitidas: {result.skipped} · fallidas: {result.failed}")

    if result.applied == 0:
        log_warn("Ninguna receta pudo aplicarse. Revisa las rutas y firmas.")
