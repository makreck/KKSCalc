import sys, os, json
from modules.math_wrapper import MathWrapper
from pathlib import Path

class Config:
    __default_main_window = { "x": 64, "y": 64, "width": 1024, "height": 640, "sashpos": 432, }

    def __init__(self):
        self.init()
        self.path = self.get_AppPath(filename="config.json")

    def init(self):
        self.configData = {
            "MainWindow": Config.__default_main_window,
            "AngleMode": MathWrapper.AngleMode.DEG.value,
        }
        return self

    def load(self):
        try:
            with open(self.path) as file_stream:
                self.configData = json.load(file_stream)
        except Exception as e:
            pass
        return self
    
    def save(self):
        try:
            with open(self.path, "w") as file_stream:
                json.dump(self.configData, file_stream, sort_keys=True, indent=4)
        except Exception as e:
            pass
        return self

    def get_WindowPos(self, wnd_name = "MainWindow"):
        return self.configData.get(wnd_name, Config.__default_main_window)

    def set_WindowPos(self, wnd_name = "MainWindow", window = __default_main_window):
        self.configData[wnd_name] = window
        return self

    def set_VariableContent(self, vars: dict):
        self.configData["Variables"] = vars
        return self
    
    def get_VariableContent(self) -> dict:
        return self.configData.get("Variables", {})

    def get_AngleMode(self) -> MathWrapper.AngleMode:
        mode = self.configData.get("AngleMode", MathWrapper.AngleMode.DEG.value[0])
        name = mode[0]
        amode = MathWrapper.AngleMode((name,))
        return amode

    def set_AngleMode(self, amode = MathWrapper.AngleMode.DEG):
        self.configData["AngleMode"] = amode.value
        return self
    
    def set_ScreenContent(self, content: str):
        self.configData["Screen"] = content
        return self

    def get_ScreenContent(self) -> str:
        return self.configData.get("Screen", "")

    def set_Round(self, mode: bool) -> bool:
        self.configData["Round"] = mode
        return mode

    def get_Round(self) -> bool:
        return self.configData.get("Round", False)

    def set_ReUse(self, mode: bool) -> bool:
        self.configData["ReUse"] = mode
        return mode

    def get_ReUse(self) -> bool:
        return self.configData.get("ReUse", False)
        
    def set_NumberFormat(self, fmt: str):
        self.configData["NumFormat"] = fmt
        
    def get_NumberFormat(self) -> str:
        return self.configData.get("NumFormat", "dec")
        
    def get_AppPath(self, folder = "", filename = "") -> Path:
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            self.root_path = str(Path(sys._MEIPASS))
        else:
            self.root_path = str(Path(__file__).resolve().parent)

        path = os.path.join(self.root_path, folder)
        try:
            os.makedirs(path)
        except:
            pass

        return os.path.join(path, filename)

    def get_Display(self) -> float:
        return self.configData.get("Display", 0.0)

    def set_Display(self, value: float):
        self.configData["Display"] = value
    