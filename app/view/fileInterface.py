from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QFileDialog
from qfluentwidgets import ScrollArea, FluentIcon, CommandBar, Action


class FileInterface(ScrollArea):
    """ Home interface """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("File")

        self.hBoxLayout = QHBoxLayout(self)
        self.commandBar = CommandBar(self)
        # self.dropDownButton = self.createDropDownButton()

        self.hBoxLayout.addWidget(self.commandBar, 0)

        # change button style
        self.commandBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        # self.commandBar.setMenuDropDown(False)
        # self.commandBar.setButtonTight(True)
        # setFont(self.commandBar, 14)

        self.addButton(FluentIcon.ADD, '新建', self.file_cho)

    def addButton(self, icon, text, do=None):
        action = Action(icon, text, self)
        if do is None:
            do = lambda: print(f"\"{text}\" has been clicked")
        action.triggered.connect(do)
        self.commandBar.addAction(action)
        
    def file_cho(self):
        folder = QFileDialog.getExistingDirectory(
            self, self.tr("Choose folder"), "./")