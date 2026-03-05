import os, sys

class AppTools:
    def __init__(self):
        pass
    
    def get_ResourcePath(self, folder=None) -> str:
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            res_path = sys._MEIPASS
        else:
            res_path = os.path.dirname(os.path.abspath(__file__))
        if folder:
            res_path = os.path.join(res_path, folder)
            try:
                os.makedirs(res_path)
            except:
                pass
        return res_path
    
    def get_ImageResourcePath(self, image_file = "") -> str:
        return os.path.join(self.get_ResourcePath("images/"), image_file)

    def get_AppPath(self, folder = None, filename = "") -> str:
        return os.path.join(AppTools().get_ResourcePath(folder), filename)
