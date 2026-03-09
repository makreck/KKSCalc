import json
from modules.math_wrapper import MathWrapper
from modules.gui import Gui
from modules.app_tools import AppTools

class Config:
    __default_main_window = { "x": 64, "y": 64, "width": 1024, "height": 640, "sashpos": 432, }

    def __init__(self):
        self.init()
        self.path = AppTools().get_AppDataPath(filename="config.json")

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
        
    def set_NumberFormat(self, fmt: Gui.NumFormat):
        self.configData["NumFormat"] = fmt.value

    def get_NumberFormat(self) -> Gui.NumFormat:
        fmt = self.configData.get("NumFormat", Gui.NumFormat.DEC.value)
        return Gui.NumFormat[fmt]

    def get_Display(self) -> float:
        return self.configData.get("Display", 0.0)

    def set_Display(self, value: float):
        self.configData["Display"] = value
    
    def store_default_variables(self, def_variables: dict):
        self.configData["DefaultVariables"] = def_variables

    def get_default_variables(self) -> dict:
        return self.configData.get("DefaultVariables", {})

    def parse_macro_name(self, macro_name="default"):
        if not macro_name:
            macro_name = "default"
        elif type(macro_name) != str:
            macro_name = str(macro_name)
        name = macro_name.strip().lower().replace(" ", "_")
        return "Macro." + name

    def get_Macro(self, name="default"):
        return self.configData.get(self.parse_macro_name(name), [ "a=a+1", "b=a+2", "c=a+3", "d=a+b+c", ]) # Test-Macro

    def set_Macro(self, name="default", macro=[ ".res" ]):
        key = self.parse_macro_name(name)
        self.configData[key] = macro        

    def get_Macro_List(self):
        return [key[6:].lower() for key in self.configData.keys() if key.startswith("Macro.")]

    def delete_Macro(self, name=None):
        if name == None: return
        key = self.parse_macro_name(name)
        deleted_macro = self.configData.pop(key, None)
        print(f"Delete macro \"{name}\", content=\"{deleted_macro}\"")
        
