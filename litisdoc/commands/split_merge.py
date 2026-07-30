import typer
from pathlib import Path
from typing import List
from litisdoc.backends.qpdf import merge_pdfs, split_pdf

app = typer.Typer(help="Comandos para unir ou separar PDFs.")

@app.command("merge")
def merge(
    output_pdf: Path = typer.Argument(..., help="Caminho para salvar o PDF unido"),
    input_pdfs: List[Path] = typer.Argument(..., help="Lista de PDFs de entrada", exists=True, dir_okay=False)
):
    """
    Une múltiplos arquivos PDF em um único arquivo utilizando QPDF.
    """
    merge_pdfs(output_pdf, input_pdfs)

@app.command("split")
def split(
    input_pdf: Path = typer.Argument(..., help="Arquivo PDF para separar/extrair páginas", exists=True, dir_okay=False),
    output_dir: Path = typer.Argument(..., help="Diretório de saída para salvar os PDFs"),
    pages: str = typer.Option("", "--pages", "-p", help="Range de páginas para extrair (ex: '1-5,8'). Se não especificado, separa todas as páginas.")
):
    """
    Separa um arquivo PDF em múltiplas páginas ou extrai um intervalo específico.
    """
    split_pdf(input_pdf, output_dir, pages)
