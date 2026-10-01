# smalilog/lms/commands.py
"""Comandos Typer del mini-LMS."""
from __future__ import annotations

import asyncio
import datetime as dt
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from .config import settings
from .db import Memory
from .mcp_client import SmaliMcpClient
from .trainer import Trainer
from . import render
from .query import _cli_query as q, manifest

app = typer.Typer(
    help="Mini-LMS: búsqueda, memoria y consultas sobre smali.",
    no_args_is_help=True,
)

# Los subcomandos reales se registran una sola vez.
app.add_typer(q.app, name="local")
app.add_typer(manifest.app, name="manifest")

console = Console()
mem_app = typer.Typer(help="Memoria y entrenamiento.")
app.add_typer(mem_app, name="mem")


async def _open():
    s = settings()
    mem = Memory(s.resolved_db())
    await mem.init()
    mcp = SmaliMcpClient(s.server_cmd, s.server_args)
    await mcp.start()
    return s, mem, mcp


async def _ensure_indexed(mem: Memory, mcp: SmaliMcpClient, s) -> str | None:
    """Indexa el workspace configurado, o el CWD si no hay ninguno.

    El índice del server vive en memoria; como cada comando arranca un
    proceso nuevo, hay que reindexar antes de cada consulta.
    """
    from pathlib import Path

    if s.workspace:
        target = str(s.workspace)
    else:
        target = str(Path.cwd())
        console.print(
            f"[yellow]Sin workspace en config.toml; uso CWD: {target}[/yellow]"
        )

    console.print(f"[dim]Indexando {target}...[/dim]")
    stats = await mcp.call_tool("smali_index", {"directory": target})
    if isinstance(stats, dict):
        await mem.upsert_workspace(target, stats)
    console.print(f"[dim]  → {stats}[/dim]")
    return target

def run(coro):
    try:
        return asyncio.run(coro)
    except RuntimeError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=1)


def _ws(s) -> str | None:
    return str(s.workspace) if s.workspace else None


@app.command()
def index(path: Path = typer.Argument(None)):
    """Indexa un directorio smali (explícito)."""
    async def _do():
        s, mem, mcp = await _open()
        try:
            target = str(path or s.workspace or "")
            if not target:
                console.print("[red]Sin path ni workspace[/red]")
                return
            console.print(f"[dim]Indexando {target}...[/dim]")
            stats = await mcp.call_tool("smali_index", {"directory": target})
            if isinstance(stats, dict):
                await mem.upsert_workspace(target, stats)
            await mem.log("index", target, _ws(s) or target)
            console.print(f"[green]OK[/green] {stats}")
        finally:
            await mcp.stop()
    run(_do())


@app.command()
def find(
    query: str,
    limit: int = 15,
    pick: int = typer.Option(None, "--pick", help="Elegir # y registrar feedback"),
    no_index: bool = typer.Option(False, "--no-index", help="No reindexar antes"),
):
    """Busca símbolos (alias + afinidad aprendida)."""
    async def _do():
        s, mem, mcp = await _open()
        try:
            if not no_index:
                await _ensure_indexed(mem, mcp, s)
            t = Trainer(mem, mcp)
            items = await t.search(query, limit)
            if not items:
                console.print("[yellow]Sin resultados[/yellow]")
                return
            render.print_symbols(items, title=f"Búsqueda: {query}", show_score=True)
            if pick:
                if not 1 <= pick <= len(items):
                    console.print(f"[red]--pick fuera de rango (1..{len(items)})[/red]")
                    return
                chosen = items[pick - 1]
                sym = chosen.get("symbol") or chosen.get("name")
                await t.record_choice(query, sym)
                console.print(f"[green]Feedback:[/green] {sym}")
            await mem.log("find", query, _ws(s))
        finally:
            await mcp.stop()
    run(_do())


def _not_implemented(name: str) -> None:
    console.print(f"[yellow]{name}: aún no implementado[/yellow]")
    raise typer.Exit(code=2)



@app.command("def")
def definition(symbol: str):
    """Muestra la definición de un símbolo (clase)."""
    async def _do():
        s, mem, mcp = await _open()
        try:
            await _ensure_indexed(mem, mcp, s)
            res = await mcp.call_tool("smali_find_definition", {"symbol": symbol})
            if not res:
                console.print(f"[yellow]Sin definición para {symbol}[/yellow]")
                return
            import json
            console.print_json(json.dumps(res, default=str, ensure_ascii=False))
        finally:
            await mcp.stop()
    run(_do())


@app.command()
def xref(symbol: str):
    """Cross-reference summary de una clase."""
    async def _do():
        s, mem, mcp = await _open()
        try:
            await _ensure_indexed(mem, mcp, s)
            res = await mcp.call_tool("smali_xref_summary", {"class_name": symbol})
            if not res:
                console.print("[yellow]Sin resultados[/yellow]")
                return
            import json
            console.print_json(json.dumps(res, default=str, ensure_ascii=False))
        finally:
            await mcp.stop()
    run(_do())


@app.command()
def callgraph(symbol: str, method: str = typer.Option(..., "--method", "-m"),
              depth: int = 2):
    """Call graph de un método (placeholder: sin depth aún)."""
    async def _do():
        s, mem, mcp = await _open()
        try:
            await _ensure_indexed(mem, mcp, s)
            res = await mcp.call_tool("smali_call_graph", {
                "class_name": symbol, "method_name": method,
            })
            if not res:
                console.print("[yellow]Sin resultados[/yellow]")
                return
            import json
            console.print_json(json.dumps(res, default=str, ensure_ascii=False))
        finally:
            await mcp.stop()
    run(_do())


@app.command()
def typehier(klass: str):
    """Type hierarchy de una clase."""
    async def _do():
        s, mem, mcp = await _open()
        try:
            await _ensure_indexed(mem, mcp, s)
            res = await mcp.call_tool("smali_type_hierarchy", {"class_name": klass})
            if not res:
                console.print("[yellow]Sin resultados[/yellow]")
                return
            import json
            console.print_json(json.dumps(res, default=str, ensure_ascii=False))
        finally:
            await mcp.stop()
    run(_do())


@app.command()
def strings(query: str, limit: int = 30):
    """Busca en literales const-string."""
    async def _do():
        s, mem, mcp = await _open()
        try:
            await _ensure_indexed(mem, mcp, s)
            res = await mcp.call_tool("smali_search_strings", {
                "query": query, "max_results": limit,
            })
            if not res:
                console.print("[yellow]Sin resultados[/yellow]")
                return
            import json
            console.print_json(json.dumps(res, default=str, ensure_ascii=False))
        finally:
            await mcp.stop()
    run(_do())


@app.command()
def stats():
    """Estadísticas del índice actual."""
    async def _do():
        s, mem, mcp = await _open()
        try:
            await _ensure_indexed(mem, mcp, s)
            res = await mcp.call_tool("smali_get_stats", {})
            console.print_json(data=res)
        finally:
            await mcp.stop()
    run(_do())

# smalilog/lms/commands.py — añadir al final, antes de las mem_app

@app.command()
def returns(
    ret_type: str = typer.Argument(
        "Ljava/lang/String;",
        help="Tipo de retorno smali (p.ej. 'Ljava/lang/String;', 'I', 'V'). "
             "Atajos: 'string', 'int', 'void', 'boolean'.",
    ),
    pattern: str = typer.Option(
        "", "--pattern", "-p",
        help="Filtro opcional por nombre del método (substring).",
    ),
    limit: int = typer.Option(50, "--limit", "-n"),
    no_index: bool = typer.Option(False, "--no-index"),
):
    """Encuentra métodos cuyo tipo de retorno coincide.

    Ejemplos:
      smalilog lms returns                       # todos los que devuelven String
      smalilog lms returns string -p is
      smalilog lms returns I -p get              # todos los que devuelven int
      smalilog lms returns void -p init
    """
    # atajos cómodos
    ALIASES = {
        "string": "Ljava/lang/String;",
        "str":    "Ljava/lang/String;",
        "int":    "I",
        "long":   "J",
        "double": "D",
        "float":  "F",
        "boolean": "Z",
        "bool":   "Z",
        "void":   "V",
        "char":   "C",
        "byte":   "B",
        "short":  "S",
    }
    wanted = ALIASES.get(ret_type.lower(), ret_type)

    async def _do():
        s, mem, mcp = await _open()
        try:
            if not no_index:
                await _ensure_indexed(mem, mcp, s)

            # El server exige un pattern; si no nos dan uno, usamos
            # heurísticas para no traer lo mismo siempre.
            pattern_to_send = pattern or "L"   # la mayoría de firmas tienen 'L'
            console.print(
                f"[dim]Buscando métodos con retorno [/dim]"
                f"[cyan]{wanted}[/cyan][dim] (pattern='{pattern_to_send}')[/dim]"
            )

            raw = await mcp.call_tool(
                "smali_search_symbols", {"pattern": pattern_to_send}
            )
            if isinstance(raw, dict):
                items = raw.get("results") or raw.get("symbols") or raw.get("items") or []
            elif isinstance(raw, list):
                items = raw
            else:
                items = []

            # Filtro por firma: termina en ")<ret_type>"
            suffix = f"){wanted}"
            matched = []
            for it in items:
                sym = it.get("symbol") or it.get("name") or ""
                sig = it.get("signature") or ""
                # Acepta match contra "symbol" (que suele ser name+sig) o "signature"
                hay = f"{sym}{sig}"
                if suffix in hay:
                    matched.append(it)
                # caso void: en smali es 'V' pero algunos servers usan 'void'
                elif wanted == "V" and (")V" in hay or "->void" in hay):
                    matched.append(it)

            if not matched:
                console.print("[yellow]Sin resultados[/yellow]")
                console.print(
                    "[dim]Tip: el server devuelve hasta 100 símbolos por pattern. "
                    "Prueba con --pattern más específico o usa un atajo (string, int...).[/dim]"
                )
                return

            render.print_symbols(
                matched[:limit],
                title=f"Métodos que devuelven {wanted}  (pattern='{pattern_to_send}')",
            )
        finally:
            await mcp.stop()
    run(_do())


@mem_app.command("alias-set")
def alias_set(name: str, target: str, kind: str = typer.Option(None, "--kind")):
    """Define un alias (p.ej. 'login' → 'Lcom/x/A;->doLogin')."""
    async def _do():
        mem = Memory(settings().resolved_db())
        await mem.init()
        await mem.set_alias(name, target, kind)
        console.print(f"[green]Alias[/green] {name} → {target}")
    run(_do())


@mem_app.command("alias-list")
def alias_list():
    """Lista alias ordenados por hits."""
    async def _do():
        mem = Memory(settings().resolved_db())
        await mem.init()
        rows = await mem.list_aliases()
        render.print_table(
            ["Alias", "Target", "Kind", "Hits"], rows, title="Alias"
        )
    run(_do())


@mem_app.command("history")
def history(limit: int = 20):
    """Muestra el historial de comandos."""
    async def _do():
        mem = Memory(settings().resolved_db())
        await mem.init()
        rows = await mem.recent(limit)
        t = Table("Cuándo", "Cmd", "Args")
        for ts, cmd, args in rows:
            t.add_row(
                dt.datetime.fromtimestamp(ts).strftime("%H:%M:%S"),
                cmd,
                args or "",
            )
        console.print(t)
    run(_do())

