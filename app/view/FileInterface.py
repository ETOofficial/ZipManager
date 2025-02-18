import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QTableWidgetItem, QFileDialog, QAbstractItemView, QLabel
from qfluentwidgets import ScrollArea, FluentIcon, CommandBar, Action, TableWidget, RoundMenu, \
    TransparentDropDownPushButton, CommandButton

from app.utils.fileOperator import remove_nested, dictList_to_listList, getinfo


class CustomTableWidget(TableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.pathinfolib:list[dict] = [] # 待处理的路径信息列表

        # 设置 tableView 为不可编辑
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # enable border
        self.setBorderVisible(True)
        self.setBorderRadius(8)
        self.setWordWrap(False)
        # 设置行数和列数
        self.len_row = len(self.pathinfolib)
        self.columnTitles = [self.tr("路径"), self.tr("文件（夹）名"), self.tr("大小"), self.tr("修改日期"), self.tr("创建日期"), self.tr("访问日期")]
        self.columnKeys = ["path", "name", "size", "mtime", "ctime", "atime"]
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
                    path = self.pathinfolib[row]
                    print(f"Selected path: {path}")
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        # 获取双击的单元格位置
        index = self.indexAt(event.pos())
        row = index.row()
        column = index.column()
        path = self.parent().pathinfolib[row]["path"]
        if index.isValid():
            # 检查 Ctrl 键是否被按下
            if event.modifiers() & Qt.ControlModifier:
                print(f"Ctrl + Double-click on Row {row}, Column {column}")
                # TODO 弹出确认窗口：打开所有选中的文件
            else:
                print(f"Double-click on Row {row}, Column {column}")
                # 你可以在这里添加更多的逻辑
                print(f"Double-clicked path: {path}")
                if os.path.isfile(path) or os.path.isdir(path):
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

    # TODO 反选功能
    # def counter_selection(self):
    #     """反选"""
    #     select_rows = self.get_select_rows()
    #     self.clearSelection()
    #     for row in range(self.rowCount()):
    #         if row not in select_rows:
    #             self.setRangeSelected(, True)

    def contextMenu(self, event, row, column):
        menu = RoundMenu(parent=self)
        
        remove = Action(FluentIcon.DELETE, self.tr('移出列表'))
        remove.triggered.connect(lambda: self.remove_row(row))
        remove_all = Action(FluentIcon.DELETE, self.tr('移出所有文件'))
        remove_all.triggered.connect(self.remove_all)
        remove_selected = Action(FluentIcon.DELETE, self.tr('移出选中文件'))
        remove_selected.triggered.connect(self.remove_selected)
        open_dir = Action(FluentIcon.FOLDER, self.tr('打开文件所在位置'))
        open_dir.triggered.connect(lambda: os.startfile(os.path.dirname(self.pathinfolib[row]["path"])))
        open_file = Action(FluentIcon.PLAY, '打开文件（夹）')
        # TODO
        
        menu.addActions([
            remove,
            remove_all,
            remove_selected,
            open_dir,
            open_file
        ])

        menu.exec(event.globalPos())
        
    def remove_row(self, row):
        del(self.pathinfolib[row])
        self.update()
        
    def pop_row(self, row):
        row = self.pathinfolib.pop(row)
        self.update()
        return row
        
    def remove_all(self):
        # TODO 弹出确定窗口
        self.pathinfolib = []
        self.update()
        
    def remove_selected(self):
        select_rows = self.get_select_rows()
        for i in select_rows:
            self.pathinfolib.remove(self.pathinfolib[i])
        self.clearSelection()
        self.update()

    def update(self):
        self.len_row = len(self.pathinfolib)
        if self.len_row == 0:
            self.parent().add_label.show()
            self.hide()
        else:
            self.parent().add_label.hide()
            self.show()
        self.setRowCount(self.len_row)
        list_info = dictList_to_listList(self.pathinfolib, self.columnKeys)
        for i in range(self.len_row):
            for j in range(self.len_column):
                self.setItem(i, j, QTableWidgetItem(str(list_info[i][j])))
                

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
        
        self.add_label = QLabel(self.tr('拖入以添加文件（夹）'))
        self.add_label.setAlignment(Qt.AlignCenter)

        # 创建文件表格
        self.tableView = CustomTableWidget(self)

        # 添加按钮
        self.compress_all_button = self.addButton(FluentIcon.PLAY, self.tr('压缩全部'), )
        self.unzip_all_button = self.addButton(FluentIcon.PLAY, self.tr('解压全部'), )
        self.commandBar.addSeparator()
        self.add_file_button = self.addButton(FluentIcon.ADD, self.tr('添加文件'), self.select_file)
        self.add_folder_button = self.addButton(FluentIcon.ADD, self.tr('添加文件夹'), self.select_folder)
        self.select_all_button = self.commandBar.addAction(Action(FluentIcon.CHECKBOX, self.tr('全选'), triggered=self.select_all, checkable=True))
        # self.addButton(FluentIcon.CHECKBOX, "全选", self.select_all, True)
        # self.addButton(FluentIcon.CHECKBOX, "反选", self.tableView.counter_selection)

        # 创建下拉按钮
        self.dropDownButton = self.createDropDownButton()
        # add custom widget
        self.commandBar.addWidget(self.dropDownButton)

        
    
        # 将元素加入布局
        self.vBoxLayout.addWidget(self.commandBar)
        self.vBoxLayout.addWidget(self.tableView)
        self.vBoxLayout.addWidget(self.add_label)

        if len(self.tableView.pathinfolib) == 0:
            self.compress_all_button.setEnabled(False)
            self.unzip_all_button.setEnabled(False)
            self.tableView.hide()
            self.add_label.show()
        
        print(f"{self.object_name} has been inited")

    def select_all(self, isChecked):
        if isChecked:
            self.tableView.selectAll()
        else:
            self.tableView.clearSelection()

    def createDropDownButton(self):
        button = TransparentDropDownPushButton(self.tr('其它选项'), self, FluentIcon.MORE)
        
        remove_all = Action(FluentIcon.DELETE, self.tr('移出所有文件'))
        remove_all.triggered.connect(self.tableView.remove_all)
        remove_selected = Action(FluentIcon.DELETE, self.tr('移出选中文件'))
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

    def addButton(self, icon, text, triggered=None) -> CommandButton:
        if triggered is None:
            triggered = lambda: print(f"\"{text}\" has been clicked")
        action = Action(icon, text, self)
        action.triggered.connect(triggered)
        return self.commandBar.addAction(action)

    
        
    def select_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, self.tr("选择文件"), "", "All Files (*)", options=options)
        if file_path:
            print(f"选择的文件：{file_path}")
            self.tableView.pathinfolib.append({**{"path": file_path}, **getinfo(file_path)})
            self.tableView.pathinfolib = remove_nested(self.tableView.pathinfolib)
            self.tableView.update()
            
    def select_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path = QFileDialog.getExistingDirectory(self, self.tr("选择文件夹"), "", options=options)
        if file_path:
            print(f"选择的文件夹：{file_path}")
            self.tableView.pathinfolib.append({**{"path": file_path}, **getinfo(file_path)})
            self.tableView.pathinfolib = remove_nested(self.tableView.pathinfolib)
            self.tableView.update()