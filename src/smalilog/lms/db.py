# smalilog/lms/db.py
"""Memoria local (SQLite) para el mini-LMS."""
from __future__ import annotations

import re
import time
from pathlib import Path

import aiosqlite


_CAMEL = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")
_NONALNUM = re.compile(r"[^A-Za-z0-9]+")


SCHEMA = """
CREATE TABLE IF NOT EXISTS workspace (
    id INTEGER PRIMARY KEY,
    path TEXT UNIQUE NOT NULL,
    indexed_at REAL NOT NULL,
    files INTEGER, classes INTEGER, methods INTEGER, fields INTEGER
);

CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY,
    ts REAL NOT NULL,
    cmd TEXT NOT NULL,
    args TEXT NOT NULL,
    workspace TEXT
);

CREATE TABLE IF NOT EXISTS pinned (
    id INTEGER PRIMARY KEY,
    symbol TEXT NOT NULL,
    kind TEXT,
    note TEXT,
    ts REAL NOT NULL,
    UNIQUE(symbol)
);

CREATE TABLE IF NOT EXISTS alias (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    target TEXT NOT NULL,
    kind TEXT,
    hits INTEGER DEFAULT 0,
    ts REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY,
    query TEXT NOT NULL,
    chosen_symbol TEXT NOT NULL,
    ts REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS affinity (
    query_term TEXT NOT NULL,
    symbol TEXT NOT NULL,
    score REAL NOT NULL DEFAULT 0,
    PRIMARY KEY (query_term, symbol)
);

CREATE INDEX IF NOT EXISTS idx_hist_ts ON history(ts);
CREATE INDEX IF NOT EXISTS idx_fb_query ON feedback(query);
"""


async def _configure(db: aiosqlite.Connection) -> None:
    await db.execute("PRAGMA journal_mode=WAL")
    await db.execute("PRAGMA busy_timeout=5000")
    await db.execute("PRAGMA foreign_keys=ON")


def _connect(path) -> aiosqlite.Connection:
    return aiosqlite.connect(path)


def tokenize_query(q: str) -> list[str]:
    """Tokeniza tanto queries humanas como símbolos smali.

    'Lcom/example/LoginActivity;->doLogin' ->
        ['lcom', 'example', 'login', 'activity', 'dologin']
    'login screen' -> ['login', 'screen']
    """
    if not q:
        return []
    q = q.replace("->", " ").replace(";", " ")
    out = []
    for chunk in _NONALNUM.split(q):
        if not chunk:
            continue
        for part in _CAMEL.split(chunk):
            part = part.lower()
            if part:
                out.append(part)
    return out


# Alias retrocompatible (había código que importaba `_tokens`)
_tokens = tokenize_query


class Memory:
    def __init__(self, path: Path):
        self.path = Path(path)
        # ✅ Defensivo: crea el directorio padre ANTES de que nadie use la DB
        self.path.parent.mkdir(parents=True, exist_ok=True)

    async def init(self) -> None:
        # Por si acaso alguien instanció Memory antes de que existiera el dir
        self.path.parent.mkdir(parents=True, exist_ok=True)
        async with _connect(self.path) as db:
            await _configure(db)
            await db.executescript(SCHEMA)
            await db.commit()

    # ---------- workspace ----------
    async def upsert_workspace(self, path: str, stats: dict) -> None:
        async with _connect(self.path) as db:
            await _configure(db)
            await db.execute("""
              INSERT INTO workspace(path, indexed_at, files, classes, methods, fields)
              VALUES(?,?,?,?,?,?)
              ON CONFLICT(path) DO UPDATE SET
                indexed_at=excluded.indexed_at,
                files=excluded.files, classes=excluded.classes,
                methods=excluded.methods, fields=excluded.fields
            """, (path, time.time(),
                  stats.get("files"), stats.get("classes"),
                  stats.get("methods"), stats.get("fields")))
            await db.commit()

    async def last_workspace(self) -> str | None:
        async with _connect(self.path) as db:
            await _configure(db)
            async with db.execute(
                "SELECT path FROM workspace ORDER BY indexed_at DESC LIMIT 1"
            ) as cur:
                row = await cur.fetchone()
                return row[0] if row else None

    # ---------- historial ----------
    async def log(self, cmd: str, args: str, workspace: str | None) -> None:
        async with _connect(self.path) as db:
            await _configure(db)
            await db.execute(
                "INSERT INTO history(ts, cmd, args, workspace) VALUES(?,?,?,?)",
                (time.time(), cmd, args, workspace),
            )
            await db.commit()

    async def recent(self, limit: int = 20) -> list[tuple]:
        async with _connect(self.path) as db:
            await _configure(db)
            async with db.execute(
                "SELECT ts, cmd, args FROM history ORDER BY ts DESC LIMIT ?",
                (limit,),
            ) as cur:
                return await cur.fetchall()

    # ---------- alias ----------
    async def set_alias(self, name: str, target: str, kind: str | None = None) -> None:
        async with _connect(self.path) as db:
            await _configure(db)
            await db.execute("""
              INSERT INTO alias(name, target, kind, ts) VALUES(?,?,?,?)
              ON CONFLICT(name) DO UPDATE SET target=excluded.target,
                kind=excluded.kind, ts=excluded.ts
            """, (name, target, kind, time.time()))
            await db.commit()

    async def resolve_alias(self, name: str) -> str | None:
        async with _connect(self.path) as db:
            await _configure(db)
            async with db.execute(
                "SELECT target FROM alias WHERE name=?", (name,)
            ) as cur:
                row = await cur.fetchone()
            if not row:
                return None
            await db.execute(
                "UPDATE alias SET hits=hits+1 WHERE name=?", (name,)
            )
            await db.commit()
            return row[0]

    async def list_aliases(self) -> list[tuple]:
        async with _connect(self.path) as db:
            await _configure(db)
            async with db.execute(
                "SELECT name, target, kind, hits FROM alias ORDER BY hits DESC"
            ) as cur:
                return await cur.fetchall()

    # ---------- pinned ----------
    async def pin(self, symbol: str, kind: str | None, note: str | None) -> None:
        async with _connect(self.path) as db:
            await _configure(db)
            await db.execute("""
              INSERT INTO pinned(symbol, kind, note, ts) VALUES(?,?,?,?)
              ON CONFLICT(symbol) DO UPDATE SET kind=excluded.kind,
                note=excluded.note, ts=excluded.ts
            """, (symbol, kind, note, time.time()))
            await db.commit()

    async def pinned_list(self) -> list[tuple]:
        async with _connect(self.path) as db:
            await _configure(db)
            async with db.execute(
                "SELECT symbol, kind, note FROM pinned ORDER BY ts DESC"
            ) as cur:
                return await cur.fetchall()

    # ---------- feedback / afinidad ----------
    async def feedback(self, query: str, chosen_symbol: str) -> None:
        async with _connect(self.path) as db:
            await _configure(db)
            await db.execute(
                "INSERT INTO feedback(query, chosen_symbol, ts) VALUES(?,?,?)",
                (query, chosen_symbol, time.time()),
            )
            for term in tokenize_query(query):
                await db.execute("""
                  INSERT INTO affinity(query_term, symbol, score) VALUES(?,?,1.0)
                  ON CONFLICT(query_term, symbol) DO UPDATE SET
                    score = score + 1.0
                """, (term, chosen_symbol))
            await db.commit()

    async def affinity_for(self, query: str) -> dict[str, float]:
        terms = tokenize_query(query)
        if not terms:
            return {}
        q = ",".join("?" * len(terms))
        async with _connect(self.path) as db:
            await _configure(db)
            async with db.execute(
                f"SELECT symbol, SUM(score) AS s FROM affinity "
                f"WHERE query_term IN ({q}) "
                f"GROUP BY symbol HAVING s > 0 "
                f"ORDER BY s DESC LIMIT 20",
                terms,
            ) as cur:
                return {row[0]: row[1] for row in await cur.fetchall()}

