import sqlite3
from if_calc import Ui_InfCalc
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QTableWidgetItem, QWidget
B = {'б': 0, 'К': 1, 'М': 2, 'Г': 3, 'Т': 4}


class InfCalc(QMainWindow, Ui_InfCalc):  # ToDo: Раздел информатика
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Начальные значения
        self.interpreter_ss_1 = '10'
        self.interpreter_ss_2 = '2'
        self.сounter_ss_1 = 2
        self.number = 0
        self.interpreter_unit_1 = 'бит'
        self.interpreter_unit_2 = 'байт'
        self.history = ''
        self.initUI()

    def initUI(self):
        # Переводчик СС подключение виджитов
        self.comboBox.currentTextChanged.connect(self.interpreter_text_changed_1)  # Исходная СС
        self.comboBox_2.currentTextChanged.connect(self.interpreter_text_changed_2)  # Конечная СС
        self.pushButton.clicked.connect(self.cliced_btn_1)
        # Счётчик цифр подключение виджитов
        self.comboBox_3.currentTextChanged.connect(self.col_text_changed_1)  # Конечная СС
        self.comboBox_4.currentTextChanged.connect(self.col_text_number)  # Цифра
        self.pushButton_2.clicked.connect(self.cliced_btn_2)
        # Переводчик из одной единица памяти в другую подключение виджитов
        self.comboBox_5.currentTextChanged.connect(self.interpreter_text_changed_3)  # Исходная еденица
        self.comboBox_7.currentTextChanged.connect(self.interpreter_text_changed_4)  # Конечная еденица
        self.pushButton_3.clicked.connect(self.cliced_btn_3)
        self.connection = sqlite3.connect('CalcBaz.sqlite')  # Подключение базы данных

    def interpreter_text_changed_1(self, s):  # Получение значения comboBox
        self.interpreter_ss_1 = s

    def interpreter_text_changed_2(self, s):  # Получение значения comboBox
        self.interpreter_ss_2 = s

    def col_text_changed_1(self, s):  # Получение значения comboBox
        self.сounter_ss_1 = s

    def col_text_number(self, s):  # Получение значения comboBox
        self.number = s

    def interpreter_text_changed_3(self, s):  # Получение значения comboBox
        self.interpreter_unit_1 = s

    def interpreter_text_changed_4(self, s):  # Получение значения comboBox
        self.interpreter_unit_2 = s

    def cliced_btn_1(self):  # Переводчик СС
        if self.interpreter_ss_1 != '10':
            ss_10 = int(self.lineEdit.text(), int(self.interpreter_ss_1))
        else:
            ss_10 = int(self.lineEdit.text())
        n = ''
        while ss_10 > 0:
            n = n + str(ss_10 % int(self.interpreter_ss_2))
            ss_10 = ss_10 // int(self.interpreter_ss_2)
        self.history = f'I: {self.lineEdit.text()} CC{self.interpreter_ss_1} -> {n[::-1]} CC{self.interpreter_ss_2}'
        self.connection.cursor().execute(f"""INSERT INTO inf_calc(history) VALUES('{self.history}')""")
        self.connection.commit()
        self.textBrowser_2.setText(n[::-1])

    def cliced_btn_2(self):  # Счётчик цифр
        col = 0  # Количество number в x
        x = eval(self.lineEdit_2.text())
        ss = int(self.сounter_ss_1)
        n = int(self.number)
        while x > 0:  # Цикл пока X > 0
            if x % ss == n:  # Ищем остаток от деления x на S.
                col += 1  # Если он равен number, то это number
            x //= ss
        self.history = f'II: {self.lineEdit_2.text()} CC{ss} {n} -> {col}'
        self.connection.cursor().execute(f"""INSERT INTO inf_calc(history) VALUES('{self.history}')""")
        self.textBrowser_3.setText(str(col))
        self.connection.commit()

    def cliced_btn_3(self):  # Переводчик из одной единица памяти в другую
        number = int(self.lineEdit_3.text())
        bits = 1
        if 'бит' in self.interpreter_unit_1 and 'бит' not in self.interpreter_unit_2:
            bits = 8
        summ = number * 1024 ** int(B[self.interpreter_unit_1[0]]) / bits  # перевод в биты или байты
        bits = 1
        if 'бит' not in self.interpreter_unit_1 and 'бит' in self.interpreter_unit_2:
            bits = 8
        summ = summ / 1024 ** int(B[self.interpreter_unit_2[0]]) * bits  # перевод в биты или байты
        self.textBrowser_5.setText(str(summ))
        self.history = f'''III: {number}{self.interpreter_unit_1} -> {summ}{self.interpreter_unit_2}'''
        self.connection.cursor().execute(f"""INSERT INTO inf_calc(history) VALUES('{self.history}')""")
        self.connection.commit()
