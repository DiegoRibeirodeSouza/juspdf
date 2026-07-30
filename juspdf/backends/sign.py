import os
from pathlib import Path
from rich.console import Console

console = Console()

def sign_batch_with_a3(tasks: list, pin: str) -> None:
    """Assina um ou múltiplos PDFs em lote usando Token A3 (PKCS#11) via pyHanko, reutilizando a sessão."""
    try:
        from pyhanko.sign import signers
        from pyhanko.sign.pkcs11 import PKCS11Signer
        from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
    except ImportError:
        console.print("[bold red]Erro:[/bold red] O pacote pyhanko[pkcs11] não está instalado ou configurado.")
        return

    # Buscar biblioteca PKCS#11 do sistema (OpenSC é o mais comum no Linux)
    pkcs11_paths = [
        "/usr/lib/safesign-private/libaetpkss.so.3",
        "/usr/lib/safesign-private/libaetpkss.so",
        "/usr/lib/x86_64-linux-gnu/opensc-pkcs11.so",
        "/usr/lib/opensc-pkcs11.so",
        "/usr/lib/libeToken.so",
        "/usr/lib/libaetpkss.so.3",
        "/usr/local/lib/libeToken.so",
        "/usr/lib/libwdkP11.so", # Certisign
        "/usr/lib/watchdata/ICP/lib/libwdkP11.so", # WatchData
        "/usr/lib/libbit4xpki.so" # Bit4id
    ]
    
    try:
        import pkcs11
        
        module_path = None
        token = None
        
        for p in pkcs11_paths:
            if os.path.exists(p):
                try:
                    lib = pkcs11.lib(p)
                    tokens = list(lib.get_tokens())
                    if tokens:
                        module_path = p
                        token = tokens[0]
                        break
                except Exception:
                    continue
        
        if not module_path or not token:
            console.print("[bold red]Erro:[/bold red] Nenhum token/smartcard detectado nas bibliotecas padrões. Conecte o dispositivo A3 e tente novamente.")
            return
            
        console.print(f"[bold green]Módulo PKCS#11 detectado:[/bold green] {module_path}")
        console.print(f"[bold green]Token encontrado:[/bold green] {token.label}")
        console.print("[yellow]Comunicando com o Token A3 (abrindo sessão criptográfica única)...[/yellow]")
        
        with token.open(user_pin=pin) as session:
            # Lista certificados disponíveis no token
            certs = list(session.get_objects({pkcs11.Attribute.CLASS: pkcs11.ObjectClass.CERTIFICATE}))
            cert_options = []
            for c in certs:
                try:
                    label = c[pkcs11.Attribute.LABEL]
                    if isinstance(label, bytes):
                        label = label.decode('utf-8', errors='ignore')
                    cid = c[pkcs11.Attribute.ID]
                    if label and cid:
                        cert_options.append({'label': label, 'id': cid})
                except Exception:
                    pass
            
            chosen_cert_id = None
            
            for c in cert_options:
                if c['label'] == "DIEGO RIBEIRO DE SOUZA 2024-10-09 20:22:25":
                    chosen_cert_id = c['id']
                    chosen_label = c['label']
                    break
            
            if not chosen_cert_id:
                if len(cert_options) > 1:
                    import questionary
                    choices = [c['label'] for c in cert_options]
                    chosen_label = questionary.select(
                        "Foram encontrados múltiplos certificados no Token. Selecione qual deseja utilizar:",
                        choices=choices
                    ).ask()
                    
                    if not chosen_label:
                        console.print("[yellow]Operação cancelada pelo usuário.[/yellow]")
                        return
                    
                    for c in cert_options:
                        if c['label'] == chosen_label:
                            chosen_cert_id = c['id']
                            break
                elif len(cert_options) == 1:
                    chosen_cert_id = cert_options[0]['id']
                    chosen_label = cert_options[0]['label']
                
            from pyhanko.sign.signers.pdf_signer import PdfSigner
            from pyhanko.sign.fields import SigFieldSpec
            from pyhanko.stamp import TextStampStyle
            import io
            
            cert_name = "Certificado ICP-Brasil"
            if chosen_cert_id:
                for c in cert_options:
                    if c['id'] == chosen_cert_id:
                        cert_name = c['label'].split(' emitido ')[0].split(' (')[0].split(' 20')[0].strip()
                        break
                        
            stamp_style = TextStampStyle(
                stamp_text=f"Assinado digitalmente por {cert_name}\nData: %(ts)s\nTecnologia: pyHanko"
            )

            for input_pdf, output_pdf in tasks:
                try:
                    # Instanciar o signer e meta a cada arquivo para evitar 'stale state' no driver PKCS11
                    signer_kwargs = {'pkcs11_session': session, 'use_raw_mechanism': True}
                    if chosen_cert_id:
                        signer_kwargs['cert_id'] = chosen_cert_id
                    signer = PKCS11Signer(**signer_kwargs)

                    meta = signers.PdfSignatureMetadata(
                        field_name='Signature1',
                        reason='Assinado digitalmente via JusPDF',
                    )

                    with open(input_pdf, 'rb') as doc_in:
                        w = IncrementalPdfFileWriter(doc_in)
                        
                        new_field_spec = SigFieldSpec(
                            sig_field_name='Signature1',
                            on_page=-1, # última página
                            box=(150, 20, 450, 100) # x1, y1, x2, y2 (centralizado no rodapé)
                        )
                        
                        pdf_signer = PdfSigner(
                            signature_meta=meta,
                            signer=signer,
                            stamp_style=stamp_style,
                            new_field_spec=new_field_spec
                        )
                        
                        # Usar um buffer em memória para prevenir corrompimento caso o token falhe no meio da operação
                        out_buffer = io.BytesIO()
                        pdf_signer.sign_pdf(
                            w, existing_fields_only=False, output=out_buffer
                        )
                        
                        # Se não houve erro, salvar no arquivo final
                        with open(output_pdf, 'wb') as doc_out:
                            doc_out.write(out_buffer.getvalue())
                            
                    console.print(f"[bold green]Sucesso:[/bold green] Arquivo assinado e salvo em {output_pdf.name}")
                except Exception as ex:
                    console.print(f"[bold red]Falha ao assinar '{input_pdf.name}':[/bold red] {ex}")
                    
    except Exception as e:
        console.print(f"[bold red]Falha na comunicação com o Token:[/bold red] {e}")
        console.print("Verifique se o token A3 está bem conectado e se a senha está correta.")

def sign_with_a3(input_pdf: Path, output_pdf: Path, pin: str) -> None:
    sign_batch_with_a3([(input_pdf, output_pdf)], pin)
