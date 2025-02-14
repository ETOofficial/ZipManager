from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentIcon, FluentWindow

from .fileInterface import FileInterface


class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()

        # create sub interface
        self.fileInterface = FileInterface(self)


        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.fileInterface, FluentIcon.FOLDER, '文件')


    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon(':/ZipManager/images/logo.png'))
        self.setWindowTitle('PyQt-Fluent-Widgets')

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)