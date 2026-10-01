# smalilog/lms/config.py
"""Reexporta la configuración global de smalilog.

Históricamente este módulo tenía su propia copia; ahora es un alias
para evitar divergencias entre `smalilog.config` y `smalilog.lms.config`.
"""
from smalilog.config import Settings, settings  # noqa: F401

__all__ = ["Settings", "settings"]

