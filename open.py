import json
import base64
import os
import getpass
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from fun import generate_AES_key

with open("speicher.json","r") as f:
    speicher = json.load(f)

salt_bytes =base64.b64decode(speicher["salt"])
nonce_bytes =base64.b64decode(speicher["nonce"])
ciphertext_bytes = base64.b64decode(speicher["ciphertext"])

#print("Inhalt: ", base64.b64encode(ciphertext_bytes))

Eingabe_Passwort = getpass.getpass("Passowert eingeben bitte: ")

key = generate_AES_key(Eingabe_Passwort,salt_bytes)

aes =AESGCM(key)

try:
    Klartext = aes.decrypt(nonce_bytes,ciphertext_bytes,None)
    data = json.loads(Klartext.decode())

    #print(json.dumps(data,indent=1))

    for seite, eintrag in data.items():
        benutzer = eintrag.get("benutzername", "")
        pw = eintrag.get("passwort", "")

        print(f"{seite}:")
        print(f"  Benutzername: {benutzer}")
        print(f"  Passwort: {pw}")
        print()




except Exception:
    print("Flasches Passwort du lümmel")