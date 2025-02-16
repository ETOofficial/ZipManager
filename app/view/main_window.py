from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentIcon, FluentWindow

from .fileInterface import FileInterface
from ..utils.fileinfo import remove_nested, getinfo


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
        paths = event.mimeData().text()
        paths = paths.split('\n')
        if paths[-1] == '':
            del (paths[-1])
        for i in range(len(paths)):
            paths[i] = paths[i][8:]
        print(paths)
        files_info=[]
        for i, path in enumerate(paths):
            file_info = getinfo(path)
            files_info.append({
                "path": path,
                "name": file_info["name"],
                "size": file_info["size"],
                "mtime": file_info["mtime"],
                "ctime": file_info["ctime"],
                "atime": file_info["atime"]
            })
        self.fileInterface.tableView.pathlib.extend(files_info)
        
        # 检查文件是否嵌套
        self.fileInterface.tableView.pathlib = remove_nested(self.fileInterface.tableView.pathlib, False)
        
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