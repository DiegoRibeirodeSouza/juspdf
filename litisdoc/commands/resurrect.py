import typer
from pathlib import Path
from typing_extensions import Annotated
from litisdoc.backends.resurrect import scrub_pdf

app = typer.Typer(help="Remove histórico oculto e salvamentos incrementais do PDF (Scrub)")

@app.command("scrub")
def resurrect(
    input_pdf: Annotated[Path, typer.Argument(help="PDF de origem", exists=True, file_okay=True)],
    output_pdf: Annotated[Path, typer.Argument(help="PDF de destino")],
):
    scrub_pdf(input_pdf, output_pdf)
