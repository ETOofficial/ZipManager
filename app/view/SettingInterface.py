from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget
from qfluentwidgets import ScrollArea, SettingCardGroup, ExpandLayout, SwitchSettingCard, FluentIcon, ConfigItem

from ..common.config import ucfg, user_config


def save_cfg(key, value):
    ucfg[key] = value
    user_config.save()
    print("config saved")


class SettingInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.object_name = "SettingInterface"
        self.setObjectName(self.object_name)

        self.scrollWidget = QWidget()
        # self.scrollWidget.setObjectName('scrollWidget')
        self.expandLayout = ExpandLayout(self.scrollWidget)
        
        self.developerGroup = SettingCardGroup(self.tr("开发人员选项"), self.scrollWidget)
        self.enableDebugCard = SwitchSettingCard(
            FluentIcon.CODE,
            self.tr("启用调试"),
            self.tr("启用调试功能"),
            configItem=ConfigItem("developer", "enableDebug", ucfg["debug"]),
            parent=self.developerGroup
        )
        # self.enableDebugCharged = pyqtSignal(bool)
        self.enableDebugCard.checkedChanged.connect(lambda:save_cfg("debug", self.enableDebugCard.isChecked()))
        self.developerGroup.addSettingCards([
            self.enableDebugCard
        ])

        self.expandLayout.addWidget(self.developerGroup)

        self.initWidget()

    def initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 120, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        
    