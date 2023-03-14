import sqlite3
from information import Ui_Information
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QTableWidgetItem, QWidget


class Information(QWidget, Ui_Information):  # ToDo: Информация
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pred = 'Математика'
        self.initUI()

    def initUI(self):
        self.comboBox.currentTextChanged.connect(self.object)
        self.pushButton.clicked.connect(self.choice)
        self.connection = sqlite3.connect("CalcBaz.sqlite")
        self.con = self.connection.cursor()

    def object(self, s):  # Получение значения comboBox
        self.pred = s

    def choice(self):  # Вывод информации по разделу
        self.textBrowser.setText('')
        res = self.con.execute(f"""SELECT definition FROM information WHERE object = '{self.pred}'""").fetchall()
        self.name = res[-1][-1]
        self.textBrowser.setText(self.name)
