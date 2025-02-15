import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QTableWidgetItem, QFileDialog, QAbstractItemView
from qfluentwidgets import ScrollArea, FluentIcon, CommandBar, Action, TableWidget, RoundMenu, \
    TransparentDropDownPushButton

from ..utils.fileinfo import getinfo, remove_nested


class CustomTableWidget(TableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.pathlib = [] # 待处理的路径列表

        # 设置 tableView 为不可编辑
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # enable border
        self.setBorderVisible(True)
        self.setBorderRadius(8)
        self.setWordWrap(False)
        # 设置行数和列数
        self.len_row = len(self.pathlib)
        self.columnTitles = ["路径", "文件（夹）名", "大小", "修改日期", "创建日期", "访问日期"]
        self.len_column = len(self.columnTitles)
        self.setColumnCount(self.len_column)
        self.update()
        self.setHorizontalHeaderLabels(self.columnTitles)

    def mousePressEvent(self, event):
        index = self.indexAt(event.pos())
        row = index.row()
        column = index.column()
        if event.button() == Qt.RightButton:
            # 获取点击的单元格位置
            if index.isValid():
                print(f"Right-click on Row {row}, Column {column}")
                # 显示上下文菜单
                self.contextMenu(event, row, column)
        elif event.button() == Qt.LeftButton:
            # 处理左键点击事件
            if index.isValid():
                # 检查 Ctrl 键是否被按下
                if event.modifiers() & Qt.ControlModifier:
                    print(f"Ctrl + Left-click on Row {row}, Column {column}")
                    
                else:
                    print(f"Left-click on Row {row}, Column {column}")
                    # 你可以在这里添加更多的逻辑
                    path = self.pathlib[row]
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

    def contextMenu(self, event, row, column):
        menu = RoundMenu(parent=self)

        menu.addActions([
            Action(FluentIcon.DELETE, '移出列表'),
            Action(FluentIcon.FOLDER, '打开文件所在文件夹'),
            Action(FluentIcon.PLAY, '打开文件（夹）')
        ])

        menu.exec(event.globalPos())
        
    def remove_row(self, row):
        self.pathlib.remove(row)
        self.update()
        
    def pop_row(self, row):
        row = self.pathlib.pop(row)
        self.update()
        return row
        
    def remove_all(self):
        self.pathlib = []
        self.update()
        
    def remove_selected(self):
        select_rows = self.get_select_rows()
        for i in select_rows:
            self.pathlib.remove(self.pathlib[i])
        self.clearSelection()
        self.update()

    def update(self):
        self.len_row = len(self.pathlib)
        self.setRowCount(self.len_row)
        for i, path in enumerate(self.pathlib):
            FileInfo = getinfo(path)
            self.setItem(i, 0, QTableWidgetItem(path))
            self.setItem(i, 1, QTableWidgetItem(FileInfo["name"]))
            self.setItem(i, 2, QTableWidgetItem(FileInfo["size"]))
            self.setItem(i, 3, QTableWidgetItem(FileInfo["mtime"]))
            self.setItem(i, 4, QTableWidgetItem(FileInfo["ctime"]))
            self.setItem(i, 5, QTableWidgetItem(FileInfo["atime"]))

class FileInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.object_name = "FileInterface"
        self.setObjectName(self.object_name)
        
        

        # 创建布局实例
        self.vBoxLayout = QVBoxLayout(self)
        self.commandBar = CommandBar(self)
        # change button style
        self.commandBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        # 创建文件表格
        self.tableView = CustomTableWidget(self)

        # 添加按钮
        self.addButton(FluentIcon.PLAY, '压缩全部', )
        self.addButton(FluentIcon.PLAY, '解压全部', )
        self.commandBar.addSeparator()
        self.addButton(FluentIcon.ADD, '添加文件', self.select_file)
        self.addButton(FluentIcon.ADD, '添加文件夹', self.select_folder)
        self.commandBar.addAction(Action(FluentIcon.CHECKBOX, '全选', triggered=self.select_all, checkable=True))
        # self.addButton(FluentIcon.CHECKBOX, "全选", self.select_all, True)
        # self.addButton(FluentIcon.CHECKBOX, "反选", self.tableView.counter_selection)

        # 创建下拉按钮
        self.dropDownButton = self.createDropDownButton()
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
        
        remove_all = Action(FluentIcon.DELETE, '移出所有文件')
        remove_all.triggered.connect(self.tableView.remove_all)
        remove_selected = Action(FluentIcon.DELETE, '移出选中文件')
        remove_selected.triggered.connect(self.tableView.remove_selected)

        menu = RoundMenu(parent=self)
        menu.addActions([
            Action(FluentIcon.PLAY, '单独压缩每个文件'),
            Action(FluentIcon.PLAY, '压缩选中文件'),
            Action(FluentIcon.PLAY, '单独压缩每个选中文件'),
            Action(FluentIcon.PLAY, '解压选中文件'),
            remove_all,
            remove_selected
        ])
        button.setMenu(menu)
        
        return button       

    def addButton(self, icon, text, triggered=None):
        if triggered is None:
            triggered = lambda: print(f"\"{text}\" has been clicked")
        action = Action(icon, text, self)
        action.triggered.connect(triggered)
        self.commandBar.addAction(action)

    
        
    def select_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "All Files (*)", options=options)
        if fileName:
            print(f"选择的文件：{fileName}")
            self.tableView.pathlib.append(fileName)
            self.tableView.pathlib = remove_nested(self.tableView.pathlib)
            self.tableView.update()
            
    def select_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folderName = QFileDialog.getExistingDirectory(self, "选择文件夹", "", options=options)
        if folderName:
            print(f"选择的文件夹：{folderName}")
            self.tableView.pathlib.append(folderName)
            self.tableView.pathlib = remove_nested(self.tableView.pathlib)
            self.tableView.update()