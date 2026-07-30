import typer
from pathlib import Path
from typing import List
from juspdf.backends.img2pdf import convert_images_to_pdf

app = typer.Typer(help="Comandos para conversão (imagem -> PDF).")

@app.command("img2pdf")
def img2pdf(
    output_pdf: Path = typer.Argument(..., help="Arquivo PDF de saída"),
    images: List[Path] = typer.Argument(..., help="Lista de imagens de entrada (jpeg, png, jp2, etc)", exists=True, dir_okay=False)
):
    """
    Converte uma ou mais imagens em um PDF sem perdas, preservando os pixels exatos.
    """
    convert_images_to_pdf(output_pdf, images)
