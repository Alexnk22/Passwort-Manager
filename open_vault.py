import json
import base64
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from test import generate_AES_key

with open("speicher.json","r") as f:
    speicher = json.load(f)

salt_bytes =base64.b64decode(speicher["salt"])
nonce_bytes =base64.b64decode(speicher["nonce"])
ciphertext_bytes = base64.b64decode(speicher["ciphertext"])

Eingabe_Passwort = input("Passowert eingeben bitte: ")

key = generate_AES_key(Eingabe_Passwort,salt_bytes)

aes =AESGCM(key)

try:
    Klartext = aes.decrypt(nonce_bytes,ciphertext_bytes,None)
    print("Vault geöffnet!")
    print("Inhalt: ",Klartext.decode())
except Exception:
    print("Flasches Passwort du lümmel")