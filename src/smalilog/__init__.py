"""smalilog - Remote logger para Android."""

from . import config
from .server import LogServer

__version__ = config.VERSION
__all__ = ["LogServer", "config", "__version__"]
