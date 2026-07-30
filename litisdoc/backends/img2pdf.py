from pathlib import Path
from litisdoc.core.deps import check_dependency
from litisdoc.core.executor import run_subprocess
from typing import List

def convert_images_to_pdf(output_pdf: Path, images: List[Path]) -> None:
    """Converte lista de imagens para um PDF sem perdas, usando img2pdf."""
    check_dependency("img2pdf", "img2pdf")
    
    cmd = ["img2pdf", "-o", str(output_pdf)] + [str(img) for img in images]
    
    run_subprocess(
        cmd,
        success_msg=f"{len(images)} imagens convertidas e salvas em {output_pdf.name}",
        error_msg="Falha ao converter imagens para PDF com img2pdf."
    )
