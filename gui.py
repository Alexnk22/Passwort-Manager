import sys

import json 
from herz import decrypt_vault, anzeigen
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QLineEdit,
    QWidget, QMessageBox, QGridLayout, QTableWidget, QTableWidgetItem
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

        self.menu = MainMenuWindow(self.s_data,self.key,self.speicher,self.passwort_real)
        self.menu.show()
        self.close()
        
        
class MainMenuWindow(QMainWindow):
    def __init__(self, data, key, speicher, password):
        super().__init__()
        self.data = data
        self.setWindowTitle("Speicher")
        self.setFixedSize(500, 300)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QGridLayout()
        central.setLayout(layout)

        self.button1 = QPushButton("Passwörter anzeigen")
        self.button1.setMinimumSize(200,150)
        self.button1.clicked.connect(self.open_passwort_anzeige)
        layout.addWidget(self.button1,0,0)

        self.button2 = QPushButton("Passwörter bearbeiten")
        self.button2.setMinimumSize(200,150)
        layout.addWidget(self.button2,0,1)

        self.btn_logout = QPushButton("Logout")
        layout.addWidget(self.btn_logout, 1, 0, 1, 2) 
        self.btn_logout.clicked.connect(self.logout)

    def open_passwort_anzeige(self):
        self.pw_window = passworter_anzeigen(self.data)
        self.pw_window.show()
        self.close()

    def logout(self):
        self.close()

class passworter_anzeigen(QMainWindow):
    def __init__(self, data):
        super().__init__()

        self.setWindowTitle("Passwörter")
        self.setFixedSize(700, 400)
        self.data = data

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        central.setLayout(layout)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Suchen...")
        self.search.textChanged.connect(self.filter_table)
        layout.addWidget(self.search)
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Webseite", "Benutzername", "Passwort", "Cpy"])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        

        self.table.verticalHeader().setDefaultSectionSize(25)

       
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 30)

        layout.addWidget(self.table)
  

        self.visible = {}
        self.table.cellClicked.connect(self.toggle_password)
        self.table.itemSelectionChanged.connect(self.hide_all_passwords)


        self.load_data()
        

    def load_data(self):
        daten_dict = anzeigen(self.data, "all")

        self.table.setRowCount(len(daten_dict))

        for row, (seite, info) in enumerate(daten_dict.items()):
            bn = info.get("benutzername", "")
            pw = info.get("passwort", "")

            self.visible[row] = False
            self.table.setItem(row, 0, QTableWidgetItem(seite))
            self.table.setItem(row, 1, QTableWidgetItem(bn))

     
     
            masked = "●" * len(pw)
            pw_item = QTableWidgetItem(masked)
            pw_item.setData(Qt.ItemDataRole.UserRole, pw)
            self.table.setItem(row, 2, pw_item)


            copy_btn = QPushButton("K")
            self.table.setStyleSheet("QTableWidget::item { padding: 0px; margin: 0px; }")
            copy_btn.setFixedSize(30,30)

            copy_btn.clicked.connect(lambda _, r=row: self.copy_password(r))
            self.table.setCellWidget(row, 3, copy_btn)
            

            

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