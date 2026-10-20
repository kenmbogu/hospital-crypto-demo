from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
import os, json

def load_public_key(p): return serialization.load_pem_public_key(open(p,"rb").read())
def load_private_key(p): return serialization.load_pem_private_key(open(p,"rb").read(), None)

john_public = load_public_key("keys/john_peter_public.pem")
amina_private = load_private_key("keys/amina_fleming_private.pem")

with open("data/patient_medical_results_sample.txt","rb") as f:
    plaintext = f.read()

aes_key = AESGCM.generate_key(bit_length=256)
aesgcm = AESGCM(aes_key)
nonce = os.urandom(12)
ciphertext = aesgcm.encrypt(nonce, plaintext, None)

encrypted_aes_key = john_public.encrypt(aes_key,
    padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

signature = amina_private.sign(ciphertext,
    asym_padding.PSS(mgf=asym_padding.MGF1(hashes.SHA256()), salt_length=asym_padding.PSS.MAX_LENGTH),
    hashes.SHA256())

bundle = {
    "encrypted_aes_key": encrypted_aes_key.hex(),
    "nonce": nonce.hex(),
    "ciphertext": ciphertext.hex(),
    "signature": signature.hex()
}
with open("data/encrypted_package.json","w") as out:
    json.dump(bundle, out, indent=2)
print("[Amina] Encrypted - ready to send via email")
