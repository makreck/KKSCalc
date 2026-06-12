# ==============================================================================
#
#  PROJECT:     "KKSCalc" KKS Desktop Calculator Tool
#  COPYRIGHT:   (C)2025-2026 KKS-Elektronik,  M. Kreck, <makreck@googlemail.com>
#
#  This program is free software: you can redistribute it and/or modify it under
#  the terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  This program is distributed in the hope that it will be useful,   but WITHOUT
#  ANY WARRANTY, without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE, see the GNU General Public License for details.
#
#  You should have received a copy of the  GNU General Public License along with
#  this program. If not, see <https://www.gnu.org/licenses/>.
#  
#  ==============================================================================

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
