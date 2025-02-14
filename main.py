import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from app.view.main_window import MainWindow

QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

# create application
app = QApplication(sys.argv)

# create main window
w = MainWindow()
w.show()

app.exec_()