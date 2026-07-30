import subprocess
import typer
from rich.console import Console

console = Console()

def run_subprocess(cmd: list[str], success_msg: str = "", error_msg: str = "Falha ao executar comando externa.") -> str:
    """Executa um comando de sistema (subprocess) de forma isolada."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        if success_msg:
            console.print(f"[bold green]Sucesso:[/bold green] {success_msg}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Erro:[/bold red] {error_msg}")
        if e.stderr:
            console.print(f"[red]Detalhes do erro do executável:[/red]\n{e.stderr.strip()}")
        elif e.stdout:
            console.print(f"[red]Detalhes da saída:[/red]\n{e.stdout.strip()}")
        raise typer.Exit(code=1)
    except FileNotFoundError:
        console.print(f"[bold red]Erro:[/bold red] Executável '{cmd[0]}' não encontrado (mesmo após check).")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]Erro inesperado:[/bold red] {str(e)}")
        raise typer.Exit(code=1)
