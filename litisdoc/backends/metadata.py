from pathlib import Path
from pypdf import PdfReader, PdfWriter
from rich.console import Console

console = Console()

def clear_metadata(input_pdf: Path, output_pdf: Path) -> None:
    """Remove metadados de um PDF usando pypdf."""
    try:
        reader = PdfReader(str(input_pdf))
        writer = PdfWriter()
        
        for page in reader.pages:
            writer.add_page(page)
            
        # Adiciona um dicionário vazio de metadados
        writer.add_metadata({})
        
        with open(str(output_pdf), "wb") as f:
            writer.write(f)
            
        console.print(f"[bold green]Sucesso:[/bold green] Metadados removidos. Salvo em {output_pdf.name}")
    except Exception as e:
        console.print(f"[bold red]Falha ao limpar metadados:[/bold red] {e}")
