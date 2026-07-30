import subprocess
from pathlib import Path
from juspdf.core.deps import check_dependency
from juspdf.core.executor import run_subprocess
from rich.console import Console

console = Console()

def scrub_pdf(input_pdf: Path, output_pdf: Path) -> None:
    """Usa pdfresurrect para remover histórico oculto e salvamentos incrementais de um PDF."""
    check_dependency("pdfresurrect", "pdfresurrect")
    
    # pdfresurrect -w <pdf> creates a scrubbed PDF (overwrites original if output not specified)
    # Mas queremos salvar no output_pdf, então fazemos uma cópia primeiro.
    import shutil
    shutil.copy2(input_pdf, output_pdf)
    
    cmd = ["pdfresurrect", "-w", str(output_pdf)]
    
    run_subprocess(
        cmd,
        success_msg=f"Histórico e versões ocultas removidas. Salvo em {output_pdf.name}",
        error_msg="Falha ao fazer scrub no PDF com pdfresurrect."
    )
