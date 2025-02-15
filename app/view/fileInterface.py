import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QTableWidgetItem, QFileDialog, QAction, QAbstractItemView
from qfluentwidgets import ScrollArea, FluentIcon, CommandBar, Action, TableWidget, RoundMenu, MenuAnimationType, \
    TransparentDropDownPushButton, setFont

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
            row = index.row()
            column = index.column()
            if index.isValid():
                # 检查 Ctrl 键是否被按下
                if event.modifiers() & Qt.ControlModifier:
                    print(f"Ctrl + Left-click on Row {row}, Column {column}")
                    
                else:
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
        path = self.parent().pathlib[row]
        if index.isValid():
            # 检查 Ctrl 键是否被按下
            if event.modifiers() & Qt.ControlModifier:
                print(f"Ctrl + Double-click on Row {row}, Column {column}")
                # self.parent().add_select_path(path)
                # 弹出确认窗口：打开所有选中的文件
            else:
                print(f"Double-click on Row {row}, Column {column}")
                # 你可以在这里添加更多的逻辑
                print(f"Double-clicked path: {path}")
                if os.path.isfile(path):
                    os.startfile(path)
                elif os.path.isdir(path):
                    os.startfile(path)
                else:
                    print("Invalidpath")
        super().mouseDoubleClickEvent(event)
        
    def get_select_rows(self):
        rows = []
        selected_indexes = self.selectedIndexes()
        for index in selected_indexes:
            row = index.row()
            column = index.column()
            if column == 1:
                rows.append(row)
        return tuple(rows)

    # def counter_selection(self):
    #     """反选"""
    #     select_rows = self.get_select_rows()
    #     self.clearSelection()
    #     for row in range(self.rowCount()):
    #         if row not in select_rows:
    #             self.setRangeSelected(, True)

class FileInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.object_name = "FileInterface"
        self.setObjectName(self.object_name)
        
        self.pathlib = [] # 待处理的路径列表

        # 创建布局实例
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout2 = QVBoxLayout(self)
        self.commandBar = CommandBar(self)
        self.dropDownButton = self.createDropDownButton()

        # change button style
        self.commandBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        # 创建文件表格
        self.tableView = CustomTableWidget(self)
        # 设置 tableView 为不可编辑
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
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

        # 添加按钮
        self.addButton(FluentIcon.PLAY, '压缩全部', )
        self.addButton(FluentIcon.PLAY, '解压全部', )
        self.commandBar.addSeparator()
        self.addButton(FluentIcon.ADD, '添加文件', self.select_file)
        self.addButton(FluentIcon.ADD, '添加文件夹', self.select_folder)
        self.commandBar.addAction(Action(FluentIcon.CHECKBOX, '全选', triggered=self.select_all, checkable=True))
        # self.addButton(FluentIcon.CHECKBOX, "全选", self.select_all, True)
        # self.addButton(FluentIcon.CHECKBOX, "反选", self.tableView.counter_selection)

        # add custom widget
        self.commandBar.addWidget(self.dropDownButton)

        
    
        # 将元素加入布局
        self.vBoxLayout.addWidget(self.commandBar)
        self.vBoxLayout.addWidget(self.tableView)

        
        print(f"{self.object_name} has been inited")

    def select_all(self, isChecked):
        if isChecked:
            self.tableView.selectAll()
        else:
            self.tableView.clearSelection()

    def createDropDownButton(self):
        button = TransparentDropDownPushButton('其它选项', self, FluentIcon.MORE)
        button.setFixedHeight(34)
        setFont(button, 12)

        menu = RoundMenu(parent=self)
        menu.addActions([
            Action(FluentIcon.COPY, 'Copy'),
            Action(FluentIcon.CUT, 'Cut'),
            Action(FluentIcon.PASTE, 'Paste'),
            Action(FluentIcon.CANCEL, 'Cancel'),
            Action('Select all'),
        ])
        button.setMenu(menu)
        return button       

    def addButton(self, icon, text, triggered=None):
        if triggered is None:
            triggered = lambda: print(f"\"{text}\" has been clicked")
        action = Action(icon, text, self)
        action.triggered.connect(triggered)
        self.commandBar.addAction(action)

    def tableView_update(self):
        self.len_row = len(self.pathlib)
        self.tableView.setRowCount(self.len_row)
        for i, path in enumerate(self.pathlib):
            FileInfo = getinfo(path)
            # print(FileInfo)
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
            
    def remove_file(self, row):
        self.pathlib.pop(row)
        self.tableView_update()
        print(f"{self.object_name} file has been removed")