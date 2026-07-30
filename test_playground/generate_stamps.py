import os
from pyhanko.sign import signers
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign.signers.pdf_signer import PdfSigner
from pyhanko.sign.fields import SigFieldSpec
from pyhanko.stamp import TextStampStyle, QRStampStyle
from pyhanko.pdf_utils.images import PdfImage

signer = signers.SimpleSigner.load(
    key_file='key.pem', 
    cert_file='cert.pem', 
    ca_chain_files=('cert.pem',), 
    signature_mechanism=None
)
meta = signers.PdfSignatureMetadata(field_name='Signature1', url="https://validar.iti.gov.br")

style1 = TextStampStyle(
    stamp_text="Assinado digitalmente por\nDiego Ribeiro de Souza OAB/MG 211.002\nData: %(ts)s\nTecnologia: LitisDoc",
    border_width=2,
)

bg_img = PdfImage('dummy_logo.png')
style2 = TextStampStyle(
    stamp_text="Assinado digitalmente por\nDiego Ribeiro de Souza OAB/MG 211.002\nData: %(ts)s",
    background=bg_img,
    background_opacity=0.3
)

style3 = QRStampStyle(
    stamp_text="Assinado digitalmente por\nDiego Ribeiro de Souza OAB/MG 211.002\nData: %(ts)s\nValide em %(url)s",
    border_width=1
)

def apply_stamp(input_path, output_path, style):
    with open(input_path, 'rb') as f:
        w = IncrementalPdfFileWriter(f)
        pdf_signer = PdfSigner(
            signature_meta=meta,
            signer=signer,
            stamp_style=style,
            new_field_spec=SigFieldSpec('Signature1', box=(150, 20, 450, 100))
        )
        with open(output_path, 'wb') as out:
            pdf_signer.sign_pdf(w, existing_fields_only=False, output=out)

try:
    apply_stamp("stamp_samples/blank_1.pdf", "stamp_samples/Estilo1_Classico.pdf", style1)
    apply_stamp("stamp_samples/blank_2.pdf", "stamp_samples/Estilo2_Institucional.pdf", style2)
    apply_stamp("stamp_samples/blank_3.pdf", "stamp_samples/Estilo3_QRCode.pdf", style3)
    print("Sucesso!")
except Exception as e:
    print("Error:", e)
