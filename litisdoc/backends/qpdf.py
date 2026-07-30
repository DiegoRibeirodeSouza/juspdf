from pathlib import Path
from litisdoc.core.deps import check_dependency
from litisdoc.core.executor import run_subprocess

def merge_pdfs(output_pdf: Path, input_pdfs: list[Path]) -> None:
    """Usa QPDF para unir vários PDFs."""
    check_dependency("qpdf", "qpdf")
    
    # Ex: qpdf --empty --pages in1.pdf in2.pdf -- out.pdf
    cmd = ["qpdf", "--empty", "--pages"] + [str(p) for p in input_pdfs] + ["--", str(output_pdf)]
    
    run_subprocess(
        cmd,
        success_msg=f"{len(input_pdfs)} arquivos unidos com sucesso em {output_pdf.name}",
        error_msg="Ocorreu um erro ao tentar unir os PDFs com QPDF."
    )

def split_pdf(input_pdf: Path, output_dir: Path, pages: str = "") -> None:
    """Usa QPDF para extrair ou separar páginas. Se pages não for passado, separa cada página."""
    check_dependency("qpdf", "qpdf")
    
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
        
    if pages:
        # Extrair páginas específicas
        output_file = output_dir / f"{input_pdf.stem}_extraido.pdf"
        # qpdf in.pdf --pages in.pdf 1-5 -- out.pdf
        cmd = ["qpdf", str(input_pdf), "--pages", ".", pages, "--", str(output_file)]
        run_subprocess(
            cmd,
            success_msg=f"Páginas '{pages}' extraídas para {output_file.name}",
            error_msg="Falha ao extrair páginas com QPDF."
        )
    else:
        # Separar todas as páginas
        # qpdf in.pdf --split-pages out_dir/prefix_%d.pdf
        output_pattern = str(output_dir / f"{input_pdf.stem}_page-%d.pdf")
        cmd = ["qpdf", str(input_pdf), "--split-pages", output_pattern]
        run_subprocess(
            cmd,
            success_msg=f"Arquivo {input_pdf.name} separado em páginas individuais em {output_dir}/",
            error_msg="Falha ao separar páginas com QPDF."
        )

def rotate_pdf(input_pdf: Path, output_pdf: Path, angle: str) -> None:
    """Usa QPDF para rotacionar as páginas de um PDF."""
    check_dependency("qpdf", "qpdf")
    
    # qpdf in.pdf out.pdf --rotate=+90
    cmd = ["qpdf", str(input_pdf), str(output_pdf), f"--rotate={angle}"]
    
    run_subprocess(
        cmd,
        success_msg=f"PDF {input_pdf.name} rotacionado ({angle}) e salvo em {output_pdf.name}",
        error_msg="Falha ao rotacionar PDF com QPDF."
    )

def encrypt_pdf(input_pdf: Path, output_pdf: Path, password: str) -> None:
    """Usa QPDF para proteger o PDF com senha (256-bit AES)."""
    check_dependency("qpdf", "qpdf")
    # qpdf --encrypt pass pass 256 -- in.pdf out.pdf
    cmd = ["qpdf", "--encrypt", password, password, "256", "--", str(input_pdf), str(output_pdf)]
    run_subprocess(
        cmd,
        success_msg=f"PDF protegido com senha e salvo em {output_pdf.name}",
        error_msg="Falha ao proteger PDF com senha."
    )

def decrypt_pdf(input_pdf: Path, output_pdf: Path, password: str) -> None:
    """Usa QPDF para remover a senha do PDF."""
    check_dependency("qpdf", "qpdf")
    # qpdf --password=pass --decrypt in.pdf out.pdf
    cmd = ["qpdf", f"--password={password}", "--decrypt", str(input_pdf), str(output_pdf)]
    run_subprocess(
        cmd,
        success_msg=f"Senha removida. PDF salvo em {output_pdf.name}",
        error_msg="Falha ao descriptografar PDF (senha incorreta?)."
    )

def linearize_pdf(input_pdf: Path, output_pdf: Path) -> None:
    """Usa QPDF para otimizar o PDF para carregamento rápido na web (Linearização)."""
    check_dependency("qpdf", "qpdf")
    # qpdf --linearize in.pdf out.pdf
    cmd = ["qpdf", "--linearize", str(input_pdf), str(output_pdf)]
    run_subprocess(
        cmd,
        success_msg=f"PDF otimizado para web (linearizado) salvo em {output_pdf.name}",
        error_msg="Falha ao linearizar PDF."
    )
