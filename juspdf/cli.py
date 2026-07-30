import typer
from rich.console import Console
from juspdf.tui import run_tui

from juspdf.commands import compress, split_merge, rotate, extract, ocr, convert, search, resurrect, impose, sign, verify, dossier

app = typer.Typer(
    help="juspdf - Canivete suíço para manipulação de PDFs no Linux.",
    no_args_is_help=False
)

console = Console()

# Registrando os subcomandos na raiz do app para acesso direto (ex: juspdf merge)
app.registered_commands += compress.app.registered_commands
app.registered_commands += split_merge.app.registered_commands
app.registered_commands += rotate.app.registered_commands
app.registered_commands += extract.app.registered_commands
app.registered_commands += ocr.app.registered_commands
app.registered_commands += convert.app.registered_commands
app.registered_commands += search.app.registered_commands
app.registered_commands += resurrect.app.registered_commands
app.registered_commands += impose.app.registered_commands
app.registered_commands += sign.app.registered_commands
app.registered_commands += verify.app.registered_commands
app.registered_commands += dossier.app.registered_commands

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        run_tui()
