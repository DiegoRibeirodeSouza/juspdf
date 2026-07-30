import typer
from pathlib import Path
from typing_extensions import Annotated
from juspdf.backends.imposition import create_booklet

app = typer.Typer(help="Cria imposição de páginas para formato livreto")

@app.command("impose")
def impose(
    input_pdf: Annotated[Path, typer.Argument(help="PDF de origem", exists=True, file_okay=True)],
    output_pdf: Annotated[Path, typer.Argument(help="PDF de destino")],
):
    create_booklet(input_pdf, output_pdf)
