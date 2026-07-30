import typer
from pathlib import Path
from litisdoc.backends.ocrmypdf import apply_ocr

app = typer.Typer(help="Comandos para OCR.")

@app.command("ocr")
def ocr(
    input_pdf: Path = typer.Argument(..., help="Arquivo PDF de entrada", exists=True, dir_okay=False),
    output_pdf: Path = typer.Argument(..., help="Arquivo PDF com texto pesquisável de saída"),
    lang: str = typer.Option("por", "--lang", "-l", help="Idioma do OCR (ex: por, eng)"),
    force: bool = typer.Option(False, "--force", "-f", help="Força a rasterização e o OCR em todas as páginas"),
    deskew: bool = typer.Option(False, "--deskew", "-d", help="Alinha (desentorta) páginas escaneadas tortas")
):
    """
    Aplica Reconhecimento Ótico de Caracteres (OCR) em um PDF, tornando seu texto pesquisável.
    """
    apply_ocr(input_pdf, output_pdf, lang=lang, force=force, deskew=deskew)
