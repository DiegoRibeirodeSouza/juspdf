from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor

c = canvas.Canvas("stamp_samples/Mocks_Inovadores.pdf", pagesize=A4)
width, height = A4

def draw_fake_text(title):
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, title)
    c.setFont("Helvetica", 11)
    for i in range(25):
        c.drawString(50, 750 - (i*20), "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Documento de teste da justiça.")

# --- Estilo 4: Tarja Lateral (Estilo PJe) ---
draw_fake_text("Estilo 4: Tarja Lateral Margem Direita (Estilo Tribunal)")
c.saveState()
# Translate to right edge, middle of page
c.translate(width - 20, height / 2)
c.rotate(90) # Rotate text vertically
c.setFont("Helvetica", 9)
c.setFillColor(HexColor("#444444"))
text = "Assinado eletronicamente por DIEGO RIBEIRO DE SOUZA (OAB/MG 211.002) - ICP-Brasil"
c.drawCentredString(0, 0, text)
c.restoreState()
c.showPage()

# --- Estilo 5: Selo (Badge) no Canto Superior Direito ---
draw_fake_text("Estilo 5: Selo (Badge) Canto Superior Direito")
# Draw a small pill/badge at top right
badge_w = 220
badge_h = 35
badge_x = width - badge_w - 30
badge_y = height - badge_h - 30

c.setStrokeColor(HexColor("#003366")) # Dark blue border
c.setLineWidth(1)
c.setFillColor(HexColor("#F0F8FF")) # AliceBlue bg
c.roundRect(badge_x, badge_y, badge_w, badge_h, radius=10, fill=1, stroke=1)

c.setFillColor(HexColor("#000000"))
c.setFont("Helvetica-Bold", 8)
c.drawString(badge_x + 10, badge_y + 20, "ASSINADO DIGITALMENTE - ICP-BRASIL")
c.setFont("Helvetica", 8)
c.drawString(badge_x + 10, badge_y + 8, "DIEGO RIBEIRO DE SOUZA - OAB/MG 211.002")
c.showPage()

# --- Estilo 6: Marca D'água Diagonal ---
draw_fake_text("Estilo 6: Marca D'água Transparente Diagonal")
c.saveState()
c.translate(width / 2, height / 2)
c.rotate(45)
c.setFont("Helvetica-Bold", 24)
c.setFillColorRGB(0.8, 0.8, 0.8, alpha=0.5) # Light gray with transparency
c.drawCentredString(0, 15, "ASSINADO DIGITALMENTE")
c.setFont("Helvetica", 18)
c.drawCentredString(0, -15, "DIEGO RIBEIRO DE SOUZA - OAB/MG 211.002")
c.restoreState()
c.showPage()

c.save()
print("Mocks inovadores gerados!")
