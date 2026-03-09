#!/usr/bin/env python3

from modules.calculator import Calculator

if __name__ == "__main__":
    Calculator().run()

# Python dependencies:
#
#   pip3 install pyperclip Pillow cairosvg tkinterweb
#
# Linux:
#
#    Clipboard:
#       sudo apt-get install xclip
#
#    Overwrite system wide:
#       sudo apt remove python3-pil python3-pil.imagetk
#       sudo apt update
#       sudo apt install -y libjpeg-dev zlib1g-dev libfreetype6-dev python3 python3-dev python3-pip python3-tk python3-pyperclip python3-pil python3-cairosvg
#
#    python3 -m pip install --user --upgrade Pillow --break-system-packages
#    python3 -m pip install --user --upgrade cairosvg --break-system-packages
#    python3 -m pip install --user --upgrade tkinterweb --break-system-packages
#    python3 -m pip install --user --upgrade pyperclip --break-system-packages
#
# Python installer:
#   pyinstaller --onefile --add-data="modules/images/*.png:modules/images" --hidden-import=PIL._tkinter_finder --hidden-import=tkinter main.py
#   pyinstaller --onedir --noconsole --add-data="modules/images/*.png:modules/images" --hidden-import=PIL._tkinter_finder --hidden-import=tkinter main.py
