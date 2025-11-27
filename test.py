from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os
import base64

def generate_AES_key(passwort: str, salt:bytes)->bytes:
    KDF = PBKDF2HMAC(
        algorithm = hashes.SHA256(),
        length = 32, 
        salt = salt,
        iterations = 200_000,
        backend=default_backend())

    key = KDF.derive(passwort.encode())
    return key


if __name__ == "__main__":
    salt = os.urandom(16)
    pw = "meinPasswort123"

    key1 = generate_AES_key(pw, salt)
    key2 = generate_AES_key(pw, salt)

    print("Gleicher Key?", key1 == key2)

    salt2 = os.urandom(16)
    key3 = generate_AES_key(pw, salt2)

    print("Andere Salts → anderer Key?", key1 != key3)

