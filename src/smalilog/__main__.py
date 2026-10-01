"""Permite ejecutar ``python -m smalilog``."""
from .main import cli

if __name__ == "__main__":
    raise SystemExit(cli())
