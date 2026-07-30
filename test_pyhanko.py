try:
    from pyhanko.sign.pkcs11 import PKCS11Signer
    print("PKCS11Signer imported successfully")
except Exception as e:
    print(f"Error: {e}")
