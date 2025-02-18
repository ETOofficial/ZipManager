from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentIcon, FluentWindow, SplashScreen, NavigationItemPosition

from app.common.config import user_config as ucfg
from app.common.debug import sleep
from app.utils.fileOperator import remove_nested, getinfo
from app.view.FileInterface import FileInterface
from app.view.SettingInterface import SettingInterface
from app.view.TaskInterface import TaskInterface


class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Zip Manager')
        self.setWindowIcon(QIcon('app/resource/images/logo.png'))

        # create splash screen and show window
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.show()

        # 设置窗口位置及大小
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.resize(int(w * ucfg.load("main_win_size_per")["w"]), int(h * ucfg.load("main_win_size_per")["h"]))
        self.move(int(w * ucfg.load("main_win_pos_per")["x"]), int(h * ucfg.load("main_win_pos_per")["y"]))
        del desktop, w, h

        # create sub interface
        self.taskInterface = TaskInterface(self)
        self.fileInterface = FileInterface(self)
        self.settingInterface = SettingInterface(self)

        self.initNavigation()

        self.setAcceptDrops(True)

        # close splash screen
        self.splashScreen.finish()

    def initNavigation(self):
        self.addSubInterface(self.taskInterface, FluentIcon.PLAY, self.tr('任务'))
        self.addSubInterface(self.fileInterface, FluentIcon.FOLDER, self.tr('文件'))
        self.addSubInterface(self.settingInterface, FluentIcon.SETTING, self.tr('设置'), NavigationItemPosition.BOTTOM)
        if ucfg.load("enable_debug"):
            sleep(self)

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
            del paths[-1]
        for i in range(len(paths)):
            paths[i] = paths[i][8:]
        print(paths)
        files_info = []
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
        self.fileInterface.tableView.pathinfolib.extend(files_info)
        self.stackedWidget.setCurrentWidget(self.fileInterface)

        # 检查文件是否嵌套
        self.fileInterface.tableView.pathinfolib = remove_nested(self.fileInterface.tableView.pathinfolib)

        self.fileInterface.tableView.__update()

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
