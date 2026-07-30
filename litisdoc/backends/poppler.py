from pathlib import Path
from litisdoc.core.deps import check_dependency
from litisdoc.core.executor import run_subprocess
from rich.console import Console

console = Console()

def extract_text(input_pdf: Path, output_txt: Path, preserve_layout: bool = False) -> None:
    """Extrai texto de um PDF usando pdftotext (poppler)."""
    check_dependency("pdftotext", "poppler-utils")
    
    cmd = ["pdftotext"]
    if preserve_layout:
        cmd.append("-layout")
        
    cmd.extend([str(input_pdf), str(output_txt)])
    
    run_subprocess(
        cmd,
        success_msg=f"Texto extraído de {input_pdf.name} para {output_txt.name}",
        error_msg="Falha ao extrair texto com pdftotext."
    )

def extract_images(input_pdf: Path, output_dir: Path) -> None:
    """Extrai todas as imagens de um PDF usando pdfimages (poppler)."""
    check_dependency("pdfimages", "poppler-utils")
    
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
        
    # pdfimages -all in.pdf out_dir/prefix
    prefix = output_dir / input_pdf.stem
    cmd = ["pdfimages", "-all", str(input_pdf), str(prefix)]
    
    run_subprocess(
        cmd,
        success_msg=f"Imagens extraídas de {input_pdf.name} para a pasta {output_dir}/",
        error_msg="Falha ao extrair imagens com pdfimages."
    )

def get_info(input_pdf: Path) -> None:
    """Exibe informações do PDF usando pdfinfo (poppler)."""
    check_dependency("pdfinfo", "poppler-utils")
    check_dependency("pdffonts", "poppler-utils")
    
    cmd_info = ["pdfinfo", str(input_pdf)]
    cmd_fonts = ["pdffonts", str(input_pdf)]
    
    # Run sem suprimir output, queremos ver
    output_info = run_subprocess(
        cmd_info,
        error_msg="Falha ao obter informações com pdfinfo."
    )
    
    output_fonts = run_subprocess(
        cmd_fonts,
        error_msg="Falha ao obter fontes com pdffonts."
    )
    
    console.print(f"[bold cyan]\n--- Informações de {input_pdf.name} ---[/bold cyan]")
    console.print(output_info)
    console.print(f"[bold cyan]--- Fontes de {input_pdf.name} ---[/bold cyan]")
    console.print(output_fonts)

def render_to_images(input_pdf: Path, output_dir: Path) -> None:
    """Renderiza cada página do PDF como imagem (JPEG) usando pdftocairo."""
    check_dependency("pdftocairo", "poppler-utils")
    
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
        
    prefix = output_dir / "pagina"
    cmd = ["pdftocairo", "-jpeg", str(input_pdf), str(prefix)]
    
    run_subprocess(
        cmd,
        success_msg=f"Páginas renderizadas para {output_dir}/",
        error_msg="Falha ao renderizar PDF para imagens."
    )
