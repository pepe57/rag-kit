"""Evaluation commands for RAG Facile CLI."""

import typer

from cli.commands.eval import search, sources

app = typer.Typer(
    help="Search and manage evaluation datasets",
    add_completion=False,
)

app.add_typer(search.app, name="search")
app.command(name="sources")(sources.list_sources)
