import json
import os
import base64
import getpass
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from fun import generate_AES_key

with open("speicher.json","r") as f:
    speicher = json.load(f)

salt_bytes =base64.b64decode(speicher["salt"])
nonce_bytes =base64.b64decode(speicher["nonce"])
ciphertext_bytes = base64.b64decode(speicher["ciphertext"])

Eingabe_Passwort = getpass.getpass("Passowert eingeben bitte: ")

key = generate_AES_key(Eingabe_Passwort,salt_bytes)

aes =AESGCM(key)

try:
    Klartext = aes.decrypt(nonce_bytes,ciphertext_bytes,None)
except Exception:
    print("Flasches Passwort du lümmel")
    exit()

speicher_data = json.loads(Klartext.decode())

seite = input("Seite: ")
benutzername = input("Benutzername: ")
password = input("Passwort: ")




speicher_data[seite] ={"benutzername": benutzername,"passwort":password}

new_plaintext = json.dumps(speicher_data).encode()

new_nonce = os.urandom(12)
aes = AESGCM(key)
new_ciphertext = aes.encrypt(new_nonce,new_plaintext,None)

speicher["nonce"] = base64.b64encode(new_nonce).decode()
speicher["ciphertext"] = base64.b64encode(new_ciphertext).decode()

with open("speicher.json", "w") as f:
    json.dump(speicher, f, indent=2)
