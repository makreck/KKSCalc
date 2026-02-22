#!/usr/bin/env python3

from modules.calculator import Calculator

if __name__ == "__main__":
    Calculator().run()

# Dependencies:
#
# pip3 install pyperclip Pillow cairosvg tkinterweb
#
# Linux:
#
# Overwrite system wide:
# sudo apt remove python3-pil python3-pil.imagetk
# sudo apt update
#
# sudo apt install -y libjpeg-dev zlib1g-dev libfreetype6-dev
# sudo apt install -y python3 python3-dev python3-pip python3-tk python3-pyperclip python3-pil python3-cairosvg
#
# python3 -m pip install --user --upgrade Pillow --break-system-packages
# python3 -m pip install --user --upgrade cairosvg --break-system-packages
# python3 -m pip install --user --upgrade tkinterweb --break-system-packages
# python3 -m pip install --user --upgrade pyperclip --break-system-packages
#
# Installer:
#
# pyinstaller --onefile --add-data="modules/images/*.png:modules/images/" main.py
