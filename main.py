from modules.calculator import Calculator
from modules.roman_numbers import RomanNumber

if __name__ == "__main__":
    Calculator().run()

# Dependencies:
# pip3 install --upgrade pyperclip Pillow

# Make an executable:
#  pip install pyinstaller
#  pyinstaller --hidden-import=PIL._tkinter_finder --onefile --add-data "modules/images/*.png:images" main.py
    