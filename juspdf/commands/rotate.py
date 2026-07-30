import typer
from pathlib import Path
from juspdf.backends.qpdf import rotate_pdf

app = typer.Typer(help="Comando para rotacionar PDFs.")

@app.command("rotate")
def rotate(
    input_pdf: Path = typer.Argument(..., help="Arquivo PDF de entrada", exists=True, dir_okay=False),
    output_pdf: Path = typer.Argument(..., help="Arquivo PDF de saída"),
    angle: str = typer.Option("+90", "--angle", "-a", help="Ângulo de rotação (ex: +90, -90, +180)")
):
    """
    Rotaciona as páginas de um arquivo PDF utilizando QPDF.
    """
    rotate_pdf(input_pdf, output_pdf, angle)
