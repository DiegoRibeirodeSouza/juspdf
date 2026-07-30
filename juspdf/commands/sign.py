import typer
import questionary
from pathlib import Path
from typing_extensions import Annotated
from juspdf.backends.sign import sign_with_a3

app = typer.Typer(help="Assina um PDF digitalmente usando um Token A3")

@app.command("sign")
def sign(
    input_pdf: Annotated[Path, typer.Argument(help="PDF de origem", exists=True, file_okay=True)],
    output_pdf: Annotated[Path, typer.Argument(help="PDF de destino")],
):
    pin = questionary.password("Digite o PIN (senha) do seu Token A3:").ask()
    if not pin:
        typer.echo("Assinatura cancelada (PIN vazio).")
        raise typer.Exit()
        
    sign_with_a3(input_pdf, output_pdf, pin)
