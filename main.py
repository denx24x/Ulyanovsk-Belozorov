from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5 import uic
import sqlite3
import sys


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        con = sqlite3.connect("coffee.sqlite")
        cur = con.execute("""select * from Coffee""")
        self.tableWidget.setColumnCount(len(cur.description))
        self.tableWidget.setHorizontalHeaderLabels([i[0] for i in cur.description])
        con.close()
        self.run()

    def run(self):
        con = sqlite3.connect("coffee.sqlite")
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
