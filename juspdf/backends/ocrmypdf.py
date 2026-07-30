from pathlib import Path
from juspdf.core.deps import check_dependency
from juspdf.core.executor import run_subprocess

def apply_ocr(input_pdf: Path, output_pdf: Path, lang: str = "por", force: bool = False, deskew: bool = False) -> None:
    """Aplica OCR em um PDF usando ocrmypdf."""
    check_dependency("ocrmypdf", "ocrmypdf tesseract-ocr tesseract-ocr-por")
    
    cmd = ["ocrmypdf", "-l", lang]
    
    if force:
        cmd.append("--force-ocr") # Força OCR rasterizando todas as páginas
    else:
        cmd.append("--skip-text") # Ignora páginas que já têm texto
        
    if deskew:
        cmd.append("--deskew")
        
    cmd.extend([str(input_pdf), str(output_pdf)])
    
    run_subprocess(
        cmd,
        success_msg=f"OCR aplicado em {input_pdf.name} e salvo em {output_pdf.name}",
        error_msg="Falha ao aplicar OCR com ocrmypdf."
    )

def convert_to_pdfa(input_pdf: Path, output_pdf: Path) -> None:
    """Usa ocrmypdf para converter o PDF para o formato PDF/A (bypassa OCR)."""
    check_dependency("ocrmypdf", "ocrmypdf")
    
    cmd = [
        "ocrmypdf", 
        "--skip-text",           # Pula OCR (mais rápido)
        "--tesseract-timeout", "0",
        str(input_pdf), 
        str(output_pdf)
    ]
    
    run_subprocess(
        cmd,
        success_msg=f"Convertido para PDF/A e salvo em {output_pdf.name}",
        error_msg="Falha ao converter para PDF/A com ocrmypdf."
    )
