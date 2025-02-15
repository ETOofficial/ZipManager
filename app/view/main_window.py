import os.path

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QTableWidgetItem
from qfluentwidgets import FluentIcon, FluentWindow

from .fileInterface import FileInterface

from ..utils.fileinfo import remove_nested

class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()

        # create sub interface
        self.fileInterface = FileInterface(self)

        self.initWindow()
        self.initNavigation()
        
        
        

    def initNavigation(self):
        self.addSubInterface(self.fileInterface, FluentIcon.FOLDER, '文件')


    def initWindow(self):
        
        # self.setWindowIcon(QIcon(':/ZipManager/images/logo.png'))
        self.setWindowTitle('PyQt-Fluent-Widgets')
        self.resize(900, 700)
        self.setAcceptDrops(True)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def dragEnterEvent(self, evn):
        """鼠标拖入事件"""
        print("鼠标拖入")
        if evn.mimeData().hasUrls():
            evn.acceptProposedAction()
        else:
            print("拖入的数据不是URL")
            evn.ignore()

    def dropEvent(self, event):
        """鼠标释放事件"""
        print("鼠标释放")
        path = event.mimeData().text()
        path = path.split('\n')
        if path[-1] == '':
            del (path[-1])
        for i in range(len(path)):
            path[i] = path[i][8:]
        print(path)
        self.fileInterface.tableView.pathlib.extend(path)
        
        # 检查文件是否嵌套
        self.fileInterface.tableView.pathlib = remove_nested(self.fileInterface.tableView.pathlib)
        
        self.fileInterface.tableView.update()

    

    def dragMoveEvent(self, event):
        """鼠标移动事件"""
        # print("鼠标移动")
        pass

if __name__ == "__main__":
    import sys
    from PyQt5.QtCore import Qt

    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # create application
    app = QApplication(sys.argv)

    # create main window
    w = MainWindow()
    w.show()

    app.exec_()