import typer
from pathlib import Path
from typing import List
from litisdoc.backends.dossier import create_dossier

app = typer.Typer(help="Comandos para criação de Dossiês padronizados em A4.")

@app.command("dossier")
def dossier(
    title: str = typer.Argument(..., help="Título principal do dossiê (ex: 'COMPROVANTES DE PIX')"),
    input_files: List[Path] = typer.Argument(..., help="Lista de arquivos (PDF, PNG, JPG) para processar", exists=True),
    output: Path = typer.Option(..., "--output", "-o", help="Caminho do arquivo PDF de saída final")
):
    """
    Gera um Dossiê A4. Cria uma capa limpa com o Título fornecido,
    centraliza e escala todos os PDFs e imagens anexos em páginas A4 brancas padronizadas,
    unindo-os num arquivo limpo e pronto para o PJe.
    """
    create_dossier(title, input_files, output)
