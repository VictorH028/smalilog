# smalilog/lms/trainer.py
"""Combina MCP + memoria local para búsqueda con ranking aprendido."""
from __future__ import annotations

import os
import sys

from .db import Memory
from .mcp_client import SmaliMcpClient


class Trainer:
    """
    Combina MCP + memoria local:
      - Resuelve alias (y sigue buscando por si acaso).
      - Re-rankea combinando score del MCP con afinidad aprendida.
      - Registra feedback.
    """

    def __init__(self, mem: Memory, mcp: SmaliMcpClient):
        self.mem, self.mcp = mem, mcp

    async def search(self, query: str, limit: int = 15) -> list[dict]:
        # 1) alias (sin cortocircuitar)
        alias_target = await self.mem.resolve_alias(query)

        # 2) fuzzy vía MCP — el tool se llama smali_search_symbols y
        #    recibe `pattern` (no `query`). No acepta `limit`.
        try:
            raw = await self.mcp.call_tool(
                "smali_search_symbols", {"pattern": query}
            )
        except Exception as exc:  # noqa: BLE001
            sys.stderr.write(f"[trainer] MCP falló: {exc!r}\n")
            if alias_target:
                return [{"symbol": alias_target, "_alias": True}]
            raise

        if os.environ.get("SMALILOG_DEBUG"):
            import json
            sys.stderr.write(
                "[trainer] raw: "
                + json.dumps(raw, ensure_ascii=False, default=str)[:800]
                + "\n"
            )

        if isinstance(raw, list):
            items = raw
        elif isinstance(raw, dict):
            items = (
                raw.get("symbols")
                or raw.get("results")
                or raw.get("items")
                or []
            )
        else:
            items = []

        # 3) inyectar alias al frente si existe
        if alias_target:
            items = [{"symbol": alias_target, "_alias": True}] + [
                it for it in items
                if (it.get("symbol") or it.get("name")) != alias_target
            ]

        # 4) re-rank: base_mcp + afinidad aprendida; alias siempre primero
        aff = await self.mem.affinity_for(query) or {}
        max_aff = max(aff.values(), default=0.0) or 1.0

        def score(it: dict) -> float:
            if it.get("_alias"):
                return 1_000_000.0
            sym = it.get("symbol") or it.get("name") or ""
            base = float(it.get("score", 0.0) or 0.0)
            a = aff.get(sym, 0.0) / max_aff
            return base + a

        items.sort(key=score, reverse=True)
        return items[:limit]

    async def record_choice(self, query: str, symbol: str) -> None:
        await self.mem.feedback(query, symbol)



