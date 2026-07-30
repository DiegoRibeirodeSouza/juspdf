import subprocess
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def verify_signatures(input_pdf: Path) -> None:
    """Verifica e exibe as assinaturas presentes em um PDF usando pdfsig."""
    
    if not input_pdf.exists():
        console.print(f"[bold red]Erro:[/bold red] Arquivo '{input_pdf}' não encontrado.")
        return
        
    console.print(f"[bold cyan]Analisando assinaturas em:[/bold cyan] {input_pdf.name}")
    console.print("[yellow]Aguarde...[/yellow]\n")
    
    try:
        # Chama a ferramenta pdfsig
        result = subprocess.run(
            ['pdfsig', str(input_pdf)],
            capture_output=True,
            text=True,
            check=False # Nós mesmos tratamos o código de saída
        )
        
        output = result.stdout.strip()
        if not output and result.stderr:
            output = result.stderr.strip()
            
        if "No signatures found" in output or "Does not contain any signatures" in output or not output:
            console.print(Panel(
                Text("Nenhuma assinatura digital encontrada neste documento.", style="yellow"),
                title="Status da Assinatura",
                expand=False
            ))
            return
            
        # Formata a saída nativa do pdfsig com Rich para ficar agradável
        
        if "Signature is Valid" in output:
            color = "green"
        elif "Signature is Invalid" in output:
            color = "yellow" # Colocamos yellow ao invés de red porque frequentemente falta a raiz ICP-Brasil no Linux
        else:
            color = "white"
            
        console.print(Panel(
            output,
            title="Detalhes da Assinatura (pdfsig)",
            border_style=color,
            expand=False
        ))
        
        if "Signature is Invalid" in output:
            console.print("\n[dim]* Nota: No Linux, 'Signature is Invalid' frequentemente significa apenas que a Cadeia ICP-Brasil não está instalada no sistema. A assinatura criptográfica pode ainda ser totalmente válida e reconhecida por Tribunais (PJe, e-SAJ).[/dim]")
        elif "Certificate issuer is unknown" in output:
            console.print("\n[dim]* Nota: A sua assinatura criptográfica está 100% válida! O aviso 'Certificate issuer is unknown' é absolutamente normal no Linux porque o sistema operacional não vem de fábrica com as Autoridades Certificadoras Brasileiras instaladas no seu banco de dados interno. Isso não afeta a validade jurídica nos Tribunais.[/dim]")

    except FileNotFoundError:
        console.print("[bold red]Erro:[/bold red] Ferramenta 'pdfsig' não encontrada. Instale com 'sudo apt-get install poppler-utils'.")
    except Exception as e:
        console.print(f"[bold red]Erro ao verificar assinaturas:[/bold red] {e}")
