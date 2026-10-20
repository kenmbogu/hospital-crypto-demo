# Hospital Secure File Transfer - Cryptography Demo

> What happens when a hospital email gets hijacked? This project proves that with proper encryption, stolen data is still useless.

A practical simulation showing how **Hybrid Encryption (RSA + AES-GCM + Signatures)** protects patient medical results even when the communication channel is compromised.

### The Story

- **Amina Fleming (Hospital Worker):** Has a file `patient_medical_results.txt` that needs to be sent securely.
- **Dr. John Peter (Doctor):** The recipient. Only he should be able to read the file.
- **You (The Attacker):** You intercept the email and try to read or alter the file.

### How It Works

We use **Hybrid Encryption**, which is how real healthcare systems work:

1. **Key Generation:** Both Amina and Dr. John generate RSA-2048 key pairs.
2. **Encryption (Amina's side):**
   - Generate random AES-256 key.
   - Encrypt file with AES-GCM (fast + authenticated).
   - Encrypt AES key with Dr. John's PUBLIC key (OAEP).
   - Sign ciphertext with Amina's PRIVATE key (PSS) - proves origin.
3. **Attack Simulation:** Attacker intercepts email. Without Dr. John's private key, data is unreadable. Tampering breaks signature.
4. **Decryption (Dr. John's side):**
   - Verify Amina's signature, decrypt AES key with his PRIVATE key, decrypt file.

**Result:** Decrypted file == Original only for the legitimate doctor.

### Project Structure



### How to Run

```bash
# 1. Install
pip install -r requirements.txt

# 2. Generate keys for Amina and John
python src/generate_keys.py

# 3. Amina encrypts
python src/encrypt.py

# 4. Attacker tries (and fails)
python src/attacker.py

# 5. John decrypts
python src/decrypt.py


## Proof - Attack Fails, Doctor Succeeds

### 1. Attacker intercepts email but fails
He steals `f0457f1f...` ciphertext but it's unreadable. No private key = FAILS. Tampering = signature FAILS.

![Attacker Fails]
(01_attacker_fails.png)

### 2. Authorized doctor decrypts successfully
Signature verified from Amina Fleming, original patient data recovered.

![Doctor Decrypts]
(02_doctor_decrypts_ok.png)

**Tech:** AES-256 + RSA + Digital Signature | Synthetic data only, no real PHI


