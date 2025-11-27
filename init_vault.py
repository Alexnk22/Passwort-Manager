import os
import json
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from test import generate_AES_key 

def get_Passwort():
    
    return input("Das Passwort bitte: ")

salt = os.urandom(16)

AES_Key = generate_AES_key(get_Passwort(),salt)

# Data sind die daten die verschlüsselt werden sollen per AAES-GCM
data = b"{}"
aes = AESGCM(AES_Key)
nonce = os.urandom(12)
ciphertext = aes.encrypt(nonce,data,None)


speicher = {
    "salt":base64.b64encode(salt).decode("utf-8"),
    "nonce":base64.b64encode(nonce).decode("utf-8"),
    "ciphertext":base64.b64encode(ciphertext).decode("utf-8")
}

with open("speicher.json", "w") as f:
    json.dump(speicher, f, indent=2)



