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
    exit()

speicher_data = json.loads(Klartext.decode())

seite = input("Auf welcher seite wollen sie was ändern? ")

if seite not in speicher_data:
    print("Diese Seite existiert nicht im Vault.")
    exit()

print("\nAktueller Eintrag:")
print(f"  Benutzername: {speicher_data[seite].get('benutzername', '')}")
print(f"  Passwort:     {speicher_data[seite].get('passwort', '')}\n")

neuer_benutzer = input("Neuer Benutzername: ")
neues_passwort = input("Neues Passwort: ")

eintrag = speicher_data[seite]

if neuer_benutzer != "":
    eintrag["benutzername"] = neuer_benutzer

if neues_passwort != "":
    eintrag["passwort"] = neues_passwort

speicher_data[seite] = eintrag

new_plaintext = json.dumps(speicher_data).encode()

new_nonce = os.urandom(12)
aes = AESGCM(key)
new_ciphertext = aes.encrypt(new_nonce, new_plaintext, None)

speicher["nonce"] = base64.b64encode(new_nonce).decode()
speicher["ciphertext"] = base64.b64encode(new_ciphertext).decode()

with open("speicher.json", "w") as f:
    json.dump(speicher, f, indent=2)

print("Eintrag aktualisiert.")
