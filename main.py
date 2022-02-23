import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QApplication


def database_dialog(que, *inf):
    connection = sqlite3.connect('coffees.db')
    cursor = connection.cursor()
    information = cursor.execute(que, inf).fetchall()
    connection.commit()
    connection.close()
    return information


def all_inf():
    return database_dialog("""SELECT * FROM coffees""")


class TableWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('main.ui', self)
        self.setWindowTitle('Эспрессо')

        self.load_database()

    def load_database(self):
        result = all_inf()
        self.table.setRowCount(len(result))
        if result:
            titles = ['ID', 'Название сорта', 'Степень обжарки', 'Молотый/в зёрнах',
                      'Описание вкуса', 'Цена', 'Объём упаковки']
            self.table.setColumnCount(len(result[0]))
            self.table.setHorizontalHeaderLabels(titles)
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    item = QTableWidgetItem(str(val))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.table.setItem(i, j, item)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TableWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
