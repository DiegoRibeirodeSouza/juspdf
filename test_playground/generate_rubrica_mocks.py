from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import datetime

# Registrar a fonte cursiva
try:
    pdfmetrics.registerFont(TTFont('Rubrica', 'GreatVibes-Regular.ttf'))
    has_font = True
except Exception as e:
    has_font = False
    print("Erro ao carregar fonte:", e)

c = canvas.Canvas("stamp_samples/Mocks_Rubrica.pdf", pagesize=A4)
width, height = A4

def draw_fake_text(title):
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(HexColor("#000000"))
    c.drawString(50, 800, title)
    c.setFont("Helvetica", 11)
    for i in range(20):
        c.drawString(50, 750 - (i*20), "Lorem ipsum dolor sit amet, petição judicial demonstrativa.")

# Dados da assinatura
nome = "Diego R. de Souza" # Rubrica mais curta
data_str = "Assinado eletronicamente em 29/07/2026 às 23:10"
tech_str = "Tecnologia: ICP-Brasil / PyHanko"

font_name = "Rubrica" if has_font else "Helvetica-Oblique"

# --- Estilo 7: Rubrica Central (Minimalista) ---
draw_fake_text("Estilo 7: Rubrica Central Simples")
# Posição: Centro, fim da página
c.setFillColor(HexColor("#000000"))
c.setFont(font_name, 36)
c.drawCentredString(width/2, 100, nome)
c.setFont("Helvetica", 8)
c.drawCentredString(width/2, 80, data_str)
c.drawCentredString(width/2, 68, tech_str)
c.showPage()

# --- Estilo 8: Rubrica sobre Linha de Assinatura ---
draw_fake_text("Estilo 8: Rubrica sobre Linha de Assinatura")
c.setFillColor(HexColor("#000000"))
c.setFont(font_name, 36)
# Text above line
c.drawCentredString(width/2, 110, nome)
# Line
c.setLineWidth(1)
c.line(width/2 - 100, 105, width/2 + 100, 105)
# Text below line
c.setFont("Helvetica", 8)
c.drawCentredString(width/2, 90, data_str)
c.drawCentredString(width/2, 78, tech_str)
c.showPage()

# --- Estilo 9: Rubrica em Azul-Caneta Escuro ---
draw_fake_text("Estilo 9: Rubrica em Tinta Azul (Simulação de Caneta)")
c.setFillColor(HexColor("#000080")) # Navy blue
c.setFont(font_name, 38)
c.drawCentredString(width/2, 110, nome)
c.setStrokeColor(HexColor("#000000"))
c.setLineWidth(0.5)
c.line(width/2 - 100, 105, width/2 + 100, 105)
c.setFillColor(HexColor("#000000"))
c.setFont("Helvetica", 8)
c.drawCentredString(width/2, 90, data_str)
c.drawCentredString(width/2, 78, tech_str)
c.showPage()

# --- Estilo 10: Rubrica Lateral (Nome de um lado, Dados do outro) ---
draw_fake_text("Estilo 10: Rubrica Lateral (Elegante Corporativo)")
c.setFillColor(HexColor("#000000"))
c.setLineWidth(1)
# Draw a subtle border box at the bottom right
box_w = 320
box_h = 70
box_x = width - box_w - 40
box_y = 50

# c.rect(box_x, box_y, box_w, box_h)
# Divide line in the middle of the box
c.line(box_x + 140, box_y + 10, box_x + 140, box_y + box_h - 10)

# Left side: Rubrica (Blue)
c.setFillColor(HexColor("#000080"))
c.setFont(font_name, 28)
c.drawString(box_x + 10, box_y + 25, nome)

# Right side: Data (Black)
c.setFillColor(HexColor("#000000"))
c.setFont("Helvetica-Bold", 8)
c.drawString(box_x + 155, box_y + 45, "Documento assinado digitalmente")
c.setFont("Helvetica", 8)
c.drawString(box_x + 155, box_y + 32, "Diego Ribeiro de Souza (OAB/MG 211.002)")
c.drawString(box_x + 155, box_y + 20, data_str)
c.drawString(box_x + 155, box_y + 8, tech_str)

c.showPage()

c.save()
print("Mocks de rubrica gerados com fonte cursiva!")
