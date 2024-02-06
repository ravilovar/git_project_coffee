import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem
from mainWindow import Ui_MainWindow
from addEditCoffeeForm import Ui_addEditCoffeeForm


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connection = sqlite3.connect("data/coffee.sqlite")
        self.pushButton.clicked.connect(self.coffee_load)
        self.addEditFormButton.clicked.connect(self.coffee_add_edit_form)
        self.second_form = AddEditForm(self, self.connection, self.lineEdit_ID.text())

    def coffee_load(self):
        query = """SELECT * FROM Coffee"""
        res = self.connection.cursor().execute(query).fetchall()

        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)

        for i, row in enumerate(res):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))

        self.tableWidget.setHorizontalHeaderLabels(['ID', 'Сорт', 'Обжарка', 'Помол', 'Вкус', 'Цена', 'Объем'])

    def closeEvent(self, event):
        self.connection.close()

    def coffee_add_edit_form(self):
        self.second_form = AddEditForm(self, self.connection, self.lineEdit_ID.text())
        if int(self.lineEdit_ID.text()) == 0:
            self.second_form.setWindowTitle('Новая запись')
        else:
            self.second_form.setWindowTitle('Изменить запись')
        self.second_form.show()


class AddEditForm(QWidget, Ui_addEditCoffeeForm):
    def __init__(self, *args):
        super().__init__()
        self.connection = args[1]
        self.coffee_ID = int(args[2])
        self.setupUi(self)
        self.saveButton.clicked.connect(self.coffee_add)

    def coffee_add(self):
        cur = self.connection.cursor()
        if self.coffee_ID == 0:
            que = "INSERT INTO Coffee (Name, Roast, Ground, Taste, Price, Package) VALUES(?,?,?,?,?,?)"
        else:
            que = f"""UPDATE Coffee 
                      SET Name=?, Roast=?, Ground=?, Taste=?, Price=?, Package=?
                      WHERE ID={self.coffee_ID}"""
        cur.execute(que, (self.lineEdit_1.text(), self.lineEdit_2.text(),
                          self.lineEdit_3.text(), self.lineEdit_4.text(),
                          self.lineEdit_5.text(), self.lineEdit_6.text(),
                          )
                    )
        self.connection.commit()
        self.form_clear()
        self.hide()

    def form_clear(self):
        self.lineEdit_1.setText('')
        self.lineEdit_2.setText('')
        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')
        self.lineEdit_5.setText('')
        self.lineEdit_6.setText('')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
