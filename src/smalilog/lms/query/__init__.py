# src/smalilog/lms/query/__init__.py
"""Subpaquete de consultas sobre smali (scanner, query DSL, manifest)."""
from __future__ import annotations

from ._manifest import Component, ManifestInfo, parse_manifest
from ._query import Query
from ._scanner import ClassInfo, MethodInfo, SmaliIndex

__all__ = [
    "Component", "ManifestInfo", "parse_manifest",
    "Query",
    "ClassInfo", "MethodInfo", "SmaliIndex",
]

