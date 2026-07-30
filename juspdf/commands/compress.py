import typer
from pathlib import Path
from juspdf.backends.ghostscript import compress_pdf

app = typer.Typer(help="Comandos para compressão de PDFs.")

@app.command("compress")
def compress(
    input_pdf: Path = typer.Argument(..., help="Caminho para o arquivo PDF de entrada", exists=True, dir_okay=False),
    output_pdf: Path = typer.Argument(..., help="Caminho para salvar o PDF comprimido"),
    level: str = typer.Option("ebook", "--level", "-l", help="Nível de compressão: screen (baixa res), ebook (média res), printer (alta res), prepress (altíssima)")
):
    """
    Comprime um arquivo PDF utilizando Ghostscript.
    """
    compress_pdf(input_pdf, output_pdf, level)
