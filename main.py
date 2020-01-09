from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog
import UI.main
import UI.addEditCoffeeForm
import sqlite3
import sys


class AddEdit(QDialog, UI.addEditCoffeeForm.Ui_Dialog):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        con = sqlite3.connect("data/coffee.sqlite")
        cur = con.execute("""select * from Coffee""")
        self.tableWidget.setColumnCount(len(cur.description) - 1)
        self.tableWidget.setHorizontalHeaderLabels([i[0] for i in cur.description[1:]])
        self.tableWidget.insertRow(0)
        con.close()


class Example(QMainWindow, UI.main.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        con = sqlite3.connect("data/coffee.sqlite")
        cur = con.execute("""select * from Coffee""")
        self.tableWidget.setColumnCount(len(cur.description))
        self.tableWidget.setHorizontalHeaderLabels([i[0] for i in cur.description])
        self.pushButton.clicked.connect(self.add_or_edit)
        self.pushButton_2.clicked.connect(self.delete)
        con.close()
        self.load_ids()
        self.run()

    def run(self):
        con = sqlite3.connect("data/coffee.sqlite")
        cur = con.cursor()
        try:
            result = cur.execute("""select * from Coffee""").fetchall()
            self.tableWidget.setRowCount(0)
            for ind, i in enumerate(result):
                self.tableWidget.insertRow(ind)
                for gind, g in enumerate(i):
                    self.tableWidget.setItem(ind, gind, QTableWidgetItem(str(g)))
        except:
            pass
        con.close()

    def load_ids(self):
        con = sqlite3.connect("data/coffee.sqlite")
        self.ids = [i[0] for i in con.execute('''select id from Coffee''').fetchall()]
        con.close()

    def add_or_edit(self):
        try:
            id = int(self.lineEdit.text())
        except Exception:
            return
        con = sqlite3.connect("data/coffee.sqlite")
        ask = AddEdit()
        if id in self.ids:
            bf = con.execute('''select * from Coffee where id = ?''', (id, )).fetchall()[0][1:]
            for ind, i in enumerate(bf):
                ask.tableWidget.setItem(0, ind, QTableWidgetItem(str(i)))
        ask.exec()
        if ask.Accepted:
            bf = ask.tableWidget
            try:
                bf = (bf.item(0, 0).text(), bf.item(0, 1).text(), int(bf.item(0, 2).text()), int(bf.item(0, 3).text()),
                  bf.item(0, 4).text(), int(bf.item(0, 5).text()), int(bf.item(0, 6).text()))
            except Exception:
                con.close()
                return
            con.execute('''delete from Coffee where id = ?''', (id,))
            con.execute('''insert into Coffee values(?, ?, ?, ?, ?, ?, ?, ?)''', (id, *bf))
            con.commit()
            self.load_ids()
            self.run()
        con.close()

    def delete(self):
        try:
            id = int(self.lineEdit.text())
        except Exception:
            return
        con = sqlite3.connect("data/coffee.sqlite")
        con.execute('''delete from Coffee where id = ?''', (id,))
        con.commit()
        self.load_ids()
        self.run()
        con.close()


if __name__ == '__main__':
    sys.excepthook = lambda cls, exception, traceback: sys.__excepthook__(cls, exception, traceback)
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
