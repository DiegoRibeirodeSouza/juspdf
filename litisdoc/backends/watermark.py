from pathlib import Path
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.colors import Color
import io
from rich.console import Console

console = Console()

def add_watermark(input_pdf: Path, output_pdf: Path, text: str) -> None:
    """Adiciona uma marca d'água ao PDF."""
    try:
        # 1. Gerar o PDF da marca d'água em memória
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=A4)
        c.setFont("Helvetica-Bold", 60)
        # Transparente vermelho/cinza
        c.setFillColor(Color(0.8, 0.2, 0.2, alpha=0.3))
        
        c.translate(inch, inch)
        c.rotate(45)
        # Tenta centralizar
        c.drawString(200, 100, text)
        c.save()
        packet.seek(0)
        
        watermark_pdf = PdfReader(packet)
        watermark_page = watermark_pdf.pages[0]
        
        # 2. Mesclar com o PDF original
        reader = PdfReader(str(input_pdf))
        writer = PdfWriter()
        
        for page in reader.pages:
            page.merge_page(watermark_page)
            writer.add_page(page)
            
        with open(str(output_pdf), "wb") as f:
            writer.write(f)
            
        console.print(f"[bold green]Sucesso:[/bold green] Marca d'água inserida. Salvo em {output_pdf.name}")
    except Exception as e:
        console.print(f"[bold red]Falha ao inserir marca d'água:[/bold red] {e}")

def add_pagination(input_pdf: Path, output_pdf: Path, prefix: str = "Fl. ", start_num: int = 1) -> None:
    """Adiciona números de página sequenciais no rodapé inferior direito."""
    try:
        reader = PdfReader(str(input_pdf))
        writer = PdfWriter()
        total_pages = len(reader.pages)
        
        for i, page in enumerate(reader.pages):
            current_num = start_num + i
            
            # Gera pdf com o número da página
            packet = io.BytesIO()
            c = canvas.Canvas(packet, pagesize=A4)
            c.setFont("Helvetica-Bold", 12)
            c.setFillColor(Color(0, 0, 0)) # Preto
            
            text = f"{prefix}{current_num:02d}"
            
            # Posição inferior direita (x=500, y=30)
            c.drawString(500, 30, text)
            c.save()
            packet.seek(0)
            
            number_pdf = PdfReader(packet)
            number_page = number_pdf.pages[0]
            
            page.merge_page(number_page)
            writer.add_page(page)
            
        with open(str(output_pdf), "wb") as f:
            writer.write(f)
            
        console.print(f"[bold green]Sucesso:[/bold green] Paginação inserida ({total_pages} páginas). Salvo em {output_pdf.name}")
    except Exception as e:
        console.print(f"[bold red]Falha ao inserir paginação:[/bold red] {e}")
