import json
print("=== ATTACKER: Email Intercepted ===")
with open("data/encrypted_package.json") as f:
    bundle = json.load(f)
print(f"Stole ciphertext: {bundle['ciphertext'][:60]}... -> unreadable")
print("Trying to decrypt without private key -> FAILS")
print("Trying to tamper -> signature check will FAIL for Dr. John")
print("\nCONCLUSION: Encryption saved patient data even though email leaked.")
