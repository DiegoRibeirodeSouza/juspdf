import shutil
import typer
from rich.console import Console

console = Console()

def check_dependency(binary_name: str, pkg_name: str) -> None:
    """Verifica se o binário existe no PATH."""
    if not shutil.which(binary_name):
        console.print(f"[bold red]Erro:[/bold red] O executável '{binary_name}' não foi encontrado no sistema.")
        console.print(f"Por favor, instale-o com: [bold yellow]sudo apt install {pkg_name}[/bold yellow]")
        raise typer.Exit(code=1)
