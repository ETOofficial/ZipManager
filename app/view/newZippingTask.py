from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout
from qfluentwidgets import ScrollArea, FolderListDialog, FluentWindow, CommandBar, FluentIcon, Action, MessageBoxBase, \
    SubtitleLabel


class NewZippingTask(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('新建处理任务', self)

        # self.hBoxLayout = QHBoxLayout(self)
        # self.commandBar = CommandBar(self)
        # # self.dropDownButton = self.createDropDownButton()
        # 
        # self.hBoxLayout.addWidget(self.commandBar, 0)
        # 
        # # change button style
        # self.commandBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        # # self.commandBar.setMenuDropDown(False)
        # # self.commandBar.setButtonTight(True)
        # # setFont(self.commandBar, 14)
        # 
        # self.addButton(FluentIcon.ADD, '添加')

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)

        # change the text of button
        self.yesButton.setText('确定')
        self.cancelButton.setText('取消')

        self.widget.setMinimumWidth(350)

    def addButton(self, icon, text, do=None):
        action = Action(icon, text, self)
        if do is None:
            do = lambda: print(f"\"{text}\" has been clicked")
        action.triggered.connect(do)
        self.commandBar.addAction(action)
        