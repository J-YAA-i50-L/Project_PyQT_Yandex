import sys
import sqlite3
from math import factorial, sqrt, sin, cos, tan, radians
import math
from PyQt5 import uic
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QTableWidgetItem, QWidget
from menu import Ui_MainWindow
from Informations import Information
from Physics import PhCalc
from Informatics import InfCalc
from Mathematics import MachCalc


class Sections(QMainWindow, Ui_MainWindow):  # ToDo: Меню
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.pushButton_2.clicked.connect(self.click_mach)  # Матиматика
        self.pushButton_3.clicked.connect(self.click_inf)  # Информация
        self.pushButton.clicked.connect(self.click_ph)  # Физика
        self.pushButton_4.clicked.connect(self.click_informate)  # Физика

    def click_inf(self):  # ToDo: Раздел информатика
        self.inf = InfCalc()
        self.inf.show()

    def click_mach(self):  # ToDo: Раздел математика
        self.mach = MachCalc()
        self.mach.show()

    def click_ph(self):  # ToDo: Раздел физика
        self.ph = PhCalc()
        self.ph.show()

    def click_informate(self):  # ToDo: Информация
        self.info = Information()
        self.info.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Sections()
    ex.show()
    sys.exit(app.exec())