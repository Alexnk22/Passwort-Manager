    import json
    import os
    import base64
    import getpass
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from fun import generate_AES_key


    def speicher_laden():
        with open("speicher.json", "r") as f:
            return json.load(f)


    def speicher_sichern(speicher):
        with open("speicher.json", "w") as f:
            json.dump(speicher, f, indent=2)


    def decrypt_vault():
        speicher = speicher_laden()

        salt_b = base64.b64decode(speicher["salt"])
        nonce_b = base64.b64decode(speicher["nonce"])
        ciphertext_b = base64.b64decode(speicher["ciphertext"])

        password = getpass.getpass("Passwort: ")
        key = generate_AES_key(password, salt_b)

        aes = AESGCM(key)
        try:
            klartext = aes.decrypt(nonce_b, ciphertext_b, None)
        except Exception:
            print("Falsches Passwort!")
            return None, None, None

        data = json.loads(klartext.decode())
        return data, key, speicher

    def anzeigen(data):
        if not data:
            print("Nichts gespeichert!")
            return


        for seite, eintrag in data.items():
            print(f"{seite}:")
            print(f"  Benutzername: {eintrag.get('benutzername', '')}")
            print(f"  Passwort: {eintrag.get('passwort', '')}")
            print()

    def hinzufuegen(data):
        seite = input("Seite: ")
        benutzer = input("Benutzername: ")
        passwort = input("Passwort: ")

        data[seite] = {
            "benutzername": benutzer,
            "passwort": passwort
        }

        print(f"'{seite}' wurde hinzugefügt.")


    def löschen(data):
        seite = input("Welche Seite soll gelöscht werden? ")

        if seite not in data:
            print(f"'{seite}' gibt es nciht")
            return

        del data[seite]
        print(f"'{seite}' wurde gelöscht.")



    def aktualisieren(data):
        seite = input("Welche Seite möchtest du aktualisieren? ")

        if seite not in data:
            print(f"'{seite}' gibt es nciht")
            return

        eintrag = data[seite]

        print("\nAktueller Eintrag:")
        print(f"  Benutzername: {eintrag.get('benutzername', '')}")
        print(f"  Passwort: {eintrag.get('passwort', '')}\n")

        neuer_benutzer = input("Neuer Benutzername: ")
        neues_passwort = input("Neues Passwort: ")

        if neuer_benutzer != "":
            eintrag["benutzername"] = neuer_benutzer

        if neues_passwort != "":
            eintrag["passwort"] = neues_passwort

        data[seite] = eintrag

        print(f"'{seite}' wurde aktualisiert.")



    def encrypt_and_save(data, key, speicher):
        new_plaintext = json.dumps(data).encode()
        new_nonce = os.urandom(12)

        aes = AESGCM(key)
        new_ciphertext = aes.encrypt(new_nonce, new_plaintext, None)

        speicher["nonce"] = base64.b64encode(new_nonce).decode()
        speicher["ciphertext"] = base64.b64encode(new_ciphertext).decode()

        speicher_sichern(speicher)

    if __name__ == "__main__":
        while True:
            print("\n===== Passwort-Manager =====")
            print("1 – Alle Einträge anzeigen")
            print("2 – Eintrag hinzufügen")
            print("3 – Eintrag löschen")
            print("4 – Eintrag aktualisieren")
            print("5 – Programm beenden")

            auswahl = input("\nAuswahl: ")
            if auswahl  == "5":
                print("Programm beendet.")
                break

            data, key, speicher = decrypt_vault()

            if data is None:
                continue

            if auswahl == "1":
                anzeigen(data)

            elif auswahl == "2":
                hinzufuegen(data)
                encrypt_and_save(data, key, speicher)

            elif auswahl == "3":
                löschen(data)
                encrypt_and_save(data, key, speicher)

            elif auswahl == "4":
                aktualisieren(data)
                encrypt_and_save(data, key, speicher)

            elif auswahl == "5":
                print("Programm beendet.")
                break

            else:
                print("Ungültige Auswahl.")
