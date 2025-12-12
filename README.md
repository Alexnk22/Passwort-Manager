# Password Manager (PyQt6 + AES)

Ein einfacher, lokaler Passwort-Manager mit verschlüsseltem JSON-Storage und PyQt6-GUI.  
Alle Einträge werden mit einem Masterpasswort über AES-GCM verschlüsselt und in einer Datei (`speicher.json`) gespeichert.

---

## Features

**Masterpasswort-Login**  
Beim Start gibst du dein Masterpasswort ein. Nur mit dem richtigen Passwort kann der Tresor entschlüsselt werden.

**Verschlüsselter Speicher**  
Die Passwörter liegen nicht im Klartext, sondern als AES-GCM-Ciphertext in `speicher.json`.  
Schlüsselableitung erfolgt über `generate_AES_key(...)` aus `fun.py`.

**Passwort-Tabelle**  
Nach dem Login siehst du eine Tabelle mit  
Webseite, Benutzername, verstecktem Passwort sowie Buttons zum Kopieren, Bearbeiten und Löschen.

**Suchen und Filtern**  
Über das Suchfeld kannst du nach Webseite, Benutzername oder Passwort suchen.  
Zeilen, die nicht passen, werden ausgeblendet.

**Passwörter hinzufügen**  
Über den NEW-Button kannst du neue Einträge anlegen.  
Es gibt ein eigenes Fenster mit Feldern für Webseite, Benutzername und Passwort sowie einen Button zum zufälligen Passwort generieren.

**Bearbeiten und Löschen**  
Einträge lassen sich über das Edit-Fenster ändern.  
Mit dem Delete-Button können Einträge nach Bestätigung endgültig gelöscht werden.  
Nach jeder Änderung wird der Tresor neu verschlüsselt gespeichert.

---

## Screenshots

Login-Fenster:

<img width="210" height="139" alt="grafik" src="https://github.com/user-attachments/assets/e331223f-71a5-4380-bded-7a3884e2ba9a" />

Passwort-Übersicht:

<img width="712" height="439" alt="grafik" src="https://github.com/user-attachments/assets/7efac697-f99b-40ca-9c65-f4b6ca76e37b" />

Neuen Eintrag hinzufügen:

<img width="313" height="279" alt="grafik" src="https://github.com/user-attachments/assets/db7c2a74-0f28-4e63-a65c-8105c2d310b0" />

---

## Projektstruktur

Typischer Aufbau des Projekts:

`gui.py` – PyQt6-Oberfläche (Login-Fenster, Tabelle, NEW/Edit/Delete, Suchen)  
`herz.py` – Logik für Entschlüsselung, Aktualisieren, Hinzufügen, Löschen und `encrypt_and_save`  
`fun.py` – Hilfsfunktionen, z. B. `generate_AES_key`  
`speicher.json` – verschlüsselter Tresor (Nonce, Salt, Ciphertext, …)  
`init.py` – Skript zum Erstellen eines neuen Tresors (neue `speicher.json` mit eigenem Masterpasswort)

---

## Installation und Start

Voraussetzungen: Python 3.x installiert.

Benötigte Pakete installieren, zum Beispiel:

```bash
pip install pyqt6 cryptography
