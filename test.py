import sys
import sqlite3
from math import factorial, sqrt, sin, cos, tan, radians
import math
from PyQt5 import uic
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QTableWidgetItem, QWidget
from mat_calc import Ui_MathematicalCalculator
from calc_math_vop import Ui_Form
from if_calc import Ui_InfCalc
from ph_calc import Ui_PhysicCalculator
from menu import Ui_MainWindow
from information import Ui_Information
B = {'б': 0, 'К': 1, 'М': 2, 'Г': 3, 'Т': 4}


class Sections(QMainWindow, Ui_MainWindow):  # ToDo: Раздел математика
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.pushButton_2.clicked.connect(self.click_mach)  # Матиматика
        self.pushButton_3.clicked.connect(self.click_inf)  # Информация
        self.pushButton.clicked.connect(self.click_ph)  # Физика
        self.pushButton_4.clicked.connect(self.click_informate)  # Физика

    def click_inf(self):
        self.inf = InfCalc()
        self.inf.show()

    def click_mach(self):
        self.mach = MachCalc()
        self.mach.show()

    def click_ph(self):
        self.ph = PhCalc()
        self.ph.show()

    def click_informate(self):
        self.info = Information()
        self.info.show()


class MachCalc(QWidget, Ui_MathematicalCalculator):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.znaks = ''
        self.operation = ''
        self.function = self.operation
        self.n1 = ''
        self.point = False
        self.flag_zero = True
        self.history_expression = ''
        self.initUI()

    def initUI(self):
        # Подключение кнопок с цифрами
        self.btn0.clicked.connect(self.click_on_number)
        self.btn1.clicked.connect(self.click_on_number)
        self.btn2.clicked.connect(self.click_on_number)
        self.btn3.clicked.connect(self.click_on_number)
        self.btn4.clicked.connect(self.click_on_number)
        self.btn5.clicked.connect(self.click_on_number)
        self.btn6.clicked.connect(self.click_on_number)
        self.btn7.clicked.connect(self.click_on_number)
        self.btn8.clicked.connect(self.click_on_number)
        self.btn9.clicked.connect(self.click_on_number)
        # Подключение плавоющей точки
        self.btn_point.clicked.connect(self.points)
        # Подключения выбора знака числа
        self.btn_znak.clicked.connect(self.click_znak)
        # удаление выраженния или символа
        self.btn_clear.clicked.connect(self.clear)
        self.btn_delet.clicked.connect(self.deled)
        # Подключение операций
        self.btn_plus.clicked.connect(self.math_functions)  # +
        self.btn_minus.clicked.connect(self.math_functions)  # -
        self.btn_mult.clicked.connect(self.math_functions)  # *
        self.btn_div.clicked.connect(self.math_functions)  # /
        self.btn_pow_4.clicked.connect(self.math_pow_2)  # **2
        self.btn_pow_3.clicked.connect(self.math_pow_3)  # **3
        self.btn_sqrt.clicked.connect(self.sqrt)  # корень
        self.btn_degree.clicked.connect(self.math_functions)  # x**y
        # подключение дополнительных функций
        self.btn_percent.clicked.connect(self.percent)  # %
        self.btn_fact.clicked.connect(self.factorial)  # n!
        self.btn_pi.clicked.connect(self.pi)
        self.btn_tan.clicked.connect(self.math_tan)
        self.btn_sin.clicked.connect(self.math_sin)
        self.btn_cos.clicked.connect(self.math_cos)
        self.btn_log.clicked.connect(self.math_functions)
        # подключение равно
        self.btn_eq.clicked.connect(self.eq)
        self.btn_clear_2.clicked.connect(self.clear_baze)
        # Работа с базой даных
        self.connection = sqlite3.connect('CalcBaz.sqlite')  # Подключение БД
        self.data_base()

    def data_base(self):  # Вывод знаений БД в журнал
        column = ['Выражение', 'Результат']
        queue = 'SELECT expression, result FROM mathematics'
        res = self.connection.execute(queue).fetchall()
        self.tableWidget.setRowCount(len(res))
        self.tableWidget.setColumnCount(len(res[0]))
        self.tableWidget.setItem(0, 0, QTableWidgetItem(column[0]))
        self.tableWidget.setItem(0, 1, QTableWidgetItem(column[1]))
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
        for i, row in enumerate(res):
            i += 1
            for j, col in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(col)))

    def now_data_bas(self):  # Добавления значения в БД
        self.connection.cursor().execute(f"""INSERT INTO mathematics(expression,result) 
                                        VALUES('{self.history_expression.split('=')[0]} =',
                                        '{self.history_expression.split('=')[1]}') """)
        self.data_base()

    def click_on_number(self):  # При нажатии кнопки с цифрой
        if self.point:
            tab_val = str(self.table.value())
        else:
            tab_val = str(self.table.intValue())
        if self.operation != '':
            self.table.display('')
            self.operation, self.point = '', False
        if self.table.value() == 0.0 and not self.point:
            self.table.display(self.sender().text())
        elif self.point and tab_val[-2:] == '.0' and self.flag_zero:
            print(self.sender().text())
            if self.sender().text() == '0':
                self.table.display(tab_val)
            else:
                self.table.display(tab_val[:-1] + self.sender().text())
            self.flag_zero = False
        elif self.point and tab_val[-2:] != '.0':
            self.table.display(self.history_expression + self.sender().text())
        else:
            self.table.display(self.history_expression + self.sender().text())
        self.history_expression += self.sender().text()
        self.textBrowser.setText(self.history_expression)
        self.znaks = ''

    def math_functions(self):  # При нажатии кнопки с функцией
        self.operation = self.sender().text()
        self.function = self.sender().text()
        if self.point:
            self.oper = str(self.table.value())
        else:
            self.oper = str(self.table.intValue())
        if 'x^y' == self.operation:
            self.history_expression += f' ^ '
        else:
            self.history_expression += f' {self.operation} '
        self.textBrowser.setText(self.history_expression)

    def factorial(self):  # Вычисление и вывод факториала
        self.table.display(factorial(self.table.intValue()))
        self.history_expression += f'! = {self.table.intValue()}'
        self.textBrowser.setText(self.history_expression)
        self.now_data_bas()
        self.h_expression()

    def eq(self):
        if not self.point or '.' not in self.history_expression:
            if self.function in "*+-":
                self.table.display(eval(str(self.oper) + self.function + str(self.table.intValue())))
            elif self.function == 'x^y':
                self.table.display(eval(str(self.oper) + '**' + str(self.table.intValue())))
            elif self.function == 'log':
                self.table.display(math.log(float(self.oper), self.table.intValue()))
            else:
                self.table.display(eval(str(self.oper) + self.function + str(self.table.intValue())))
            self.history_expression += f' = {self.table.value()}'
        else:
            if self.function in "*+-":
                self.table.display(eval(str(self.oper) + self.function + str(self.table.value())))
            elif self.function == 'x^y':
                self.table.display(eval(str(self.oper) + '**' + str(self.table.value())))
            elif self.function == 'log':
                self.table.display(math.log(float(self.oper), self.table.intValue()))
            else:
                if self.function == '/' and self.table.value() > 0:
                    self.table.display(eval(str(self.oper) + self.function + str(self.table.value())))
                else:
                    self.table.display('Error')
            self.history_expression += f' = {self.table.value()}'
        self.textBrowser.setText(self.history_expression)
        self.now_data_bas()
        self.connection.commit()
        self.operation = ''
        self.h_expression()

    def clear(self):
        self.table.display('0')
        self.expression()

    def sqrt(self):  # Вычисление и вывод факториала
        self.table.display(sqrt(self.table.value()))
        if self.point:
            self.history_expression = f'√{self.history_expression } = {self.table.value()}'
        else:
            self.history_expression = f'√{self.history_expression} = {self.table.intValue()}'
        self.textBrowser.setText(self.history_expression)
        self.now_data_bas()
        self.point = True
        self.h_expression()

    def points(self):
        self.table.display(str(self.table.intValue()) + '.')
        self.history_expression += '.'
        self.textBrowser.setText(self.history_expression)
        self.point = True
        self.flag_zero = True

    def click_znak(self):
        if self.znaks == '' and str(self.table.value())[0] != '-':
            self.znaks = '-'
            if self.point:
                self.table.display(self.znaks + str(self.table.value()))
            else:
                self.table.display(self.znaks + str(self.table.intValue()))
        else:
            self.znaks = ''
            if self.point:
                self.table.display(self.znaks + str(self.table.value())[1:])
            else:
                self.table.display(self.znaks + str(self.table.intValue())[1:])
        if len(self.history_expression.split()) == 1:
            if '-' != self.history_expression[0]:
                self.history_expression = self.znaks + self.history_expression
            else:
                self.history_expression = self.history_expression[1:]
        else:
            loc = self.history_expression.split()
            if '-' not in loc[-1]:
                self.history_expression = f"{' '.join(loc[:2])} ({self.znaks}{loc[-1]})"
            else:
                self.history_expression = f"{' '.join(loc[:2])} {loc[-1][2:-1]}"
        self.textBrowser.setText(self.history_expression)

    def deled(self):  # Удаление символа числа
        if self.point:
            if str(self.table.value())[-2] == '.':
                self.table.display(str(self.table.value())[:-2])
                self.history_expression = self.history_expression[:-2]
                self.point = False
            else:
                self.table.display(str(self.table.value())[:-1])
                self.history_expression = self.history_expression[:-1]
        else:
            if len(str(self.table.intValue())) == 1:
                self.table.display('0')
                self.history_expression = self.history_expression[:-1]
            else:
                self.table.display(str(self.table.intValue())[:-1])
                self.history_expression = self.history_expression[:-1]
        self.textBrowser.setText(self.history_expression)

    def math_pow_2(self):  # Вычисление и вывод кавадарта числа
        self.table.display(eval(str(self.table.value()) + '*' + str(self.table.value())))
        if self.point:
            self.history_expression = f'{self.history_expression}^2 = {self.table.value()}'
        else:
            self.history_expression = f'{self.history_expression}^2 = {self.table.intValue()}'
        self.textBrowser.setText(self.history_expression)
        self.now_data_bas()
        self.h_expression()

    def math_pow_3(self):  # Вычисление и вывод куба числа
        self.table.display(eval(str(self.table.value()) + '**' + '3'))
        if self.point:
            self.history_expression = f'{self.history_expression}^3 = {self.table.value()}'
        else:
            self.history_expression = f'{self.history_expression}^3 = {self.table.intValue()}'
        self.textBrowser.setText(self.history_expression)
        self.now_data_bas()
        self.h_expression()

    def percent(self):
        l = len(str(self.table.value()))
        self.table.display(eval(str(self.table.value() / 100)))
        if l == 4:
            self.history_expression = self.history_expression[:-2] + f'{self.table.value()}'
        elif l == 5:
            self.history_expression = self.history_expression[:-3] + f'{self.table.value()}'
        elif l == 3:
            self.history_expression = self.history_expression[:-1] + f'{self.table.value()}'
        self.textBrowser.setText(self.history_expression)
        self.point = True

    def pi(self):
        self.table.display('3.14')
        self.history_expression += f'3.14'
        self.textBrowser.setText(self.history_expression)

    def math_sin(self):  # Вычисление и вывод sin числа
        self.table.display(round(sin(radians(self.table.value())), 3))
        self.history_expression = f'sin {self.history_expression} = {self.table.value()}'
        self.textBrowser.setText(self.history_expression)
        self.now_data_bas()
        self.h_expression()
        self.point = True

    def math_cos(self):  # Вычисление и вывод cos числа
        self.table.display(round(cos(radians(self.table.value())), 3))
        self.history_expression = f'cos {self.history_expression} = {self.table.value()}'
        self.textBrowser.setText(self.history_expression)
        self.now_data_bas()
        self.h_expression()
        self.point = True

    def math_tan(self):  # Вычисление и вывод tan числа
        self.table.display(round(tan(radians(self.table.value())), 3))
        self.history_expression = f'tan {self.history_expression} = {self.table.value()}'
        self.textBrowser.setText(self.history_expression)
        self.now_data_bas()
        self.h_expression()
        self.point = True

    def expression(self):
        self.history_expression = ''
        self.textBrowser.setText(self.history_expression)

    def h_expression(self):
        if self.point:
            self.history_expression = str(self.table.value())
        else:
            self.history_expression = str(self.table.intValue())

    def clear_baze(self):  # Очистка БД
        self.data_base()
        self.dop = MathDop()  # Вызов контекстного меню
        self.dop.show()


class MathDop(QWidget, Ui_Form):  # ToDo: Конте́кстное меню́
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


class PhCalc(QMainWindow, Ui_PhysicCalculator):  # ToDo: Раздел физика
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Начальные значения
        self.const_1 = ''
        self.const_2 = ''
        self.const_3 = ''
        self.const_4 = ''
        self.sorted_1 = ' '
        self.sorted_2 = ' '
        self.sorted_3 = ' '
        self.flag_1 = False
        self.flag_2 = False
        self.flag_3 = False
        self.flag_post = False
        self.options = 'Готовый график'
        self.initUI()

    def initUI(self):
        self.connection = sqlite3.connect("CalcBaz.sqlite")
        self.con = self.connection.cursor()
        res = self.con.execute('''SELECT сhapter FROM Physica_base''').fetchall()
        items = [x[0] for x in res]
        items = sorted(list(set(items)))
        self.comboBox.addItems(items)
        self.comboBox.currentTextChanged.connect(self.sort_1)
        self.comboBox_2.currentTextChanged.connect(self.sort_2)
        self.comboBox_3.currentTextChanged.connect(self.sort_3)
        self.comboBox_4.currentTextChanged.connect(self.option)
        self.btn_poisk.clicked.connect(self.clic_podbor)
        self.ptn_build.clicked.connect(self.build_a_graph)

    def option(self, s):  # Получение значения comboBox и оброзование фильтра БД
        self.options = s

    def sort_1(self, s):  # Получение значения comboBox и оброзование фильтра БД
        self.flag_1 = True
        self.sorted_1 = s
        self.comboBox_2.clear()
        res = self.con.execute(f"""SELECT chart FROM Physica_base WHERE сhapter = '{s}' """).fetchall()
        items = [x[0] for x in res]
        items = sorted(list(set(items)))
        self.comboBox_2.addItems(items)

    def sort_2(self, s):  # Получение значения comboBox и оброзование фильтра БД
        self.flag_2 = True
        self.sorted_2 = s
        self.comboBox_3.clear()
        res = self.con.execute(f"""SELECT zavis FROM Physica_base
                                WHERE сhapter = '{self.sorted_1}' and chart = '{s}'""").fetchall()
        items = [x[0] for x in res]
        items = list(set(items))
        self.comboBox_3.addItems(items)

    def sort_3(self, s):  # Получение значения comboBox и оброзование фильтра БД
        self.flag_3 = True
        self.sorted_3 = s

    def clic_podbor(self):
        self.bild_graph_baze()

    def bild_graph_baze(self):  # Выбор готового графика
        if self.flag_1 and self.flag_2 and self.flag_3:
            self.formula, self.const, self.id = self.con.execute(f"""SELECT formula, constants, id FROM Physica_base
                                WHERE сhapter = '{self.sorted_1}' and chart = '{self.sorted_2}'
                                and zavis = '{self.sorted_3}'""").fetchall()[-1]  # Фильтор значений БД
            self.const = self.const.split()
            res = self.con.execute(f"""SELECT formula_user FROM Physica_base WHERE id = '{self.id}'""").fetchall()[-1]
            self.textBrowser.setText(res[0])
            while len(self.const) != 4:
                self.const.append('None')
            self.label_4.setText(self.const[0])
            self.label_5.setText(self.const[1])
            self.label_6.setText(self.const[2])
            self.label_7.setText(self.const[3])
            self.flag_post = True

    def bild_graph_not_baze(self):  # Ввод графика вручную
        self.formula = self.lineEdit_5.text()
        simvor = self.lineEdit_6.text()
        self.formula = self.formula.replace(simvor, 'i')

    def constants(self):  # Константы
        self.const_1 = self.lineEdit.text()
        self.const_2 = self.lineEdit_2.text()
        self.const_3 = self.lineEdit_3.text()
        self.const_4 = self.lineEdit_4.text()

    def build_a_graph(self):  # Построение графика
        if self.options == 'Готовый график':
            if self.flag_post:
                self.constants()
                consta_1 = self.const_1
                consta_2 = self.const_2
                consta_3 = self.const_3
                consta_4 = self.const_4
                self.formula = eval(self.formula)
                self.graphicsView.clear()
                self.graphicsView.plot([i for i in range(0, 11)], [eval(self.formula) for i in range(0, 11)], pen='r')
        else:
            self.bild_graph_not_baze()
            self.graphicsView.clear()
            self.graphicsView.plot([i for i in range(0, 11)], [eval(self.formula) for i in range(0, 11)], pen='r')


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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Sections()
    ex.show()
    sys.exit(app.exec())