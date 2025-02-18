import json
import sys


def is_win11():
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
        
    def load(self, key=None):
        with open(self.CONFIG_PATH, "r") as f:
            self.config = json.load(f)
        if key:
            return self.config[key]
            
    def show(self, indent=4):
        print(json.dumps(self.config, indent=indent))
        
    def save(self):
        with open(self.CONFIG_PATH, "w") as f:
            json.dump(self.config, f, indent=4)
            
    def set(self, key, value, autosave=True):
        self.config[key] = value
        if autosave:
            self.save()

user_config = UserConfig()
# cfg = Config()