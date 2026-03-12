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
#   with images -> pyinstaller --onedir --noconsole --add-data="modules/images/*.png:modules/images" --hidden-import=PIL._tkinter_finder --hidden-import=tkinter main.py
#   pyinstaller --onedir --noconsole --hidden-import=PIL._tkinter_finder --hidden-import=tkinter main.py
