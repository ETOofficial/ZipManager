from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QTableWidgetItem
from qfluentwidgets import ScrollArea, FluentIcon, CommandBar, Action, TableWidget

from ..utils.fileinfo import getinfo


class FileInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.object_name = "FileInterface"
        self.setObjectName(self.object_name)
        
        self.pathlib = []

        # 创建布局实例
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout2 = QVBoxLayout(self)
        self.commandBar = CommandBar(self)


        # change button style
        self.commandBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.addButton(FluentIcon.PLAY, '批量压缩', )
        self.addButton(FluentIcon.PLAY, '批量解压', )
        self.addButton(FluentIcon.ADD, '添加文件', )

        # 创建文件表格
        self.tableView = TableWidget(self)
        # enable border
        self.tableView.setBorderVisible(True)
        self.tableView.setBorderRadius(8)
        self.tableView.setWordWrap(False)
        # 设置行数和列数
        self.len_row = len(self.pathlib)
        self.columnTitles = ["路径", "文件（夹）名", "大小", "修改日期", "创建日期", "访问日期"]
        self.len_column = len(self.columnTitles)
        self.tableView.setColumnCount(self.len_column)
        self.tableView_update()
        self.tableView.setHorizontalHeaderLabels(self.columnTitles)

    
        # 将元素加入布局
        self.vBoxLayout.addWidget(self.commandBar)
        self.vBoxLayout.addWidget(self.tableView)

        
        print(f"{self.object_name} has been inited")

    def addButton(self, icon, text, do=None):
        action = Action(icon, text, self)
        if do is None:
            do = lambda: print(f"\"{text}\" has been clicked")
        action.triggered.connect(do)
        self.commandBar.addAction(action)

    def tableView_update(self):
        self.len_row = len(self.pathlib)
        self.tableView.setRowCount(self.len_row)
        for i, path in enumerate(self.pathlib):
            FileInfo = getinfo(path)
            print(FileInfo)
            self.tableView.setItem(i, 0, QTableWidgetItem(path))
            self.tableView.setItem(i, 1, QTableWidgetItem(FileInfo["name"]))
            self.tableView.setItem(i, 2, QTableWidgetItem(FileInfo["size"]))
            self.tableView.setItem(i, 3, QTableWidgetItem(FileInfo["mtime"]))
            self.tableView.setItem(i, 4, QTableWidgetItem(FileInfo["ctime"]))
            self.tableView.setItem(i, 5, QTableWidgetItem(FileInfo["atime"]))
        print(f"{self.object_name} tableView has been update")