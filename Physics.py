import sqlite3
from ph_calc import Ui_PhysicCalculator
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QTableWidgetItem, QWidget


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
