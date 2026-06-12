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

#!/usr/bin/env python3

from modules.calculator import Calculator

if __name__ == "__main__":
    Calculator().run()

# Python dependencies:
#
#   pip3 install pyperclip Pillow tkinterweb pyinstaller
#
# Windows
#   pip3 install svglib reportlab
#
# Linux:
#   pip3 install cairosvg
#
#   Clipboard:
#       sudo apt install -y xclip libjpeg-dev zlib1g-dev libfreetype-dev python3 python3-dev python3-pip python3-tk python3-pyperclip python3-pil python3-cairosvg
#
#   Overwrite system wide (possibly dangerous):
#       python3 -m pip install --user --upgrade Pillow cairosvg tkinterweb pyperclip --break-system-packages
#
# Python installer:
#   pyinstaller --onedir --noconsole --add-data="modules/*:modules/*" --hidden-import=PIL._tkinter_finder --hidden-import=tkinter main.py
