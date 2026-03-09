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
            except FileExistsError:
                pass
            except Exception as e:
                print(e)
        return res_path
    
    def get_ImageResourcePath(self, image_file = "", sub_folder=None) -> str:
        if sub_folder:
            path = "images" + sub_folder
        else:
            path = "images"
        return os.path.join(self.get_ResourcePath(path), image_file)

    def get_AppDataPath(self, folder = None, filename = "") -> str:
        data_path = os.path.dirname(os.path.abspath(__file__))
        if folder:
            data_path = os.path.join(data_path, folder)
            try:
                os.makedirs(data_path, exist_ok=True)
            except:
                pass
        return os.path.join(data_path, filename)
