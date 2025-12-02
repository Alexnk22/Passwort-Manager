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
        return None, None, None

    data = json.loads(klartext.decode())
    return data, key, speicher

def anzeigen(data, seite=None):

    if seite is None or seite.lower() == "all":
        return data

    if seite not in data:
        return None

    return {seite: data[seite]}

def aktualisieren(data, seite, neuer_benutzer=None, neues_passwort=None):
    if seite not in data:
        return False

    eintrag = data[seite]

    if neuer_benutzer:
        eintrag["benutzername"] = neuer_benutzer
    if neues_passwort:
        eintrag["passwort"] = neues_passwort

    data[seite] = eintrag
    return True

def encrypt_and_save(data, key, speicher):
    new_plaintext = json.dumps(data).encode()
    new_nonce = os.urandom(12)

    aes = AESGCM(key)
    new_ciphertext = aes.encrypt(new_nonce, new_plaintext, None)

    speicher["nonce"] = base64.b64encode(new_nonce).decode()
    speicher["ciphertext"] = base64.b64encode(new_ciphertext).decode()

    speicher_sichern(speicher)

def speicher_sichern(speicher):
    with open("speicher.json", "w") as f:
        json.dump(speicher, f, indent=2)


def löschen(data, seite):
    if seite not in data:
        return False

    del data[seite]
    return True

def hinzufuegen(data, seite, benutzer, passwort=None, auto_generate=False):
    if auto_generate:
        passwort = generate_random_password(16)

    data[seite] = {
        "benutzername": benutzer,
        "passwort": passwort
    }

    return True 