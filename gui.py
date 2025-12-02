import sys

import json,random,string
from herz import decrypt_vault, anzeigen, aktualisieren, encrypt_and_save, löschen, hinzufuegen
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QLineEdit,
    QWidget, QMessageBox, QGridLayout, QTableWidget, QTableWidgetItem, QHBoxLayout
)
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


        self.setWindowTitle("Password Manager")

        central = QWidget()     
        self.setCentralWidget(central)


        self.layout = QVBoxLayout()
        central.setLayout(self.layout)

        self.label = QLabel("Passwort: ")
        self.layout.addWidget(self.label)

        self.p_input = QLineEdit()
        self.p_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.p_input.returnPressed.connect(self.login_start)
        self.layout.addWidget(self.p_input)

        self.status = QLabel("")
        self.layout.addWidget(self.status)

        self.login = QPushButton("login")
        self.login.setDefault(True)
        self.login.clicked.connect(self.login_start)
        self.layout.addWidget(self.login)

        self.setFixedSize(200,100)


    def login_start(self):
        Password = self.p_input.text()

        if(Password.strip()==""):
            QMessageBox.warning(self,"Fehler","Passwort eingeben!")
            return 
        data, key, speicher = decrypt_vault(Password)

        if data is None:
            QMessageBox.critical(self,"Fehler","Falschen Passwort.")
            return 
        self.s_data = data
        self.key = key
        self.speicher = speicher
        self.passwort_real = Password

        self.status.setText("Richtiges Passwort.")
        self.pw_window = MAIN_MANAGER(self.s_data,self.key,self.speicher)
        self.pw_window.show()
        self.close()

        
        


class MAIN_MANAGER(QMainWindow):
    def __init__(self, data,key,speicher):
        super().__init__()

        self.setWindowTitle("Passwörter")
        self.setFixedSize(700, 400)
        self.data = data
        self.key = key
        self.speicher = speicher

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        central.setLayout(layout)


        top = QHBoxLayout()

        #suchleiste
        self.search = QLineEdit()
        self.search.setPlaceholderText("Suchen...")
        self.search.textChanged.connect(self.filter_table)
        self.search.setFixedHeight(30)
        top.addWidget(self.search)

        #New Button
        self.new_btn = QPushButton("NEW")
        self.new_btn.setFixedSize(60, 30)
        self.new_btn.clicked.connect(self.new_pwd)
        top.addWidget(self.new_btn)

        #Tabele setup
        layout.addLayout(top)
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Webseite", "Benutzername", "Passwort", "Cpy","Edit","Del"])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setDefaultSectionSize(25)
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 30)
        self.table.setColumnWidth(4, 30)
        self.table.setColumnWidth(5, 30)
        layout.addWidget(self.table)
  

        self.visible = {}
        self.table.cellClicked.connect(self.toggle_password)
        self.table.itemSelectionChanged.connect(self.hide_all_passwords)
        self.load_data()

        
    def new_pwd(self):
        self.new_window = QWidget()
        self.new_window.setWindowTitle("Hinzufügen")
        self.new_window.setFixedSize(300, 240)

        layout = QVBoxLayout()
        self.new_window.setLayout(layout)

        #Webseite
        self.webseite = QLineEdit()
        layout.addWidget(QLabel("Webseite:"))
        layout.addWidget(self.webseite)

        #Benutzername
        self.benutzer = QLineEdit()
        layout.addWidget(QLabel("Benutzername:"))
        layout.addWidget(self.benutzer)

        #Passwort
        self.pwd = QLineEdit()
        layout.addWidget(QLabel("Passwort:"))
        layout.addWidget(self.pwd)

        #Passwort random generieren
        gen_btn = QPushButton("Passwort generieren")
        gen_btn.clicked.connect(self.generate_new_password)
        layout.addWidget(gen_btn)

        # Speichern
        speicher_button = QPushButton("Speichern")
        speicher_button.clicked.connect(self.neues_pwd_speichern)
        layout.addWidget(speicher_button)

        self.new_window.show()

    def generate_new_password(self):
        chars = string.ascii_letters + string.digits + "!$%&/()=?#@"
        pw = "".join(random.choice(chars) for _ in range(16))
        self.pwd.setText(pw)

    def neues_pwd_speichern(self):
        seite = self.webseite.text().strip()
        bn = self.benutzer.text().strip()
        pw = self.pwd.text().strip()

        if not seite or not bn:
            QMessageBox.warning(self, "Fehler", "Muss was beinhalten")
            return
        # fügt in speicher ein 
        hinzufuegen(self.data, seite, bn, pw)

        # verschlüsselt weider denn speicher
        encrypt_and_save(self.data, self.key, self.speicher)

        self.new_window.close()
        self.table.setRowCount(0)
        self.load_data()


        

    def load_data(self):
        dataa = anzeigen(self.data, "all")

        self.table.setRowCount(len(dataa))

        for row, (seite, info) in enumerate(dataa.items()):
            bn = info.get("benutzername", "")
            pw = info.get("passwort", "")

            self.visible[row] = False
            self.table.setItem(row, 0, QTableWidgetItem(seite))
            self.table.setItem(row, 1, QTableWidgetItem(bn))

     
            masked = "*" * len(pw)
            pw_item = QTableWidgetItem(masked)
            pw_item.setData(Qt.ItemDataRole.UserRole, pw)
            self.table.setItem(row, 2, pw_item)


            copy_btn = QPushButton("K")
            self.table.setStyleSheet("QTableWidget::item { padding: 0px; margin: 0px; }")
            copy_btn.setFixedSize(30,30)

            copy_btn.clicked.connect(lambda _, r=row: self.copy_password(r))
            self.table.setCellWidget(row, 3, copy_btn)
            edit_btn = QPushButton("E")
            edit_btn.setFixedSize(30, 30)
            edit_btn.clicked.connect(lambda _, r=row: self.edit_entry(r))
            self.table.setCellWidget(row, 4, edit_btn)

            delete_btn = QPushButton("D")
            delete_btn.setFixedSize(30, 30)
            delete_btn.clicked.connect(lambda _, r=row: self.delete_entry(r))
            self.table.setCellWidget(row, 5, delete_btn)
   
    def delete_entry(self, row):
        seite = self.table.item(row, 0).text()
        confirm = QMessageBox.question(
            self,
            "Löschen?",
            f'Soll der Eintrag "{seite}" wirklich gelöscht werden?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm != QMessageBox.StandardButton.Yes:
            return

        gelöscht = löschen(self.data, seite)

        if not gelöscht:
            QMessageBox.critical(self, "Fehler", "Konnte Eintrag nicht löschen!")
            return

        encrypt_and_save(self.data, self.key, self.speicher)
        self.table.removeRow(row)





    def edit_entry(self, row):
        seite = self.table.item(row, 0).text()
        bn = self.table.item(row, 1).text()
        pw = self.table.item(row, 2).data(Qt.ItemDataRole.UserRole)

        self.edit_win = QWidget()
        self.edit_win.setWindowTitle(f"Bearbeiten: {seite}")
        self.edit_win.setFixedSize(300, 180)

        layout = QVBoxLayout()
        self.edit_win.setLayout(layout)

        self.edit_user = QLineEdit()
        self.edit_user.setText(bn)
        layout.addWidget(QLabel("Benutzername:"))
        layout.addWidget(self.edit_user)

        self.edit_pass = QLineEdit()
        self.edit_pass.setText(pw)
        layout.addWidget(QLabel("Passwort:"))
        layout.addWidget(self.edit_pass)

        speicher_button = QPushButton("Speichern")
        speicher_button.clicked.connect(lambda: self.save_edit(row, seite))
        layout.addWidget(speicher_button)

        self.edit_win.show()

    def save_edit(self, row, seite):
            neuer_benutzername = self.edit_user.text().strip()
            neues_passwort = self.edit_pass.text().strip()

            aktualisieren(self.data, seite, neuer_benutzername, neues_passwort)

            encrypt_and_save(self.data, self.key, self.speicher)

            self.table.item(row, 1).setText(neuer_benutzername)

            masked = "*" * len(neues_passwort)
            pw_item = self.table.item(row, 2)
            pw_item.setText(masked)
            pw_item.setData(Qt.ItemDataRole.UserRole, neues_passwort)
            self.edit_win.close()


            

    def toggle_password(self, row, column):
        if column != 2:
            return

        item = self.table.item(row, 2)
        pw = item.data(Qt.ItemDataRole.UserRole)

        if not self.visible[row]:
            item.setText(pw)
            self.visible[row] = True
        else:
            item.setText("●" * len(pw))
            self.visible[row] = False

    def hide_all_passwords(self):
        for row in range(self.table.rowCount()):
            if self.visible[row]:
                item = self.table.item(row, 2)
                pw = item.data(Qt.ItemDataRole.UserRole)
                item.setText("*" * len(pw))
                self.visible[row] = False

    def copy_password(self, row):
        item = self.table.item(row, 2)
        pw = item.data(Qt.ItemDataRole.UserRole)

        if pw:
            QApplication.clipboard().setText(pw)
    def filter_table(self, text):
        text = text.lower().strip()

        for row in range(self.table.rowCount()):
            website = self.table.item(row, 0).text().lower()
            username = self.table.item(row, 1).text().lower()

            pw_item = self.table.item(row, 2)
            pw_original = pw_item.data(Qt.ItemDataRole.UserRole).lower()

            match = (
                text in website or
                text in username or
                text in pw_original
            )

            self.table.setRowHidden(row, not match)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()