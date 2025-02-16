from qfluentwidgets import ScrollArea


class TaskInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.object_name = "TaskInterface"
        self.setObjectName(self.object_name)