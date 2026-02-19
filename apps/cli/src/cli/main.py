from importlib.metadata import version as get_version
from typing import Optional

import click
import typer
from rich.console import Console

from cli.commands import (
    collections,
    config,
    generate_dataset,
    setup,
    uninstall,
    upgrade,
)


console = Console()

BANNER = """[magenta]
 ██████╗  █████╗  ██████╗     ███████╗ █████╗  ██████╗██╗██╗     ███████╗
 ██╔══██╗██╔══██╗██╔════╝     ██╔════╝██╔══██╗██╔════╝██║██║     ██╔════╝
 ██████╔╝███████║██║  ███╗    █████╗  ███████║██║     ██║██║     █████╗
 ██╔══██╗██╔══██║██║   ██║    ██╔══╝  ██╔══██║██║     ██║██║     ██╔══╝
 ██║  ██║██║  ██║╚██████╔╝    ██║     ██║  ██║╚██████╗██║███████╗███████╗
 ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝     ╚═╝     ╚═╝  ╚═╝ ╚═════╝╚═╝╚══════╝╚══════╝
[/magenta]"""


# Commands in the Getting Started panel sort before Advanced Tools commands,
# then alphabetically within each panel.
_GETTING_STARTED_COMMANDS = {"setup", "uninstall", "upgrade"}


class PanelAlphabeticalGroup(typer.core.TyperGroup):
    """Sort commands by panel (Getting Started first), then alphabetically within each panel."""

    def list_commands(self, ctx: click.Context) -> list[str]:
        all_names = list(super().list_commands(ctx))
        return sorted(
            all_names,
            key=lambda n: (0 if n in _GETTING_STARTED_COMMANDS else 1, n),
        )


app = typer.Typer(
    cls=PanelAlphabeticalGroup,
    add_completion=False,
    invoke_without_command=True,
    no_args_is_help=True,
    help="RAG Facile CLI - Build RAG applications for the French government",
)


@app.callback()
def main_callback(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the CLI version and exit",
    ),
) -> None:
    """RAG Facile CLI - Build RAG applications for the French government."""
    try:
        console.print(BANNER)
    except Exception:
        # Skip banner if terminal doesn't support Unicode (e.g., Git Bash on Windows with cp1252)
        # Catching all exceptions since rich may wrap UnicodeEncodeError
        pass

    if version:
        cli_version = get_version("rag-facile-cli")
        console.print(f"[cyan]rag-facile v{cli_version}[/cyan]")
        raise typer.Exit()


# Register Getting Started commands first so their panel renders at the top
app.command(
    name="setup", help="Setup a new workspace", rich_help_panel="🚀 Getting Started"
)(setup.run)

app.command(
    name="uninstall",
    help="Remove the RAG Facile CLI (--all for toolchain too)",
    rich_help_panel="🚀 Getting Started",
)(uninstall.run)

app.command(
    name="upgrade",
    help="Upgrade to the latest version",
    rich_help_panel="🚀 Getting Started",
)(upgrade.run)

# Advanced Tools — registered after Getting Started so their panel renders below

# Collections command group
collections_app = typer.Typer(
    name="collections",
    help="Discover and manage Albert API collections",
    no_args_is_help=True,
)
collections_app.command("list", help="List accessible collections")(
    collections.list_collections
)
app.add_typer(collections_app, name="collections", rich_help_panel="🔧 Advanced Tools")

# Config command group
config_app = typer.Typer(
    name="config",
    help="Manage RAG configuration",
    no_args_is_help=True,
)
config_app.command("show", help="Display current configuration")(config.show)
config_app.command("validate", help="Validate configuration file")(config.validate)
config_app.command("set", help="Set configuration value")(config.set_value)
config_app.add_typer(
    config.preset(), name="preset", help="Manage configuration presets"
)
app.add_typer(config_app, name="config", rich_help_panel="🔧 Advanced Tools")

app.command(
    name="generate-dataset",
    help="Generate synthetic Q/A evaluation dataset from documents",
    rich_help_panel="🔧 Advanced Tools",
)(generate_dataset.run)


if __name__ == "__main__":
    app()
