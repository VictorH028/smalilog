"""DSL de filtros combinables sobre el SmaliIndex.

Un `Query` se aplica a MethodInfo / ClassInfo y devuelve un subconjunto.

Ejemplos:
    q = Query.returning("Ljava/lang/String;").named("get*")
    q = Query.calling("Lcom/deadnote/RemoteLogger;")
    q = Query.containing_string("https://")
    q = Query.using_opcode("if-eqz")
    q = Query.named("onCreate").returning("V")
    results = q.run(index)
"""
from __future__ import annotations

import fnmatch
import re
from dataclasses import dataclass, field
from typing import Callable

from ._scanner import MethodInfo, SmaliIndex


Predicate = Callable[[MethodInfo], bool]


@dataclass
class Query:
    _predicates: list[Predicate] = field(default_factory=list)
    _desc: list[str] = field(default_factory=list)

    # ---------- builders ----------

    def named(self, pattern: str) -> Query:
        """Nombre de método, glob estilo shell: get*, *Title*, *."""
        rx = re.compile(fnmatch.translate(pattern), re.IGNORECASE)
        self._predicates.append(lambda m: bool(rx.match(m.name)))
        self._desc.append(f"name~{pattern}")
        return self

    def returning(self, ret_type: str) -> Query:
        """Tipo de retorno smali. Acepta atajos: string, int, void..."""
        t = {
            "string": "Ljava/lang/String;",
            "int": "I", "long": "J", "double": "D", "float": "F",
            "boolean": "Z", "bool": "Z", "void": "V",
            "char": "C", "byte": "B", "short": "S",
        }.get(ret_type.lower(), ret_type)
        self._predicates.append(lambda m: m.return_type == t)
        self._desc.append(f"returns={t}")
        return self

    def in_class(self, class_pattern: str) -> Query:
        """Clase contenedora (substring o glob)."""
        rx = re.compile(fnmatch.translate(class_pattern), re.IGNORECASE)
        self._predicates.append(lambda m: bool(rx.match(m.class_name)))
        self._desc.append(f"class~{class_pattern}")
        return self

    def calling(self, target_pattern: str) -> Query:
        """Llamadas salientes: algún invoke cuyo target encaje."""
        rx = re.compile(fnmatch.translate(target_pattern), re.IGNORECASE)
        self._predicates.append(
            lambda m: any(rx.match(t) for t in m.invokes)
        )
        self._desc.append(f"calls~{target_pattern}")
        return self

    def containing_string(self, pattern: str, *, regex: bool = False) -> Query:
        """Algún const-string del cuerpo coincide."""
        if regex:
            rx = re.compile(pattern)
            self._predicates.append(
                lambda m: any(rx.search(s) for s in m.const_strings)
            )
        else:
            rx = re.compile(re.escape(pattern), re.IGNORECASE)
            self._predicates.append(
                lambda m: any(rx.search(s) for s in m.const_strings)
            )
        self._desc.append(f"const~{pattern}")
        return self

    def using_opcode(self, opcode_pattern: str) -> Query:
        """Algún opcode del cuerpo encaja (glob: if-*, return-*, move-*)."""
        rx = re.compile(fnmatch.translate(opcode_pattern))
        self._predicates.append(
            lambda m: any(rx.match(o) for o in m.opcodes)
        )
        self._desc.append(f"opcode~{opcode_pattern}")
        return self

    def static(self) -> Query:
        self._predicates.append(lambda m: "static" in m.access.split())
        self._desc.append("static")
        return self

    def instance(self) -> Query:
        self._predicates.append(lambda m: "static" not in m.access.split())
        self._desc.append("instance")
        return self

    def custom(self, pred: Predicate, desc: str = "custom") -> Query:
        self._predicates.append(pred)
        self._desc.append(desc)
        return self

    # ---------- ejecución ----------

    def run(self, index: SmaliIndex, *, limit: int | None = None) -> list[MethodInfo]:
        out = []
        for m in index.methods:
            if all(p(m) for p in self._predicates):
                out.append(m)
                if limit and len(out) >= limit:
                    break
        return out

    @property
    def description(self) -> str:
        return " AND ".join(self._desc) or "<todos>"

