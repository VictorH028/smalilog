"""Comando `smalilog lms q` — consultas combinables."""
from __future__ import annotations

import time
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from ._scanner import SmaliIndex
from ._query import Query
from ..config import settings

console = Console()
app = typer.Typer(help="Consultas sobre el código smali (motor local).")


def _cache_path() -> Path:
    from platformdirs import user_cache_dir
    d = Path(user_cache_dir("smalilog"))
    d.mkdir(parents=True, exist_ok=True)
    return d / "smali_index.pkl"


def _load_index(rebuild: bool = False) -> SmaliIndex:
    s = settings()
    root = Path(s.workspace) if s.workspace else Path.cwd()
    cache = _cache_path()

    if not rebuild and cache.exists():
        try:
            idx = SmaliIndex.load(cache)
            if Path(idx.root) == root:
                console.print(f"[dim]índice cargado de cache ({len(idx.methods)} métodos)[/dim]")
                return idx
        except Exception:  # noqa: BLE001
            pass

    console.print(f"[dim]escaneando {root}...[/dim]")
    idx = SmaliIndex(root)
    stats = idx.build(verbose=True)
    console.print(
        f"[dim]{stats['files']} archivos, {stats['classes']} clases, "
        f"{stats['methods']} métodos en {stats['seconds']}s[/dim]"
    )
    idx.save(cache)
    return idx


@app.command("scan")
def scan(
    rebuild: bool = typer.Option(False, "--rebuild", help="Ignora cache"),
):
    """Construye/actualiza el índice local."""
    idx = _load_index(rebuild=rebuild)
    console.print(f"[green]OK[/green] {idx.stats}")


@app.command("q")
def q(
    name: str = typer.Option(None, "--name", "-n", help="Glob: get*, *Title*"),
    returns_: str = typer.Option(None, "--returns", "-r", help="string, int, void..."),
    klass: str = typer.Option(None, "--class", "-c", help="Glob sobre la clase"),
    calls: str = typer.Option(None, "--calls", help="Patrón de invoke target"),
    const: str = typer.Option(None, "--const", help="Substring/regex en const-string"),
    opcode: str = typer.Option(None, "--opcode", help="Glob: if-*, return-*"),
    is_static: bool = typer.Option(False, "--static"),
    instance: bool = typer.Option(False, "--instance"),
    regex: bool = typer.Option(False, "--regex", help="--const es regex"),
    limit: int = typer.Option(100, "--limit", "-l"),
    rebuild: bool = typer.Option(False, "--rebuild"),
    show_body: bool = typer.Option(False, "--show", help="Muestra consts/invokes del match"),
):
    """Consulta combinable. Ej.:

      smalilog lms q --returns string --const http
      smalilog lms q --name 'is*' --returns boolean
      smalilog lms q --calls '*RemoteLogger*' --const SMALILOG_
    """
    idx = _load_index(rebuild=rebuild)

    query = Query()
    if name:      query.named(name)
    if returns_:  query.returning(returns_)
    if klass:     query.in_class(klass)
    if calls:     query.calling(calls)
    if const:     query.containing_string(const, regex=regex)
    if opcode:    query.using_opcode(opcode)
    if is_static: query.static()
    if instance:  query.instance()

    results = query.run(idx, limit=limit)
    console.print(f"[dim]{query.description} → {len(results)} matches[/dim]")
    if not results:
        return

    t = Table("#", "Símbolo", "Tipo", "Archivo", "Línea", show_lines=False)
    for i, m in enumerate(results, 1):
        t.add_row(
            str(i),
            m.symbol,
            m.return_type,
            m.file,
            str(m.line),
        )
    console.print(t)

    if show_body:
        for m in results:
            console.print(f"\n[bold cyan]{m.symbol}[/bold cyan]  [dim]({m.file}:{m.line})[/dim]")
            if m.const_strings:
                console.print("  [yellow]const-strings:[/yellow]")
                for s in m.const_strings[:20]:
                    console.print(f"    [dim]·[/dim] {s!r}")
            if m.invokes:
                console.print("  [yellow]invokes:[/yellow]")
                for s in m.invokes[:20]:
                    console.print(f"    [dim]·[/dim] {s}")

