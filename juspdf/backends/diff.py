from pathlib import Path
from juspdf.core.deps import check_dependency
from juspdf.core.executor import run_subprocess

def compare_pdfs(pdf1: Path, pdf2: Path, output_pdf: Path) -> None:
    """Usa diff-pdf-wx para comparar dois PDFs visualmente."""
    check_dependency("diff-pdf-wx", "diff-pdf-wx")
    
    # diff-pdf-wx --output-diff=out.pdf file1.pdf file2.pdf
    cmd = ["diff-pdf-wx", f"--output-diff={output_pdf}", str(pdf1), str(pdf2)]
    
    # diff-pdf-wx retorna código 1 se houver diferenças, o que é esperado!
    # run_subprocess lança exceção em códigos diferentes de zero.
    # Então vamos fazer um wrapper manual aqui ou ignorar exit codes.
    import subprocess
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode not in [0, 1]:
            raise Exception(result.stderr)
            
        from rich.console import Console
        console = Console()
        console.print(f"[bold green]Sucesso:[/bold green] Comparação gerada em {output_pdf.name}")
    except Exception as e:
        raise Exception(f"Falha ao rodar diff-pdf-wx: {e}")
