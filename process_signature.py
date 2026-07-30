import sys
from PIL import Image, ImageChops

def clean_signature(input_path, output_path):
    # Abrir e converter para RGBA
    try:
        img = Image.open(input_path).convert("RGBA")
    except Exception as e:
        print(f"Erro ao abrir {input_path}: {e}")
        return False
        
    datas = img.getdata()
    newData = []
    # Tolerância para o branco
    for item in datas:
        # Pega pixels que são muito claros (perto do branco) e os torna transparentes
        if item[0] > 200 and item[1] > 200 and item[2] > 200:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    
    img.putdata(newData)
    
    # Recortar o excesso de borda (bounding box da parte não transparente)
    bg = Image.new(img.mode, img.size, (255,255,255,0))
    diff = ImageChops.difference(img, bg)
    bbox = diff.getbbox()
    if bbox:
        img = img.crop(bbox)
        
    img.save(output_path, "PNG")
    print(f"Assinatura processada salva em {output_path}")
    return True

if clean_signature("../assinatura.png", "assinatura_limpa.png"):
    # Gerar Mocks com ReportLab
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.colors import HexColor
    from reportlab.lib.units import cm
    
    c = canvas.Canvas("stamp_samples/Mocks_Assinatura_Real.pdf", pagesize=A4)
    width, height = A4
    
    img_path = "assinatura_limpa.png"
    
    # O tamanho natural da imagem pode variar, vamos forçar uma altura e manter a proporção
    # Altura alvo: 50 pontos (cerca de 1.7 cm)
    from reportlab.lib.utils import ImageReader
    ir = ImageReader(img_path)
    img_w, img_h = ir.getSize()
    target_h = 45
    target_w = (img_w / img_h) * target_h
    
    def draw_fake_text(title):
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(HexColor("#000000"))
        c.drawString(50, 800, title)
        c.setFont("Helvetica", 11)
        for i in range(15):
            c.drawString(50, 750 - (i*20), "Lorem ipsum dolor sit amet, petição judicial demonstrativa.")

    data_str = "Assinado eletronicamente em 29/07/2026 às 23:35"
    tech_str = "Tecnologia: ICP-Brasil / LitisDoc"
    nome_str = "Diego Ribeiro de Souza - OAB/MG 211.002"

    # --- Estilo A: Centralizada com Linha ---
    draw_fake_text("Estilo A: Assinatura Centralizada (Estilo Contrato)")
    base_y = 100
    # Imagem
    c.drawImage(img_path, (width - target_w)/2, base_y + 15, width=target_w, height=target_h, mask='auto')
    # Linha
    c.setLineWidth(0.5)
    c.line(width/2 - 120, base_y + 10, width/2 + 120, base_y + 10)
    # Textos
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(width/2, base_y - 2, nome_str)
    c.setFont("Helvetica", 8)
    c.drawCentredString(width/2, base_y - 14, data_str)
    c.drawCentredString(width/2, base_y - 24, tech_str)
    c.showPage()
    
    # --- Estilo B: Corporativo Lateral ---
    draw_fake_text("Estilo B: Estilo Corporativo Lateral")
    box_w = 320
    box_h = 60
    box_x = width - box_w - 40
    box_y = 60
    c.setLineWidth(1)
    c.line(box_x + 130, box_y + 5, box_x + 130, box_y + box_h - 5)
    
    # Imagem (escala pra caber na caixa esquerda)
    scale = min(120 / img_w, 50 / img_h)
    new_w, new_h = img_w * scale, img_h * scale
    c.drawImage(img_path, box_x + (120-new_w)/2, box_y + (box_h-new_h)/2, width=new_w, height=new_h, mask='auto')
    
    # Texto
    c.setFont("Helvetica-Bold", 8)
    c.drawString(box_x + 140, box_y + 35, nome_str)
    c.setFont("Helvetica", 8)
    c.drawString(box_x + 140, box_y + 22, data_str)
    c.drawString(box_x + 140, box_y + 10, tech_str)
    c.showPage()
    
    # --- Estilo C: Rodapé Minimalista + Assinatura ---
    draw_fake_text("Estilo C: Minimalista ICP-Brasil + Assinatura Real")
    y_pos = 3 * cm
    x_pos = width / 2
    text = "[ ICP-Brasil ] Documento assinado eletronicamente por Diego Ribeiro de Souza (OAB/MG 211.002) em 29/07/2026."
    c.setFont("Helvetica", 9)
    c.drawCentredString(x_pos, y_pos, text)
    # Linha sutil
    c.setLineWidth(0.5)
    c.setStrokeColorRGB(0.5, 0.5, 0.5)
    t_width = c.stringWidth(text, "Helvetica", 9)
    c.line(x_pos - (t_width/2), y_pos + 8, x_pos + (t_width/2), y_pos + 8)
    # Assinatura flutuando em cima da linha
    c.drawImage(img_path, (width - target_w)/2, y_pos + 12, width=target_w, height=target_h, mask='auto')
    c.showPage()
    
    c.save()
    print("Mocks de Assinatura Real gerados com sucesso!")
