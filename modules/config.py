import sys
import json
from modules.math_wrapper import MathWrapper
from pathlib import Path

class Config:
    __default_main_window = { "x": 64, "y": 64, "width": 640, "height": 480, }

    def __init__(self):
        self.init()
        self.path = self.get_AppPath("/config.json")

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
        self.configData["screen"] = content
        return self

    def get_ScreenContent(self) -> str:
        return self.configData.get("screen", "")

    def set_round(self, mode: bool) -> bool:
        self.configData["round"] = mode
        return mode

    def get_round(self) -> bool:
        return self.configData.get("round", False)

    def set_reuse(self, mode: bool) -> bool:
        self.configData["reuse"] = mode
        return mode

    def get_reuse(self) -> bool:
        return self.configData.get("reuse", False)
        
    def set_NumberFormat(self, fmt: str):
        self.configData["numformat"] = fmt
        
    def get_NumberFormat(self) -> str:
        return self.configData.get("numformat", "dec")
        
    def get_AppPath(self, filename = "") -> Path:
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            path = str(Path(sys._MEIPASS))
        else:
            path = str(Path(__file__).resolve().parent)
        return path + filename
