import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QMainWindow
from PyQt5 import QtWidgets

from demo import *

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

if __name__ == '__main__':
    # 读取配置文件
    with open('configs.json', 'r') as f:
        configs = json.load(f)
        print(json.dumps(configs, indent=4, sort_keys=True))
        
    # 创建Qt应用程序实例
    app = QApplication(sys.argv)

    # 主窗口
    main_win = MainWindow()

    # 获取屏幕的分辨率
    screen = QDesktopWidget().screenGeometry()
    
    main_win.resize(
        int(screen.width() * configs["main_win_size_per"]["width"]),
        int(screen.height() * configs["main_win_size_per"]["height"])
    )
    main_win.move(
        int(screen.width() * configs["main_win_pos_per"]["x"]),
        int(screen.height() * configs["main_win_pos_per"]["y"])
    )
    
    main_win.show()
    
    # 运行Qt应用程序
    sys.exit(app.exec_())
