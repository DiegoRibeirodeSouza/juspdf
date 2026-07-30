from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

c = canvas.Canvas("stamp_samples/Mocks_Rodape_Minimalista.pdf", pagesize=A4)

def draw_mock_page(page_num, title, text_style, with_line=False):
    # Draw some fake document text
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, title)
    c.setFont("Helvetica", 11)
    for i in range(10):
        c.drawString(50, 750 - (i*20), "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Documento de teste.")
        
    # Y position for 3 cm from bottom edge
    y_pos = 3 * cm
    # Center X
    x_pos = A4[0] / 2
    
    text = "[ ICP-Brasil ] Documento assinado eletronicamente por Diego Ribeiro de Souza (OAB/MG 211.002) em 30/07/2026."
    
    c.setFont(text_style, 9)
    # drawCentredString draws the text centered at the given X coordinate
    c.drawCentredString(x_pos, y_pos, text)
    
    if with_line:
        # Draw a subtle separator line above the text
        c.setLineWidth(0.5)
        c.setStrokeColorRGB(0.5, 0.5, 0.5)
        text_width = c.stringWidth(text, text_style, 9)
        # Line from start of text to end of text, 8 points above baseline
        c.line(x_pos - (text_width/2), y_pos + 8, x_pos + (text_width/2), y_pos + 8)

    c.showPage()

# Variation 1: Normal
draw_mock_page(1, "Variação 1: Fonte Normal", "Helvetica")
# Variation 2: Itálico (passa mais sofisticação)
draw_mock_page(2, "Variação 2: Fonte em Itálico", "Helvetica-Oblique")
# Variation 3: Itálico + Linha divisória sutil
draw_mock_page(3, "Variação 3: Itálico com Linha Divisória", "Helvetica-Oblique", with_line=True)

c.save()
print("Mocks minimalistas gerados com sucesso!")
