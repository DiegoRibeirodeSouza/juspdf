from pathlib import Path
from litisdoc.core.deps import check_dependency
from litisdoc.core.executor import run_subprocess

def compress_pdf(input_pdf: Path, output_pdf: Path, level: str) -> None:
    """Usa Ghostscript para comprimir um PDF."""
    check_dependency("gs", "ghostscript")
    
    cmd = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS=/{level}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_pdf}",
        str(input_pdf)
    ]
    
    run_subprocess(
        cmd, 
        success_msg=f"PDF {input_pdf.name} comprimido com sucesso para {output_pdf.name} (Nível: {level})",
        error_msg=f"Ocorreu um erro ao tentar comprimir {input_pdf.name} com Ghostscript."
    )
