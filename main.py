from modules.calculator import Calculator

if __name__ == "__main__":
    Calculator().run()

# Dependencies:
# pip3 install --upgrade pyperclip Pillow

# Make an executable:
#  pip install pyinstaller
#  pyinstaller --hidden-import=PIL._tkinter_finder --onefile --add-data "modules/images/*.png:images" main.py
    
# Linux:
# sudo apt install python3-tk


import tkinter as tk

# root = tk.Tk()
# root.tk.call("tk", "scaling", 2.0)  # 1.0, 1.5, 2.0 ausprobieren
# oder äquivalent:
# root.tk.call("tk", "scaling", "-displayof", ".", 2.0)

# ab hier deine Widgets
# ...
# root.mainloop()
# myfont = font.Font(family="DejaVu Sans", size=12)  # gut verfügbare TTF‑Font
# label = tk.Label(root, text="Test", font=myfont)
# label.pack()
