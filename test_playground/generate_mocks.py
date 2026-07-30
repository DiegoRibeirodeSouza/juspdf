from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.graphics.shapes import Drawing, Rect
import qrcode

# Generate a real QR code image
qr = qrcode.QRCode(version=1, box_size=3, border=1)
qr.add_data('https://validar.iti.gov.br')
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save('qr_mock.png')

c = canvas.Canvas("stamp_samples/Mocks_Carimbos_JusPDF.pdf", pagesize=A4)

def draw_header(title):
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, title)
    c.setFont("Helvetica", 10)
    c.drawString(50, 780, "Demonstração visual do carimbo para Diego Ribeiro de Souza OAB/MG 211.002")

# --- Estilo 1: Clássico ---
draw_header("Estilo 1: Carimbo Clássico (Apenas Texto com Borda)")
# Draw box
c.setStrokeColor(HexColor("#000000"))
c.setLineWidth(1.5)
c.rect(50, 650, 300, 80)
# Draw text
c.setFont("Helvetica-Bold", 11)
c.drawString(60, 710, "Assinado digitalmente por")
c.setFont("Helvetica", 11)
c.drawString(60, 695, "DIEGO RIBEIRO DE SOUZA - OAB/MG 211.002")
c.setFont("Helvetica", 9)
c.drawString(60, 675, "Data: 2026-07-29 22:50:00 -03:00")
c.drawString(60, 660, "Tecnologia: JusPDF (ICP-Brasil)")
c.showPage()

# --- Estilo 2: Institucional ---
draw_header("Estilo 2: Institucional (Com Marca d'água/Logo)")
# Draw box
c.rect(50, 650, 300, 80)
# Draw watermark (simulated with a colored box or image if we had one)
c.drawImage("dummy_logo.png", 260, 660, width=80, height=60, mask='auto')
# Draw text
c.setFont("Helvetica-Bold", 11)
c.drawString(60, 710, "Assinado digitalmente por")
c.setFont("Helvetica", 11)
c.drawString(60, 695, "DIEGO RIBEIRO DE SOUZA - OAB/MG 211.002")
c.setFont("Helvetica", 9)
c.drawString(60, 675, "Data: 2026-07-29 22:50:00 -03:00")
c.drawString(60, 660, "Tecnologia: JusPDF (ICP-Brasil)")
c.showPage()

# --- Estilo 3: QR Code ---
draw_header("Estilo 3: Moderno com QR Code")
# Draw box
c.rect(50, 650, 300, 80)
# Draw QR
c.drawImage("qr_mock.png", 270, 655, width=70, height=70)
# Draw text
c.setFont("Helvetica-Bold", 11)
c.drawString(60, 710, "Assinado digitalmente por")
c.setFont("Helvetica", 11)
c.drawString(60, 695, "DIEGO RIBEIRO DE SOUZA - OAB/MG 211.002")
c.setFont("Helvetica", 9)
c.drawString(60, 675, "Data: 2026-07-29 22:50:00 -03:00")
c.drawString(60, 660, "Valide em: https://validar.iti.gov.br")
c.showPage()

c.save()
print("Mocks gerados!")
