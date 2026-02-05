from importlib.metadata import version as get_version

import typer
from rich.console import Console

from cli.commands import init, generate_dataset

console = Console()

BANNER = """[magenta]
 ██████╗  █████╗  ██████╗     ███████╗ █████╗  ██████╗██╗██╗     ███████╗
 ██╔══██╗██╔══██╗██╔════╝     ██╔════╝██╔══██╗██╔════╝██║██║     ██╔════╝
 ██████╔╝███████║██║  ███╗    █████╗  ███████║██║     ██║██║     █████╗
 ██╔══██╗██╔══██║██║   ██║    ██╔══╝  ██╔══██║██║     ██║██║     ██╔══╝
 ██║  ██║██║  ██║╚██████╔╝    ██║     ██║  ██║╚██████╗██║███████╗███████╗
 ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝     ╚═╝     ╚═╝  ╚═╝ ╚═════╝╚═╝╚══════╝╚══════╝
[/magenta]"""

# Print banner on every invocation
console.print(BANNER)

app = typer.Typer(
    add_completion=False,
    invoke_without_command=True,
    no_args_is_help=True,
    help="RAG Facile CLI - Build RAG applications for the French government",
)

app.add_typer(init.app, name="init", help="Initialize a new workspace")
app.command(
    name="generate-dataset",
    help="Generate synthetic Q/A evaluation dataset from documents",
)(generate_dataset.run)


@app.command()
def version():
    """Show the CLI version."""
    print(f"rag-facile v{get_version('rag-facile-cli')}")


if __name__ == "__main__":
    app()
