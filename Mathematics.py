import sqlite3
from mat_calc import Ui_MathematicalCalculator
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from math import factorial, sqrt, sin, cos, tan, radians
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QTableWidgetItem, QWidget
from ContexMenu import MathContext


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
        self.dop = MathContext()  # Вызов контекстного меню
        self.data_base()
        self.dop.show()
