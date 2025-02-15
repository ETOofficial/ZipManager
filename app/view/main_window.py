import os.path

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QTableWidgetItem
from qfluentwidgets import FluentIcon, FluentWindow

from .fileInterface import FileInterface


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
        self.fileInterface.pathlib.extend(path)
        
        # 检查文件是否嵌套
        for i, path_i in enumerate(self.fileInterface.pathlib[:-1]):
            for j, path_j in enumerate(self.fileInterface.pathlib[i+1:]):
                if len(path_i) >= len(path_j):
                    if path_i[:len(path_j)] == path_j:
                        self.fileInterface.pathlib[i] = ""
                elif len(path_i) < len(path_j):
                    if path_j[:len(path_i)] == path_i:
                        self.fileInterface.pathlib[i+j+1] = ""
        self.fileInterface.pathlib = [i for i in self.fileInterface.pathlib if i != ""]
        
        self.fileInterface.tableView_update()

    

    def dragMoveEvent(self, event):
        """鼠标移动事件"""
        print("鼠标移动")

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