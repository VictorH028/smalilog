"""Análisis y modificación de AndroidManifest.xml."""
from __future__ import annotations

from ._cli import build_manifest_parser, run_manifest
from ._manifest import (
    ManifestError,
    ManifestInfo,
    PatchResult,
    parse_manifest,
    patch_manifest,
    scan_smali_entries,
)

__all__ = [
    "ManifestError",
    "ManifestInfo",
    "PatchResult",
    "build_manifest_parser",
    "parse_manifest",
    "patch_manifest",
    "run_manifest",
    "scan_smali_entries",
]
