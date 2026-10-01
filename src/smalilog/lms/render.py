# smalilog/lms/render.py
"""Renderizado con Rich para el mini-LMS."""
from __future__ import annotations

from rich.console import Console
from rich.table import Table
from rich.tree import Tree
from rich.panel import Panel
from rich.syntax import Syntax

console = Console()


def print_tree(title: str, edges: list[dict]) -> None:
    tree = Tree(f"[bold]{title}[/bold]")
    for e in edges:
        tree.add(e.get("symbol") or e.get("to") or "?")
    console.print(tree)


def print_code(code: str, lexer: str = "asm") -> None:
    console.print(Panel(Syntax(code, lexer, line_numbers=True), expand=False))


def print_symbols(
    items: list[dict],
    title: str = "Resultados",
    show_score: bool = False,
) -> None:
    t = Table(title=title, show_lines=False)
    t.add_column("#", style="dim", width=3)
    t.add_column("Símbolo", style="cyan", overflow="fold")
    t.add_column("Tipo", style="magenta", width=10)
    if show_score:
        t.add_column("Score", style="green", width=7)
    for i, it in enumerate(items, 1):
        row = [
            str(i),
            it.get("symbol") or it.get("name") or "?",
            it.get("kind", ""),
        ]
        if show_score:
            row.append(f"{it.get('score', 0):.2f}")
        t.add_row(*row)
    console.print(t)


def print_table(
    columns: list[str],
    rows: list[tuple],
    title: str | None = None,
) -> None:
    """Tabla genérica (usada por mem alias-list / mem history)."""
    t = Table(title=title, show_lines=False)
    for c in columns:
        t.add_column(c)
    for r in rows:
        t.add_row(*(str(x) if x is not None else "" for x in r))
    console.print(t)

