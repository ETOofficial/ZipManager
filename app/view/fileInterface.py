from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QVBoxLayout, QTableWidgetItem, QWidget, QLabel, QSpacerItem, QSizePolicy, QFrame, \
    QApplication
from qfluentwidgets import ScrollArea, FluentIcon, CommandBar, Action, TableWidget, TitleLabel, CardWidget


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
        self.row = len(self.pathlib)
        self.columnTitles = ["路径"]
        self.column = len(self.columnTitles)
        self.tableView.setRowCount(self.row)
        self.tableView.setColumnCount(self.column)
        for i, path in enumerate(self.pathlib):
            self.tableView.setItem(i, 0, QTableWidgetItem(path))
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

    