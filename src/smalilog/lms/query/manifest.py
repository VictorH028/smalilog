"""Consultas sobre AndroidManifest.xml."""
from pathlib import Path
import typer
from rich.console import Console
from rich.table import Table

from ._manifest import parse_manifest
from ...config import settings

console = Console()
app = typer.Typer(help="Consultas sobre AndroidManifest.xml.")


def _manifest_path() -> Path:
    s = settings()
    root = Path(s.workspace) if s.workspace else Path.cwd()
    p = root / "AndroidManifest.xml"
    if not p.exists():
        console.print(f"[red]No existe {p}[/red]")
        raise typer.Exit(1)
    return p


@app.command("manifest")
def manifest(kind: str = typer.Option(None, "--kind", "-k",
                                      help="activity|service|receiver|provider")):
    """Lista componentes del manifest."""
    m = parse_manifest(_manifest_path())
    console.print(f"[bold]package:[/bold] {m.package}")
    console.print(f"[bold]application:[/bold] {m.application_class}")

    comps = m.by_kind(kind) if kind else m.components
    t = Table("Kind", "Name", "Exported", "Intent actions")
    for c in comps:
        actions = ", ".join(
            a for ifl in c.intent_filters for a in ifl["actions"]
        ) or "-"
        t.add_row(c.kind, c.name, "yes" if c.exported else "no", actions[:60])
    console.print(t)

