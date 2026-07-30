import typer
from pathlib import Path
from typing_extensions import Annotated
from juspdf.backends.search import search_in_pdfs

app = typer.Typer(help="Busca texto dentro de PDFs em um diretório")

@app.command("search")
def search(
    target_dir: Annotated[Path, typer.Argument(help="Diretório contendo os PDFs", exists=True, dir_okay=True)],
    query: Annotated[str, typer.Argument(help="Palavra-chave ou Expressão Regular para buscar")]
):
    search_in_pdfs(target_dir, query)
