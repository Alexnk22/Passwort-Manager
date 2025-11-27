import json
import os
import base64
import getpass
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from fun import generate_AES_key

with open("speicher.json", "r") as f:
    speicher = json.load(f)

salt_b = base64.b64decode(speicher["salt"])
nonce_b = base64.b64decode(speicher["nonce"])
ciphertext_b = base64.b64decode(speicher["ciphertext"])

Eingabe_Passwort = getpass.getpass("Passowert eingeben bitte: ")

key = generate_AES_key(Eingabe_Passwort,salt_b)

aes =AESGCM(key)

try:
    Klartext = aes.decrypt(nonce_b,ciphertext_b,None)
except Exception:
    print("Flasches Passwort du lümmel")

speicher_data = json.loads(Klartext.decode())

seite = input("Welche Seite soll gelöscht werden? ")

if seite not in speicher_data:
    print("Diese Seite existiert nicht im Vault.")
    exit()

# löschen
del speicher_data[seite]

print(f"Eintrag '{seite}' wurde gelöscht.")

new_plaintext = json.dumps(speicher_data).encode()

new_nonce = os.urandom(12)
aes = AESGCM(key)
new_ciphertext = aes.encrypt(new_nonce, new_plaintext, None)

speicher["nonce"] = base64.b64encode(new_nonce).decode()
speicher["ciphertext"] = base64.b64encode(new_ciphertext).decode()

with open("speicher.json", "w") as f:
    json.dump(speicher, f, indent=2)
