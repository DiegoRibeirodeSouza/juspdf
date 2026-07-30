import subprocess
from pathlib import Path
from litisdoc.core.deps import check_dependency
from litisdoc.core.executor import run_subprocess

def create_booklet(input_pdf: Path, output_pdf: Path) -> None:
    """Usa bookletimposer para criar um livreto."""
    check_dependency("bookletimposer", "bookletimposer")
    
    # bookletimposer -b -o output input
    cmd = ["bookletimposer", "-b", "-o", str(output_pdf), str(input_pdf)]
    
    run_subprocess(
        cmd,
        success_msg=f"Livreto (Booklet) criado em {output_pdf.name}",
        error_msg="Falha ao criar livreto com bookletimposer."
    )
