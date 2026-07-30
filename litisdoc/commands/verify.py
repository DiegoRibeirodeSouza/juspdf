import typer
from pathlib import Path
from litisdoc.backends.verify import verify_signatures

app = typer.Typer()

@app.command("verify")
def verify_cmd(
    input: Path = typer.Argument(..., help="Arquivo PDF para verificar as assinaturas", exists=True, dir_okay=False)
):
    """Verifica e exibe informações sobre as assinaturas digitais contidas num PDF."""
    verify_signatures(input)
