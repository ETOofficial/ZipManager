import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QVBoxLayout, QTableWidgetItem, QFileDialog, QAbstractItemView, QLabel
from qfluentwidgets import ScrollArea, FluentIcon, CommandBar, Action, TableWidget, RoundMenu, \
    TransparentDropDownPushButton, CommandButton, InfoBar, InfoBarPosition, MessageBox

from app.common.config import user_config as ucfg
from app.utils.fileOperator import remove_nested, dictList_to_listList, getinfo


class CustomTableWidget(TableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.pathinfolib: list[dict] = ucfg.load("preprocessing_files_list")  # 待处理的路径信息列表

        # 设置 tableView 为不可编辑
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # enable border
        self.setBorderVisible(True)
        self.setBorderRadius(8)
        self.setWordWrap(False)
        # 设置行数和列数
        self.len_row = len(self.pathinfolib)
        self.columnTitles = [self.tr("路径"), self.tr("文件（夹）名"), self.tr("大小"), self.tr("修改日期"),
                             self.tr("创建日期"), self.tr("访问日期")]
        self.columnKeys = ["path", "name", "size", "mtime", "ctime", "atime"]
        self.len_column = len(self.columnTitles)
        self.setColumnCount(self.len_column)
        self.setHorizontalHeaderLabels(self.columnTitles)
        self.unfounded_numb = self.update_table()

    def mousePressEvent(self, event):
        index = self.indexAt(event.pos())
        row = index.row()
        column = index.column()
        if event.button() == Qt.RightButton:
            # 获取点击的单元格位置
            if index.isValid():
                print(f"Right-click on Row {row}, Column {column}")
                # 显示上下文菜单
                self.__contextMenu(event, row, column)
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
        path = self.pathinfolib[row]["path"]
        if index.isValid():
            # 检查 Ctrl 键是否被按下
            if event.modifiers() & Qt.ControlModifier:
                print(f"Ctrl + Double-click on Row {row}, Column {column}")
                self.open_selected()
            else:
                print(f"Double-click on Row {row}, Column {column}")
                print(f"Double-clicked path: {path}")
                self.__openfile(path)
        super().mouseDoubleClickEvent(event)

    def open_selected(self, show_errors=True):
        """
        **PROBLEM** ``show_errors`` 默认值在 connect 调用时似乎无效
        
        :param show_errors: 是否展示错误
        :return: 错误内容
        """
        print(show_errors)
        msgbox = MessageBox(
            self.tr("打开所选文件？"),
            self.tr("无法验证文件是否安全，且可能会造成卡顿"),
            parent=self.parent()
        )
        msgbox.setClosableOnMaskClicked(True)
        if not msgbox.exec():
            return
        selected_rows = self.get_selected_rows()
        paths = [pathinfo["path"] for i, pathinfo in enumerate(self.pathinfolib) if i in selected_rows]
        errors = []
        for path in paths:
            error = self.__openfile(path, show_error=False)
            print(error)
            if error is not None:
                errors.append({"path": path, "info": error})
        if show_errors and errors is not None:
            error_info = {}
            for error in errors:
                error_info[error["info"]] = error_info.get(error["info"], 0) + 1
            print(error_info)
            error_content = ""
            for error, count in error_info.items():
                error_content += f"{error}: {count}个\n"
            error_content = error_content[:-1]
            InfoBar.error(
                self.tr("文件打开失败"),
                self.tr(f"{error_content}"),
                parent=self.parent(),
                duration=3000,
                position=InfoBarPosition.BOTTOM_RIGHT
            )
        return errors

    def __openfile(self, path, show_error=True):
        """
        
        :param path: 路径
        :param show_error: 是否展示错误
        :return: 错误内容
        """
        error = None
        if os.path.isfile(path) or os.path.isdir(path):
            try:
                os.startfile(path)
            except Exception as e:
                error = f"{e}"
                if show_error:
                    InfoBar.error(
                        self.tr("文件打开失败"),
                        self.tr(f"{e}"),
                        parent=self.parent(),
                        duration=3000,
                        position=InfoBarPosition.BOTTOM_RIGHT
                    )
        else:
            error = "unfounded"
            if show_error:
                InfoBar.error(
                    self.tr("无效路径"),
                    self.tr("文件不存在"),
                    parent=self.parent(),
                    duration=3000,
                    position=InfoBarPosition.BOTTOM_RIGHT
                )
        return error

    def get_selected_rows(self):
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

    def __contextMenu(self, event, row, column):
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
        open_file.triggered.connect(lambda :self.__openfile(self.pathinfolib[row]["path"]))
        open_selected = Action(FluentIcon.PLAY, '打开选中文件（夹）')
        open_selected.triggered.connect(lambda: self.open_selected(True))

        menu.addActions([
            remove,
            remove_all,
            remove_selected,
            open_dir,
            open_file,
            open_selected,
        ])

        menu.exec(event.globalPos())

    def remove_row(self, row):
        InfoBar.success(
            self.tr("已将文件移出列表"),
            self.tr(f"{self.pathinfolib[row]["path"]}"),
            parent=self.parent(),  # 不可是 self ，否则列表清空时则不会显示
            duration=3000,
            position=InfoBarPosition.BOTTOM_RIGHT
        )
        del self.pathinfolib[row]
        self.update_table()

    def pop_row(self, row):
        row = self.pathinfolib.pop(row)
        InfoBar.success(
            self.tr("已将文件移出列表"),
            self.tr(f"{row["path"]}"),
            parent=self.parent(),
            duration=3000,
            position=InfoBarPosition.BOTTOM_RIGHT
        )
        self.update_table()
        return row

    def remove_all(self):
        msgbox = MessageBox(
            self.tr("确定移出所有文件？"),
            self.tr("文件列表将被清空"),
            parent=self.parent()
        )
        msgbox.setClosableOnMaskClicked(True)
        if not msgbox.exec():
            return
        InfoBar.success(
            self.tr("已将文件移出列表"),
            self.tr("所有"),
            parent=self.parent(),
            duration=3000,
            position=InfoBarPosition.BOTTOM_RIGHT
        )
        self.pathinfolib = []
        self.update_table()

    def remove_selected(self):
        select_rows = self.get_selected_rows()
        InfoBar.success(
            self.tr("已将文件移出列表"),
            self.tr(f"{len(select_rows)} 个文件"),
            parent=self.parent(),
            duration=3000,
            position=InfoBarPosition.BOTTOM_RIGHT
        )
        for i in select_rows[::-1]:
            del (self.pathinfolib[i])
        self.clearSelection()
        self.update_table()

    def update_table(self):
        """
        
        :return: 不存在的文件数量
        """
        self.len_row = len(self.pathinfolib)
        unfounded_numb = 0
        # if self.len_row == 0:
        #     self.parent().add_label.show()
        #     self.hide()
        #     self.parent().compress_all_button_enable = False
        #     self.parent().unzip_all_button_enable = False
        # else:
        #     self.parent().add_label.hide()
        #     self.show()
        #     self.parent().compress_all_button_enable = True
        #     self.parent().unzip_all_button_enable = True
        self.setRowCount(self.len_row)
        list_info = dictList_to_listList(self.pathinfolib, self.columnKeys)
        for i in range(self.len_row):
            if not os.path.exists(self.pathinfolib[i]["path"]):
                is_unfounded = True
                unfounded_numb += 1
            else:
                is_unfounded = False
            for j in range(self.len_column):
                if is_unfounded:
                    item = QTableWidgetItem(str(list_info[i][j]))
                    item.setForeground(QBrush(QColor(255, 0, 0)))
                    self.setItem(i, j, item)
                else:
                    self.setItem(i, j, QTableWidgetItem(str(list_info[i][j])))
        ucfg.set("preprocessing_files_list", self.pathinfolib)
        if unfounded_numb > 0:
            InfoBar.error(
                self.tr("文件不存在"),
                self.tr(f"{unfounded_numb} 个文件"),
                parent=self.parent(),
                duration=-1,
                position=InfoBarPosition.BOTTOM_RIGHT
            )
        return unfounded_numb
    
    # def __InfoBar(self, *kwargs):
        


class FileInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.object_name = "FileInterface"
        self.setObjectName(self.object_name)
        
        self.enable_compress_all_button = True
        self.enable_unzip_all_button = True

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
        self.compress_all_button = self.__addButton(FluentIcon.PLAY, self.tr('压缩全部'), )
        self.unzip_all_button = self.__addButton(FluentIcon.PLAY, self.tr('解压全部'), )
        self.commandBar.addSeparator()
        self.add_file_button = self.__addButton(FluentIcon.ADD, self.tr('添加文件'), self.__select_file)
        self.add_folder_button = self.__addButton(FluentIcon.ADD, self.tr('添加文件夹'), self.__select_folder)
        self.select_all_button = self.commandBar.addAction(
            Action(FluentIcon.CHECKBOX, self.tr('全选'), triggered=self.__select_all, checkable=True))
        # self.addButton(FluentIcon.CHECKBOX, "全选", self.select_all, True)
        # self.addButton(FluentIcon.CHECKBOX, "反选", self.tableView.counter_selection)

        # 创建下拉按钮
        self.dropDownButton = self.__createDropDownButton()
        # add custom widget
        self.commandBar.addWidget(self.dropDownButton)

        # 将元素加入布局
        self.vBoxLayout.addWidget(self.commandBar)
        self.vBoxLayout.addWidget(self.tableView)
        self.vBoxLayout.addWidget(self.add_label)

        # 更新界面
        self.update_interface()
        
    def update_interface(self):
        if len(self.tableView.pathinfolib) == 0:
            self.tableView.hide()
            self.add_label.show()
            self.enable_compress_all_button = False
            self.enable_unzip_all_button = False
        else:
            self.tableView.show()
            self.add_label.hide()
            self.enable_compress_all_button = True
            self.enable_unzip_all_button = True

        self.compress_all_button.setEnabled(self.enable_compress_all_button)
        self.unzip_all_button.setEnabled(self.enable_unzip_all_button)
        
        self.tableView.update_table()

    def __select_all(self, isChecked):
        if isChecked:
            self.tableView.selectAll()
        else:
            self.tableView.clearSelection()

    def __createDropDownButton(self):
        # FIXME 在窗口宽度不够时， CommandBar 自带的隐藏选项无法显示“其它选项”
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

    def __addButton(self, icon, text, triggered=None) -> CommandButton:
        if triggered is None:
            triggered = lambda: print(f"\"{text}\" has been clicked")
        action = Action(icon, text, self)
        action.triggered.connect(triggered)
        return self.commandBar.addAction(action)

    def __select_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, self.tr("选择文件"), "", "All Files (*)", options=options)
        if file_path:
            print(f"选择的文件：{file_path}")
            self.tableView.pathinfolib.append({**{"path": file_path}, **getinfo(file_path)})
            self.tableView.pathinfolib = remove_nested(self.tableView.pathinfolib)
            self.tableView.update_table()

    def __select_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path = QFileDialog.getExistingDirectory(self, self.tr("选择文件夹"), "", options=options)
        if file_path:
            print(f"选择的文件夹：{file_path}")
            self.tableView.pathinfolib.append({**{"path": file_path}, **getinfo(file_path)})
            self.tableView.pathinfolib = remove_nested(self.tableView.pathinfolib)
            self.tableView.update_table()
