from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentWindow, SplashScreen, SystemThemeListener


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.initWindow()

        # create system theme listener
        self.themeListener = SystemThemeListener(self)

        # start theme listener
        self.themeListener.start()

    def initWindow(self):
        self.resize(960, 780)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon(':/gallery/images/logo.png'))
        self.setWindowTitle('PyQt-Fluent-Widgets')

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        QApplication.processEvents()