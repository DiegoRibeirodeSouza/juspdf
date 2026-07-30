import typer
from pathlib import Path
from juspdf.backends.poppler import extract_text, extract_images, get_info

app = typer.Typer(help="Comandos para extração e informações de PDFs (poppler-utils).")

@app.command("info")
def info(
    input_pdf: Path = typer.Argument(..., help="Arquivo PDF", exists=True, dir_okay=False)
):
    """
    Exibe informações estruturais de um PDF (metadados, número de páginas, etc).
    """
    get_info(input_pdf)

@app.command("extract-text")
def extract_text_cmd(
    input_pdf: Path = typer.Argument(..., help="Arquivo PDF de entrada", exists=True, dir_okay=False),
    output_txt: Path = typer.Argument(..., help="Arquivo de texto de saída"),
    layout: bool = typer.Option(False, "--layout", help="Tentar preservar o layout do documento")
):
    """
    Extrai todo o texto de um PDF.
    """
    extract_text(input_pdf, output_txt, preserve_layout=layout)

@app.command("extract-images")
def extract_images_cmd(
    input_pdf: Path = typer.Argument(..., help="Arquivo PDF de entrada", exists=True, dir_okay=False),
    output_dir: Path = typer.Argument(..., help="Diretório de saída para salvar as imagens")
):
    """
    Extrai todas as imagens embutidas no PDF.
    """
    extract_images(input_pdf, output_dir)
