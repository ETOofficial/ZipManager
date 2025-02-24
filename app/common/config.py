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
        self.DEFAULT_CONFIG = {
            "main_win_size_per": {
                "w": 0.5,
                "h": 0.5
            },
            "main_win_pos_per": {
                "x": 0.25,
                "y": 0.25
            },
            "enable_developersettings": True,
            "enable_debug": False,
            "preprocessing_files_list": []
        }
        self.CONFIG_PATH = "app/configs/configs.json"
        self.config = None
        self.load()
        
    def load(self, key=None):
        with open(self.CONFIG_PATH, "r") as f:
            self.config = json.load(f)
        if key:
            return self.config.get(key, self.DEFAULT_CONFIG[key])
            
    def show(self, indent=4):
        print(json.dumps(self.config, indent=indent))
        
    def save(self):
        print("UserConfig has been saved.")
        with open(self.CONFIG_PATH, "w") as f:
            json.dump(self.config, f, indent=4)
            
    def set(self, key, value, autosave=True):
        print(f"{key} has been set {self.config[key]} to {value}")
        self.config[key] = value
        if autosave:
            self.save()
            
    # TODO 检查配置文件是否完整

user_config = UserConfig()
# cfg = Config()