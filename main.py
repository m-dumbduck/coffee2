import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QApplication, QDialog

from database_func import *

ALL_ROAST_DEGREES = ['Светлая', 'Средняя', 'Тёмная']
GROUND_IN_GRAINS = ['Молотый', 'В зёрнах']


class MultipleChoiceError(Exception):
    pass


class TableWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('main.ui', self)

        self.dialog = None

        self.load_database()
        self.add_button.clicked.connect(self.add)
        self.change_button.clicked.connect(self.change_elem)

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

    def add(self):
        self.dialog = AddCoffeeForm(self)
        self.dialog.show()
        self.state_label.setText('')

    def change_elem(self):
        try:
            selected = list(set([i.row() for i in self.table.selectedItems()]))
            if len(selected) != 1:
                raise MultipleChoiceError
            row_id = self.table.item(selected[0], 0).text()
            self.dialog = EditCoffeeForm(self, coffee_id=row_id)
            self.dialog.show()
            self.state_label.setText('')
        except MultipleChoiceError:
            self.state_label.setText('Чтобы изменить данные таблицы, выберете только одну строку')


class AddEditCoffeeForm(QDialog):
    def __init__(self, main_win):
        super().__init__()

        self.main_win = main_win
        uic.loadUi('addEditCoffeeForm.ui', self)

        self.return_to_main.clicked.connect(self.commit)
        self.degree_of_roast.addItems(ALL_ROAST_DEGREES)
        self.ground_in_grains.addItems(GROUND_IN_GRAINS)

    def commit(self):
        self.main_win.load_database()
        self.close()


class AddCoffeeForm(AddEditCoffeeForm):
    def __init__(self, main_win):
        super().__init__(main_win)

        self.return_to_main.setText('Добавить')

    def commit(self):
        if self.name.text() and self.description.toPlainText() and \
                self.price.text().isdigit() and self.volume.text():
            degree_of_roast = self.degree_of_roast.currentText()
            ground_in_grains = self.ground_in_grains.currentText()
            insert_new_coffee(self.name.text(), degree_of_roast, ground_in_grains,
                              self.description.toPlainText(), int(self.price.text()),
                              self.volume.text()
                              )
            super().commit()
        else:
            self.errors_label.setText('Введите корректные данные')


class EditCoffeeForm(AddEditCoffeeForm):
    def __init__(self, main_win, coffee_id):
        super().__init__(main_win)

        self.return_to_main.setText('Изменить')
        self.coffee_id = coffee_id

        inf = get_from_coffees_using_id(coffee_id=self.coffee_id)
        self.name.setText(str(inf[1]))
        self.degree_of_roast.setCurrentText(inf[2])
        self.ground_in_grains.setCurrentText(inf[3])
        self.description.setPlainText(str(inf[4]))
        self.price.setText(str(inf[5]))
        self.volume.setText(str(inf[6]))

    def commit(self):
        if self.name.text() and self.description.toPlainText() and \
                self.price.text().isdigit() and self.volume.text():
            degree_of_roast = self.degree_of_roast.currentText()
            ground_in_grains = self.ground_in_grains.currentText()
            change_coffee(self.name.text(), degree_of_roast, ground_in_grains,
                          self.description.toPlainText(), int(self.price.text()),
                          self.volume.text(), self.coffee_id
                          )
            super().commit()
        else:
            self.errors_label.setText('Введите корректные данные')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TableWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
