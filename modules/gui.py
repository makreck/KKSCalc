import sys
import platform
import math
import re
import pyperclip
import tkinter as tk
from pathlib import Path
from tkinter import ttk
from tkinter.font import Font
from tkinter import scrolledtext
from functools import partial
from enum import Enum
from PIL import Image, ImageDraw, ImageFont, ImageTk

class Gui():

    class Item(Enum):
        Cmd_onClose  = "close",
        VarList      = "var.event",
        Editor       = "editor.event"
        Result       = "result.event"
        Menu_Clear   = "menu.clear",
        Menu_Delete  = "menu.delete",
        Menu_Reset   = "menu.reset",
        Menu_Help    = "menu_help",
        Menu_License = "menu_license",
        Menu_Exit    = "menu.exit",
        TB_Sep       = "separator",
        TB_Trashcan  = "button.clear",
        TB_Delete    = "button.delete"
        TB_ReUse     = "button.reuse",
        TB_Round     = "button.round",
        TB_Copy      = "button_copy",
        TB_Dec       = "button.decimal",
        TB_Hex       = "button.hexadecimal",
        TB_Bin       = "button.binary",
        TB_Deg       = "button.degrees",
        TB_Rad       = "button.radians",

    menudef = [
        { "cascade": "File", "text": "Clear",           "id": Item.Menu_Clear,   },
        { "cascade": "File", "text": "Delete",          "id": Item.Menu_Delete,  },
        { "cascade": "File", "text": "Reset",           "id": Item.Menu_Reset,   },
        { "cascade": "File", "text": "_sep_",           "id": None               },
        { "cascade": "File", "text": "Exit",            "id": Item.Menu_Exit,    },

        { "cascade": "Help", "text": "Help commands",   "id": Item.Menu_Help,    },
        { "cascade": "Help", "text": "Display license", "id": Item.Menu_License, },
    ]

    tbdef = [
        { "id": Item.TB_Trashcan,   "text": "Clear", "path": "trashcan.png",       "image": None },
        { "id": Item.TB_Sep },

        { "id": Item.TB_Delete,     "text": "Clear", "path": "delete.png",         "image": None },
        { "id": Item.TB_ReUse,      "text": "Reuse", "path": "reuse.png",          "image": None },
        { "id": Item.TB_Round,      "text": "R.2",   "path": None,                 "image": None },

        { "id": Item.TB_Sep },
        { "id": Item.TB_Dec,        "text": "DEC",   "path": None,                 "image": None },
        { "id": Item.TB_Hex,        "text": "HEX",   "path": None,                 "image": None },
        { "id": Item.TB_Bin,        "text": "BIN",   "path": None,                 "image": None },

        { "id": Item.TB_Sep },
        { "id": Item.TB_Deg,        "text": "DEG",   "path": None,                 "image": None },
        { "id": Item.TB_Rad,        "text": "RAD",   "path": None,                 "image": None },

        { "id": Item.TB_Sep },
        { "id": Item.TB_Copy,       "text": "Copy",  "path": "copy_clipboard.png", "image": None },
    ]

    def __init__(self, callback = None):
        self.root = tk.Tk()
        #self.root.tk.call("tk", "scaling", 2.0)  # 1.0, 1.5, 2.0 ausprobieren
        #self.root.tk.call("tk", "scaling", "-displayof", ".", 2.0)
        self.screen_width  = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.callback      = callback
        self.editorFont    = Font(family="TkFixedFont", size=14, weight="bold") 
        self.displayFont   = Font(family="TkFixedFont", size=14, weight="bold") 
        self.varlistFont   = Font(family="TkFixedFont", size=10, weight="bold") 
        self.imageFont     = ImageFont.load_default()
        self.tbIconSize    = (32, 32)
        self.num_format    = "dec"
        self.reuse         = True
        self.resultValue   = 0.0
        self.var           = {}
        
    def closeWindow(self):
        self.callback(Gui.Item.Cmd_onClose, "WM_DELETE_WINDOW")
        self.root.destroy()
    
    def app_window(self, pos = {} ):
        self.check_geometry(pos)
        self.createWindow()
        self.createMenu()
        self.createToolbar()
        self.createStatusline()
        self.createPaned()
        self.set_WindowPos()
        self.set_ButtonPressed(Gui.Item.TB_Deg, True)
        self.set_ButtonPressed(Gui.Item.TB_Rad, False)
        return self

    def check_geometry(self, pos = {} ):
        width  = int(float(pos.get("width",  640)))
        height = int(float(pos.get("height", 480)))
        x      = int(float(pos.get("x",      str(int((self.screen_width  - width)  / 2)))))
        y      = int(float(pos.get("y",      str(int((self.screen_height - height) / 2)))))
        self.__pos = { "x": x, "y": y, "width": width, "height": height}
        return self.__pos

    def get_WindowPos(self) -> dict:
        geometry = self.root.geometry() 
        parts = re.findall(r'(\d+)x(\d+)\+(\d+)\+(\d+)', geometry)
        if parts:
            self.__pos = { "x": parts[0][2], "y": parts[0][3], "width": parts[0][0], "height": parts[0][1]}
        return self.__pos
        
    def set_WindowPos(self, pos = None):
        if type(pos) != dict:
            pos = self.__pos
        self.root.geometry(f"{pos["width"]}x{pos["height"]}+{pos["x"]}+{pos["y"]}")
        
    def dispatch(self):
        tk.mainloop()
        
    def createWindow(self, title="KKSCalc"):
        self.root.protocol("WM_DELETE_WINDOW", self.closeWindow)
        self.root.title(title)
        self.app_icon = ImageTk.PhotoImage(file=self.get_ImagePath("app_icon.png"))
        self.root.iconphoto(False, self.app_icon)

    def createMenu(self):
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        last_cascade = ""
        for element in Gui.menudef:
            if element["cascade"] != last_cascade:
                last_cascade = element["cascade"]
                menu_cascade = tk.Menu(self.menubar, tearoff=False)
                self.menubar.add_cascade(label=last_cascade, menu=menu_cascade)        
            if element["text"] == "_sep_":
                menu_cascade.add_separator()
            else:
                menu_cascade.add_command(label=element["text"], command=partial(self.callback, element["id"]))
        
    def createToolbar(self):
        self.toolbar = tk.Frame(self.root, bd=1, relief="sunken")
        self.toolbar.pack(side="top", fill="x")
        self.toolbarButtons = []
        col = 0        
        for element in Gui.tbdef:
            id = element["id"]
            if id == Gui.Item.TB_Sep:
                spacer = tk.Label(self.toolbar, text="")
                spacer.grid(row=0, column=col, padx=1, pady=1)
                self.toolbarButtons.append( { "id": id, "button": spacer, "image": None } )
            else:
                self.toolbar.columnconfigure(col, weight=1)
                btn = tk.Button(self.toolbar, compound="center", command=partial(self.callback, id))
                if element["path"] != None:
                    img = element["image"]
                    if img == None:
                        path = self.get_ImagePath(element["path"])
                        img = tk.PhotoImage(file=path)
                        element["image"] = img
                else:
                    img = self.text_to_photoimage(element["text"], self.tbIconSize)
                btn.configure(image=img)
                btn.grid(row=0, column=col, padx=0, pady=1)
                self.toolbarButtons.append( { "id": id, "button": btn, "image": img } )
            col += 1
        self.toolbar.columnconfigure(col, weight=999)
        self.result = tk.Label(self.toolbar, text="0.0", width=-1, height=1, anchor="e", bg="#000000", fg="#00F0F0", relief="raised", font=self.displayFont)
        self.result.grid(row=0, column=col, padx=2, pady=2, sticky="NSEW")
        self.result.bind("<Double-1>", self.handle_ResultEvent)
        
    def createPaned(self):
        self.paned = ttk.PanedWindow(self.root, orient="horizontal")
        self.paned.pack(fill="both", expand=True)
        self.frame_left = tk.Frame(self.paned, bg="lightblue")
        self.frame_left.pack(fill="both", expand=True)
        self.paned.add(self.frame_left)
        self.frame_right = tk.Frame(self.paned, bg="lightgreen")
        self.frame_right.pack(fill="both", expand=True)
        self.paned.add(self.frame_right)
        self.createVarList()
        self.createEditor()

    def createStatusline(self):
        self.statusline = tk.Label(self.root, text="OK", width=-1, height=1, padx=4, pady=2, anchor="w", bd=1, relief="sunken")
        self.statusline.pack(fill="x", side="bottom", padx=2, pady=2)
    
    def createVarList(self):
        style = ttk.Style()
        style.configure("Treeview", font=self.varlistFont)
        self.varlist = ttk.Treeview(self.frame_left, columns = ("name", "value"), show = "headings")
        self.varlist.heading("name", text = "Name")
        self.varlist.column("name", width = 64)
        self.varlist.heading("value", text = "Value")
        self.varlist.column("value", width = 192)
        self.varlist.tag_configure("even", background="#FFFFFF")
        self.varlist.tag_configure("odd",  background="#E0E0FF")
        self.varlist.bind('<Double-1>', self.handle_VarListEvent)
        self.varlist.pack(padx=4.0, pady=4.0, fill="both", expand=True)

    def createEditor(self):
        self.editor = tk.Text(self.frame_right, borderwidth=0, font=self.editorFont)
        self.editor.tag_config("negative", foreground="red")
        self.editor.tag_config("positive", foreground="blue")
        self.editor.tag_config("neutral",  foreground="gray")
        self.editor.pack(padx=4.0, pady=4.0, fill="both", expand=True)
        self.editor.bind("<Return>", self.handle_EditorEvent)

    def handle_ResultEvent(self, event):
        self.callback(Gui.Item.Result, 0.0)
        
    def handle_VarListEvent(self, event):
        itemID = self.varlist.identify_row(event.y)
        if itemID:
            value = self.varlist.item(itemID, 'values')        
            self.callback(Gui.Item.VarList, value)

    def handle_EditorEvent(self, event):
        start  = self.editor.index("insert linestart")
        end    = self.editor.index("insert")
        text   = self.editor.get(start, end).strip()
        result = self.callback(Gui.Item.Editor, text)
        self.update_Variables() 
        self.set_Status(result[1])
        return self.resultOutput(result, end, not "=" in text)

    def resultOutput(self, result: tuple, index, has_equ: bool):
        if has_equ and (result[2] == 1):
            text, colorAttrib = self.get_ResultString(result[0])
            self.result.config(text=text)
            self.editor.insert(index, text, colorAttrib)
            self.editor.insert(index, "=")
            if self.reuse:
                if text.startswith("\""):
                    text = "#" + text.strip("\"")
                end = self.editor.index("insert lineend")
                self.editor.insert(end, "\n" + text)
                return "break"
        if result[2] == 0:
            return "break"
        elif result[2] == 1:
            self.set_Result(result[0])
            return None
        else:
            return None
        
    def guiDefaultCallback(self, id: Item):
        print(f"Internal GUI callback error: {id}")

    def set_VariableContent(self, var: dict):
        self.var = var
        self.update_Variables()
        return self
        
    def update_Variables(self):
        if (type(self.var) != dict): return
        self.varlist.delete(*self.varlist.get_children())
        n = 0
        for entry in self.var.keys():
            value = self.var[entry]
            if type(value) == float or type(value) == int:
                entry_str = f"{float(value):18.9f}".rstrip("0")
                if entry_str.endswith("."):
                    entry_str = entry_str + "0"
                entry_str = entry_str.replace(" ", "\u2007")
            else:
                entry_str = str(value)
            self.varlist.insert("", "end", values=(entry, entry_str), tags=("odd") if (n % 2) == 0 else ("even"))
            n += 1

    def put_EditString(self, string: str):
        aktuelle_position = self.editor.index("insert")
        self.editor.insert(aktuelle_position, string.strip())

    def add_EditString(self, string: str):
        aktuelle_position = self.editor.index("end")
        self.editor.insert(aktuelle_position, "\n" + string.strip())

    def set_Status(self, status: str):
        self.statusline.config(text=status)
        
    def get_ResultString(self, value: float) -> str:
        if type(value) == str:
            return (f"\"{value}\"", "neutral" )
        self.resultValue = float(value)
        if self.round:
            value = round(value, 2)
        if self.num_format == "bin":
            result = self.float2fractional(value, 2, 8 if not self.round else 2)
        elif self.num_format == "hex":
            result = self.float2fractional(value, 16, 4 if not self.round else 2)
        else:
            if self.round:
                result = f"{value:.2f}"
            else:
                result = str(value)
        colorAttrib = "positive" if value >= 0 else "negative"
        return (result, colorAttrib)
    
    def set_Result(self, value: float):
        text, colorAttrib = self.get_ResultString(value)
        self.result.config(text=text)

    def get_Result(self) -> float:
        return self.resultValue
    
    def clear(self) -> float:
        self.editor.delete("1.0", "end")
        self.set_Result(0.0)
        return 0.0

    def set_ReUse(self, mode: bool):
        self.reuse = mode

    def set_Round(self, mode: bool):
        self.round = mode

    def set_ButtonPressed(self, id: Item, pressed: bool):
        for btn in self.toolbarButtons:
            if btn["id"] == id:
                button = btn["button"]
                button.configure(relief = "sunken" if pressed else "raised")
                return pressed
        return False
    
    def text_to_photoimage(self, text: str, size: tuple):
        image     = Image.new("RGBA", size, "#00000000")
        draw      = ImageDraw.Draw(image)

        os_name   = platform.system().strip().lower()
        if "linux" in os_name:
            font_path = "DejaVuSans-Bold.ttf"
        elif "windows" in os_name:
            font_path = "arialbd.ttf"
        else:
            font_path = None
        try:
            font  = ImageFont.truetype(font=font_path, size=size[1] / 2.7)
        except:
            font  = None

        size      = draw.textbbox(xy=size, text=text, font=font)
        width     = size[2] - size[0]
        height    = size[3] - size[1]
        x         = math.ceil(((size[0] - 1) - width)  / 2)
        y         = math.ceil(((size[1] - 1) - height) / 2 - 1)
        draw.text((x, y), text, font=font, fill="#0030C0")
        return ImageTk.PhotoImage(image)

    def get_ScreenContent(self) -> str:
        return self.editor.get("1.0", "end-1c")
    
    def set_ScreenContent(self, content: str):
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", content)
    
    def copyResultToClipboard(self):
        pyperclip.copy(self.result.cget("text"))

    def set_NumberFormat(self, fmt = "dec"):
        self.num_format = fmt

    def float2fractional(self, value: float, base = 16, digits = 8):
        digits = int(digits)
        base = int(base)
        if base == 2:
            fu = bin
            fmt = "b"
        elif base == 16:
            fu = hex
            fmt = "x"
        else:
            return str(value)
        whole, frac = divmod(abs(value), 1)
        if frac == 0:
            return fu(int(whole))
        frac_digits = ""
        for i in range(digits):
            frac *= base
            digit = int(frac)
            frac_digits += format(digit, fmt)
            frac -= digit
        return fu(int(whole)) + "." + frac_digits.rstrip("0")
    
    def get_ImagePath(self, image_file = "") -> str:
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            base_path = Path(sys._MEIPASS)
        else:
            base_path = Path(__file__).parent
        return str(base_path) + "/images/" + image_file

    def get_position_of(self, widget) -> tuple:
        geometry = widget.geometry() 
        parts = re.findall(r'(\d+)x(\d+)\+(\d+)\+(\d+)', geometry)
        if parts:
            return ( parts[0][2], parts[0][3], parts[0][0], parts[0][1] ) 
        return None

    def center_window(self, widget, window):
        widget.update_idletasks()
        widget_pos = self.get_position_of(widget)
        if widget_pos == None: return
        window_pos = self.get_position_of(window)
        if window_pos == None: return
        w = int(widget_pos[2])
        h = int(widget_pos[3])
        x = int(window_pos[0]) + (int(window_pos[2]) - w) // 2
        y = int(window_pos[1]) + (int(window_pos[3]) - h) // 2
        widget.geometry(f"{w}x{h}+{x}+{y}")
        widget.update_idletasks()

    def display_popup(self, title = "Message", text = "Text."):
        dialog_window = tk.Toplevel(self.root)
        dialog_window.title(title)
        dialog_window.grab_set()
        scrolled_text = scrolledtext.ScrolledText(dialog_window, wrap=tk.WORD, width=80, height=20, bg="lightgrey")
        scrolled_text.insert(tk.END, text)
        scrolled_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.center_window(dialog_window, self.root)
