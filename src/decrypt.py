from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
import json

def load_public_key(p): return serialization.load_pem_public_key(open(p,"rb").read())
def load_private_key(p): return serialization.load_pem_private_key(open(p,"rb").read(), None)

john_private = load_private_key("keys/john_peter_private.pem")
amina_public = load_public_key("keys/amina_fleming_public.pem")

bundle = json.load(open("data/encrypted_package.json"))
enc_key = bytes.fromhex(bundle["encrypted_aes_key"])
nonce = bytes.fromhex(bundle["nonce"])
cipher = bytes.fromhex(bundle["ciphertext"])
sig = bytes.fromhex(bundle["signature"])

amina_public.verify(sig, cipher,
    asym_padding.PSS(mgf=asym_padding.MGF1(hashes.SHA256()), salt_length=asym_padding.PSS.MAX_LENGTH),
    hashes.SHA256())
print("[John] Signature OK - from Amina")

aes_key = john_private.decrypt(enc_key,
    padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

plain = AESGCM(aes_key).decrypt(nonce, cipher, None)
print("[John] Decrypted successfully:\n", plain.decode())
