import json
import sys
from plistlib import loads

from qfluentwidgets import ConfigItem, QConfig, BoolValidator

def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000

# class Config(QConfig):
#     """ Config of application """
# 
#     # main window
#     micaEnabled = ConfigItem("MainWindow", "MicaEnabled", isWin11(), BoolValidator())
    
class UserConfig:
    def __init__(self):
        self.CONFIG_PATH = "app/configs/configs.json"
        self.config = None
        self.load()
        
    def load(self):
        with open(self.CONFIG_PATH, "r") as f:
            self.config = json.load(f)
            
    def show(self, indent=4):
        print(json.dumps(self.config, indent=indent))

user_config = UserConfig()
user_config = user_config.config
# cfg = Config()