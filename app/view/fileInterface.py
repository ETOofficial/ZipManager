from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QVBoxLayout, QTableWidgetItem, QWidget, QLabel, QSpacerItem, QSizePolicy, QFrame, \
    QApplication
from qfluentwidgets import ScrollArea, FluentIcon, CommandBar, Action, TableWidget, TitleLabel, CardWidget


class FileInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.object_name = "FileInterface"
        self.setObjectName(self.object_name)

        # 要处理的文件路径
        self.pathlib = ["C:/"]

        # 创建布局实例
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout2 = QVBoxLayout(self)
        self.commandBar = CommandBar(self)
        # self.spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)


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
        self.row = 1
        self.column = 1
        self.tableView.setRowCount(self.row)
        self.tableView.setColumnCount(self.column)
        for i, path in enumerate(self.pathlib):
            self.tableView.setItem(i, 0, QTableWidgetItem(path))
        self.tableView.setHorizontalHeaderLabels(["path"])

        # self.dropArea = QLabel(self)
        # self.dropArea.setText("拖拽文件到此处")
        # self.dropArea.setMinimumHeight(50)
    
    
        # 将元素加入布局
        self.vBoxLayout.addWidget(self.commandBar)
        self.vBoxLayout.addWidget(self.tableView)
        # self.vBoxLayout.addItem(self.spacer)
        # self.vBoxLayout.addWidget(self.dropArea)

        

        # 调用Drops方法
        # self.setAcceptDrops(True)
        # self.dropArea.setAcceptDrops(True)
        
        print(f"{self.object_name}初始化结束")

    def addButton(self, icon, text, do=None):
        action = Action(icon, text, self)
        if do is None:
            do = lambda: print(f"\"{text}\" has been clicked")
        action.triggered.connect(do)
        self.commandBar.addAction(action)

    