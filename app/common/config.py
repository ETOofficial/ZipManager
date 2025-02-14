import sys

from qfluentwidgets import ConfigItem, QConfig, BoolValidator


def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000

class Config(QConfig):
    """ Config of application """

    # main window
    micaEnabled = ConfigItem("MainWindow", "MicaEnabled", isWin11(), BoolValidator())

cfg = Config()