from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QTableWidgetItem
from qfluentwidgets import ScrollArea, FluentIcon, CommandBar, Action, TableWidget


class FileInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("File")
        
        # 要处理的文件路径
        self.pathlib = ["C:/"]

        self.vBoxLayout = QVBoxLayout(self)
        self.commandBar = CommandBar(self)

        # change button style
        self.commandBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.addButton(FluentIcon.ADD, '批量压缩', )

        self.tableView = TableWidget(self)
        # enable border
        self.tableView.setBorderVisible(True)
        self.tableView.setBorderRadius(8)
        self.tableView.setWordWrap(False)
        # 设置行数和列数
        self.tableView.setRowCount(1)
        self.tableView.setColumnCount(1)
        for i, path in enumerate(self.pathlib):
            self.tableView.setItem(i, 0, QTableWidgetItem(path))
        self.tableView.setHorizontalHeaderLabels(["path"])
        
        # 布局
        self.vBoxLayout.addWidget(self.commandBar)
        self.vBoxLayout.addWidget(self.tableView)

        # 调用Drops方法
        self.setAcceptDrops(True)

    def addButton(self, icon, text, do=None):
        action = Action(icon, text, self)
        if do is None:
            do = lambda: print(f"\"{text}\" has been clicked")
        action.triggered.connect(do)
        self.commandBar.addAction(action)


    def dragEnterEvent(self, evn):
        """鼠标拖入事件"""
        path = evn.mimeData().text()
        print(path)
        # 鼠标释放函数事件
        evn.accept()

    def dropEvent(self, evn):
        """鼠标释放事件"""
        pass

    def dragMoveEvent(self, evn):
        """鼠标移动事件"""
        pass