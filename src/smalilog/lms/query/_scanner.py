"""Escáner local de smali. Lee smali*/ y construye un índice en memoria.

Se apoya en `smalilog.smali` (parser y modelo) que ya tienes.
"""
from __future__ import annotations

import json
import pickle
import re
import time
from dataclasses import dataclass, field
from pathlib import Path

from smalilog.smali import SmaliMethod, parse_class_name, parse_smali_file


SMALI_DIRS_GLOB = "smali*"


@dataclass
class MethodInfo:
    class_name: str
    name: str
    signature: str
    access: str
    return_type: str
    parameters: list[str]
    file: str          # ruta relativa al root
    line: int          # línea donde empieza .method
    const_strings: list[str] = field(default_factory=list)
    invokes: list[str] = field(default_factory=list)   # targets completos "Lx;->y(...)"
    opcodes: list[str] = field(default_factory=list)   # "if-eqz", "return-object", ...

    @property
    def symbol(self) -> str:
        return f"{self.class_name}->{self.name}{self.signature}"


@dataclass
class ClassInfo:
    class_name: str
    superclass: str | None
    interfaces: list[str]
    file: str
    methods: list[MethodInfo] = field(default_factory=list)
    fields: list[str] = field(default_factory=list)   # "Lx;->name:TYPE"


class SmaliIndex:
    """Índice en memoria de un codebase smali."""

    def __init__(self, root: Path):
        self.root = Path(root)
        self.classes: dict[str, ClassInfo] = {}
        self.methods: list[MethodInfo] = []
        self._loaded_at: float = 0.0
        self._stats: dict = {}

    # ---------- carga ----------

    def build(self, *, verbose: bool = True) -> dict:
        t0 = time.time()
        smali_dirs = sorted(p for p in self.root.glob(SMALI_DIRS_GLOB) if p.is_dir())
        if not smali_dirs:
            # acepta también un root que ya sea smali/
            if self.root.name.startswith("smali"):
                smali_dirs = [self.root]
            else:
                raise FileNotFoundError(
                    f"No encuentro smali*/ en {self.root}. "
                    f"¿Es la raíz del APK descompilado?"
                )

        n_files = 0
        for d in smali_dirs:
            for f in d.rglob("*.smali"):
                try:
                    self._scan_file(f)
                    n_files += 1
                    if verbose and n_files % 2000 == 0:
                        print(f"  ... {n_files} archivos")
                except Exception:  # noqa: BLE001
                    continue

        self._loaded_at = time.time()
        self._stats = {
            "root": str(self.root),
            "files": n_files,
            "classes": len(self.classes),
            "methods": len(self.methods),
            "seconds": round(self._loaded_at - t0, 2),
        }
        return self._stats

    def _scan_file(self, path: Path) -> None:
        try:
            content = path.read_text(encoding="utf-8-sig", errors="ignore")
        except OSError:
            return
        if ".class " not in content:
            return

        class_name = parse_class_name(content)
        if not class_name:
            return

        lines, methods = parse_smali_file(content)
        rel = str(path.relative_to(self.root))

        # superclase e interfaces
        superclass = None
        interfaces: list[str] = []
        for ln in lines[:50]:
            s = ln.strip()
            if s.startswith(".super "):
                superclass = s.split()[-1]
            elif s.startswith(".implements "):
                interfaces.append(s.split()[-1])

        cinfo = ClassInfo(
            class_name=class_name,
            superclass=superclass,
            interfaces=interfaces,
            file=rel,
        )

        for m in methods:
            if not m.has_body:
                continue
            body = lines[m.start_line:m.end_line + 1]
            mi = MethodInfo(
                class_name=class_name,
                name=m.name,
                signature=m.signature,
                access=m.access,
                return_type=m.return_type,
                parameters=list(m.parameters),
                file=rel,
                line=m.start_line + 1,
            )
            for raw in body:
                s = raw.strip()
                if s.startswith("const-string"):
                    mi.const_strings.append(_extract_const_string(s))
                elif s.startswith("invoke-"):
                    target = _extract_invoke_target(s)
                    if target:
                        mi.invokes.append(target)
                opc = _extract_opcode(s)
                if opc:
                    mi.opcodes.append(opc)

            cinfo.methods.append(mi)
            self.methods.append(mi)

        self.classes[class_name] = cinfo

    # ---------- persistencia ----------

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("wb") as f:
            pickle.dump({
                "root": self.root,
                "classes": self.classes,
                "methods": self.methods,
                "stats": self._stats,
                "loaded_at": self._loaded_at,
            }, f, protocol=pickle.HIGHEST_PROTOCOL)

    @classmethod
    def load(cls, path: Path) -> SmaliIndex:
        with path.open("rb") as f:
            data = pickle.load(f)
        idx = cls(data["root"])
        idx.classes = data["classes"]
        idx.methods = data["methods"]
        idx._stats = data.get("stats", {})
        idx._loaded_at = data.get("loaded_at", 0.0)
        return idx

    @property
    def stats(self) -> dict:
        return dict(self._stats)


# ---------- helpers de parseo de una línea ----------

_CONST_STRING_RX = re.compile(r'const-string(?:/jumbo)?\s+\S+,\s*"(.*)"\s*$')
_INVOKE_RX = re.compile(r"invoke-\w+(?:/range)?\s+\{[^}]*\},\s*(\S+)")
_OPCODE_RX = re.compile(r"^([a-z][\w\-/]*)\b")


def _extract_const_string(line: str) -> str:
    m = _CONST_STRING_RX.search(line)
    return m.group(1) if m else ""


def _extract_invoke_target(line: str) -> str | None:
    m = _INVOKE_RX.search(line)
    return m.group(1) if m else None


def _extract_opcode(line: str) -> str | None:
    if not line or line.startswith((".", "#", ":")):
        return None
    m = _OPCODE_RX.match(line)
    return m.group(1) if m else None




