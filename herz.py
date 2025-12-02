import json
import os
import base64
import getpass
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from fun import generate_AES_key
import secrets
import string
def speicher_laden():
    with open("speicher.json", "r") as f:
        return json.load(f)

def decrypt_vault(password):
    speicher = speicher_laden()

    salt_b = base64.b64decode(speicher["salt"])
    nonce_b = base64.b64decode(speicher["nonce"])
    ciphertext_b = base64.b64decode(speicher["ciphertext"])

    key = generate_AES_key(password, salt_b)

    aes = AESGCM(key)

    
    try:
        klartext = aes.decrypt(nonce_b, ciphertext_b, None)
    except Exception:
        print("Falsches Passwort!")
        return None, None, None

    data = json.loads(klartext.decode())
    return data, key, speicher

def anzeigen(data, seite=None):

    if seite is None or seite.lower() == "all":
        return data

    if seite not in data:
        return None

    return {seite: data[seite]}
