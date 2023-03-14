import sqlite3
from calc_math_vop import Ui_Form
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QTableWidgetItem, QWidget


class MathContext(QWidget, Ui_Form):  # ToDo: Конте́кстное меню́
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.connection = sqlite3.connect('CalcBaz.sqlite')
        self.con = self.connection.cursor()
        self.pushButton.clicked.connect(self.yes)
        self.pushButton_2.clicked.connect(self.no)

    def yes(self):
        self.con.execute("""DELETE FROM mathematics WHERE id != 1""")
        self.connection.commit()
        self.connection.close()
        self.close()

    def no(self):
        self.close()
