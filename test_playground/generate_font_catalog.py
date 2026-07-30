import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image

def generate_catalog():
    # Registrar as fontes
    pdfmetrics.registerFont(TTFont('CMU-Reg', 'cm-unicode-0.7.0/cmunrm.ttf'))
    pdfmetrics.registerFont(TTFont('CMU-Bold', 'cm-unicode-0.7.0/cmunbx.ttf'))
    
    pdfmetrics.registerFont(TTFont('Pagella-Reg', 'pagella-regular.ttf'))
    pdfmetrics.registerFont(TTFont('Pagella-Bold', 'pagella-bold.ttf'))
    
    pdfmetrics.registerFont(TTFont('Lato-Reg', 'Lato-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('Lato-Bold', 'Lato-Bold.ttf'))

    c = canvas.Canvas("stamp_samples/Catalogo_Fontes.pdf", pagesize=A4)
    width, height = A4
    
    data_str = "Assinado eletronicamente em 29/07/2026 às 23:35"
    nome_str = "Diego Ribeiro de Souza - OAB/MG 211.002"

    fontes = [
        ("Computer Modern (CMU)", "CMU-Reg", "CMU-Bold"),
        ("TG Pagella (Palatino)", "Pagella-Reg", "Pagella-Bold"),
        ("Lato (Corporativo)", "Lato-Reg", "Lato-Bold")
    ]

    for title, reg, bold in fontes:
        # Título da página
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, f"Teste com Tipografia: {title}")
        c.setFont("Helvetica", 10)
        c.drawString(50, height - 70, "Estilo A com Tamanho 12.")

        # Gerar o carimbo Estilo A
        base_y = 100
        # Rubrica
        if os.path.exists('assinatura_limpa.png'):
            img = Image.open('assinatura_limpa.png')
            img_w, img_h = img.size
            aspect = img_h / float(img_w)
            target_w = 120
            target_h = target_w * aspect
            c.drawImage('assinatura_limpa.png', width/2 - target_w/2, base_y + 10, width=target_w, height=target_h, mask='auto')
        
        # Linha
        c.setLineWidth(0.5)
        c.line(width/2 - 120, base_y + 10, width/2 + 120, base_y + 10)
        
        # Textos
        c.setFont(bold, 12)
        c.drawCentredString(width/2, base_y - 5, nome_str)
        c.setFont(reg, 11)
        c.drawCentredString(width/2, base_y - 20, data_str)
        
        c.showPage()
        
    c.save()
    print("Catálogo gerado com sucesso!")

if __name__ == "__main__":
    generate_catalog()
