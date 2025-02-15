import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QTableWidgetItem, QFileDialog, QAction, QAbstractItemView
from qfluentwidgets import ScrollArea, FluentIcon, CommandBar, Action, TableWidget, RoundMenu, MenuAnimationType

from ..utils.fileinfo import getinfo, remove_nested

    # def contextMenuEvent(self, e):
    #     menu = RoundMenu(parent=self)
    #     # menu = CheckableMenu(parent=self, indicatorType=MenuIndicatorType.RADIO)
    # 
    #     # NOTE: hide the shortcut key
    #     # menu.view.setItemDelegate(MenuItemDelegate())
    # 
    #     # add actions
    #     menu.addAction(Action(FluentIcon.COPY, 'Copy'))
    #     menu.addAction(Action(FluentIcon.CUT, 'Cut'))
    #     menu.actions()[0].setCheckable(True)
    #     menu.actions()[0].setChecked(True)
    # 
    #     # add sub menu
    #     submenu = RoundMenu("Add to", self)
    #     submenu.setIcon(FluentIcon.ADD)
    #     submenu.addActions([
    #         Action(FluentIcon.VIDEO, 'Video'),
    #         Action(FluentIcon.MUSIC, 'Music'),
    #     ])
    #     menu.addMenu(submenu)
    # 
    #     # add actions
    #     menu.addActions([
    #         Action(FluentIcon.PASTE, 'Paste'),
    #         Action(FluentIcon.CANCEL, 'Undo')
    #     ])
    # 
    #     # add separator
    #     menu.addSeparator()
    #     menu.addAction(QAction(f'Select all', shortcut='Ctrl+A'))
    # 
    #     # insert actions
    #     menu.insertAction(
    #         menu.actions()[-1], Action(FluentIcon.SETTING, 'Settings', shortcut='Ctrl+S'))
    #     menu.insertActions(
    #         menu.actions()[-1],
    #         [Action(FluentIcon.HELP, 'Help', shortcut='Ctrl+H'),
    #          Action(FluentIcon.FEEDBACK, 'Feedback', shortcut='Ctrl+F')]
    #     )
    #     menu.actions()[-2].setCheckable(True)
    #     menu.actions()[-2].setChecked(True)
    # 
    #     # show menu
    #     menu.exec(e.globalPos(), aniType=MenuAnimationType.DROP_DOWN)

class CustomTableWidget(TableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            # 获取点击的单元格位置
            index = self.indexAt(event.pos())
            if index.isValid():
                row = index.row()
                column = index.column()
                print(f"Right-click on Row {row}, Column {column}")
                # # 显示上下文菜单
                # self.showContextMenu(event.globalPos(), row, column)
        elif event.button() == Qt.LeftButton:
            # 处理左键点击事件
            index = self.indexAt(event.pos())
            if index.isValid():
                row = index.row()
                column = index.column()
                print(f"Left-click on Row {row}, Column {column}")
                # 你可以在这里添加更多的逻辑
                path = self.parent().pathlib[row]
                print(f"Selected path: {path}")
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        # 获取双击的单元格位置
        index = self.indexAt(event.pos())
        row = index.row()
        column = index.column()
        # 检查 Ctrl 键是否被按下
        if index.isValid():
            if event.modifiers() & Qt.ControlModifier:
                print("Ctrl + Double-click detected")
                # 你可以在这里添加更多的逻辑
            else:
                print(f"Double-click on Row {row}, Column {column}")
                # 你可以在这里添加更多的逻辑
                path = self.parent().pathlib[row]
                print(f"Double-clicked path: {path}")
                if os.path.isfile(path):
                    os.startfile(path)
                elif os.path.isdir(path):
                    os.startfile(path)
                else:
                    print("Invalidpath")
        super().mouseDoubleClickEvent(event)

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
        self.addButton(FluentIcon.ADD, '添加文件', self.select_file)
        self.addButton(FluentIcon.ADD, '添加文件夹', self.select_folder)

        # 创建文件表格
        self.tableView = CustomTableWidget(self)
        # 设置 tableView 为不可编辑
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # # 连接 cellClicked 信号到自定义槽函数
        # self.tableView.cellClicked.connect(self.on_cell_clicked)
        # self.tableView.cellDoubleClicked.connect(self.on_cell_double_clicked)
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
        
    def select_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "All Files (*)", options=options)
        if fileName:
            print(f"选择的文件：{fileName}")
            self.pathlib.append(fileName)
            self.pathlib = remove_nested(self.pathlib)
            self.tableView_update()
        
            
    def select_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folderName = QFileDialog.getExistingDirectory(self, "选择文件夹", "", options=options)
        if folderName:
            print(f"选择的文件夹：{folderName}")
            self.pathlib.append(folderName)
            self.pathlib = remove_nested(self.pathlib)
            self.tableView_update()

    # def on_cell_clicked(self, row, column):
    #     # 处理行点击事件
    #     print(f"Row {row}, Column {column} clicked")
    #     # 你可以在这里添加更多的逻辑
    #     path = self.pathlib[row]
    #     print(f"Selected path: {path}")
    #     
    # def on_cell_double_clicked(self, row, column):
    #     # 处理双击事件
    #     print(f"Row {row}, Column {column} double clicked")
    #     # 你可以在这里添加更多的逻辑
    #     path = self.pathlib[row]
    #     print(f"Selected path: {path}")
    #     if os.path.isfile(path):
    #         os.startfile(path)
    #     elif os.path.isdir(path):
    #         os.startfile(path)
    #     else:
    #         print("Invalidpath")
            
    def remove_file(self, row):
        self.pathlib.pop(row)
        self.tableView_update()
        print(f"{self.object_name} file has been removed")