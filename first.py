from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMainWindow
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5 import uic
import sys
import random
import math


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI.ui', self)
        self.pushButton.clicked.connect(self.run)
        self.all = []

    def run(self):
        x, y = random.randint(0, self.width()), random.randint(0, self.height())
        r = random.randint(1, 50)
        imgres = QImage(2 * r, 2 * r, QImage.Format_ARGB32)
        clr = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        for i in range(2 * r):
            for g in range(2 * r):
                if math.sqrt((r - i) ** 2 + (r - g) ** 2) <= r:
                    imgres.setPixel(i, g, clr.rgba())
                else:
                    imgres.setPixel(i, g, QColor(0, 0, 0, 0).rgba())
        pixmap = QPixmap.fromImage(imgres)
        res = QLabel(self)
        res.setPixmap(pixmap)
        res.move(x, y)
        res.resize(2 * r, 2 * r)
        res.show()
        self.all.append(res)


if __name__ == '__main__':
    sys.excepthook = lambda cls, exception, traceback: sys.__excepthook__(cls, exception, traceback)
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
