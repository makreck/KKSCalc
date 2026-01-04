from modules.calculator import Calculator
        
if __name__ == "__main__":
    Calculator().run()

# Make an executable:
#  pip install pyinstaller
#  pyinstaller --hidden-import=PIL._tkinter_finder --onefile --add-data "modules/images/*.png:images" main.py
