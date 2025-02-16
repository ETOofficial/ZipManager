from qfluentwidgets import ScrollArea


class SettingInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.object_name = "SettingInterface"
        self.setObjectName(self.object_name)