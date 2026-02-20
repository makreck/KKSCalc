import sys, math, platform
import pyperclip, cairosvg
import re
import tkinter as tk
from pathlib import Path
from fractions import Fraction
from tkinter import ttk
from tkinter.font import Font
from tkinter import scrolledtext
from functools import partial
from enum import Enum
from PIL import Image, ImageDraw, ImageTk
from io import BytesIO
from modules.math_wrapper import MathWrapper
from modules.tooltip import ToolTip
from modules.scollframe import ScrollableFrame

class Gui():

    class Item(Enum):
        Cmd_onClose   = "close",
        VarList       = "var.event",
        Editor        = "editor.event"
        Result        = "result.event"
        Menu_Clear    = "menu.clear",
        Menu_Delete   = "menu.delete",
        Menu_Reset    = "menu.reset",
        Menu_Help     = "menu_help",
        Menu_License  = "menu_license",
        Menu_Copy     = "menu.copy",
        Menu_Exit     = "menu.exit",
        TB_Sep        = "separator",
        TB_Trashcan   = "button.clear",
        TB_Delete     = "button.delete"
        TB_ReUse      = "button.reuse",
        TB_Round      = "button.round",
        TB_Dec        = "button.decimal",
        TB_Hex        = "button.hexadecimal",
        TB_Bin        = "button.binary",
        TB_Frc        = "button.fraction"
        TB_Deg        = "button.degrees",
        TB_Rad        = "button.radians",
        Math_Function = 9000,

    menudef = [
        { "cascade": "File", "text": "Clear",           "id": Item.Menu_Clear,   },
        { "cascade": "File", "text": "Delete",          "id": Item.Menu_Delete,  },
        { "cascade": "File", "text": "Reset",           "id": Item.Menu_Reset,   },
        { "cascade": "File", "text": "_sep_",           "id": None               },
        { "cascade": "File", "text": "Exit",            "id": Item.Menu_Exit,    },

        { "cascade": "Edit", "text": "Copy",            "id": Item.Menu_Copy,    },

        { "cascade": "Help", "text": "Help commands",   "id": Item.Menu_Help,    },
        { "cascade": "Help", "text": "Display license", "id": Item.Menu_License, },
    ]

    def svg_trashcan(self, color_background="#4a90e2", color_text="#ffffff"):
        return  f'''
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 32 32">
                    <rect width="32" height="32" rx="4" ry="4" fill="{color_background}" stroke="#357abd" stroke-width="0"/>
                    <path transform="translate(3 3)" fill-rule="evenodd" fill="{color_text}" d="M12,13.5857864 L14.2928932,11.2928932 L15.7071068,12.7071068 L13.4142136,15 L15.7071068,17.2928932 L14.2928932,18.7071068 L12,16.4142136 L9.70710678,18.7071068 L8.29289322,17.2928932 L10.5857864,15 L8.29289322,12.7071068 L9.70710678,11.2928932 L12,13.5857864 Z M7,4 L7,3 C7,1.8954305 7.8954305,1 9,1 L15,1 C16.1045695,1 17,1.8954305 17,3 L17,4 L20,4 C21.1045695,4 22,4.8954305 22,6 L22,8 C22,9.1045695 21.1045695,10 20,10 L19.9198662,10 L19,21 C19,22.1045695 18.1045695,23 17,23 L7,23 C5.8954305,23 5,22.1045695 5.00345424,21.0830455 L4.07986712,10 L4,10 C2.8954305,10 2,9.1045695 2,8 L2,6 C2,4.8954305 2.8954305,4 4,4 L7,4 Z M7,6 L4,6 L4,8 L20,8 L20,6 L17,6 L7,6 Z M6.08648886,10 L7,21 L17,21 L17.0034542,20.9169545 L17.9132005,10 L6.08648886,10 Z M15,4 L15,3 L9,3 L9,4 L15,4 Z"/>
                </svg>
                '''

    def svg_reuse(self, color_background="#4a90e2", color_text="#ffffff"):
        return f'''
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 32 32">
                    <rect width="32" height="32" rx="4" ry="4" fill="{color_background}" stroke="#357abd" stroke-width="0"/>
                    <path transform="translate(4 4)" fill-rule="evenodd" fill="{color_text}" d="M7.41421356,19 L9.70710678,21.2928932 L8.29289322,22.7071068 L3.58578644,18 L8.29289322,13.2928932 L9.70710678,14.7071068 L7.41421356,17 L16,17 C17.6568542,17 19,15.6568542 19,14 L19,11 L21,11 L21,14 C21,16.7614237 18.7614237,19 16,19 L7.41421356,19 Z M16.5867862,5.00099979 L14.2928932,2.70710678 L15.7071068,1.29289322 L20.4142136,6 L15.7071068,10.7071068 L14.2928932,9.29289322 L16.5847866,7.00099979 L8,7.00099979 C6.34314575,7.00099979 5,8.34414554 5,10.0009998 L5,13.0009998 L3,13.0009998 L3,10.0009998 C3,7.23957604 5.23857625,5.00099979 8,5.00099979 L16.5867862,5.00099979 Z"/>
                </svg>
                '''

    def svg_delete(self, color_background="#4a90e2", color_text="#ffffff"):
        return f'''
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 32 32">
                    <rect width="32" height="32" rx="4" ry="4" fill="{color_background}" stroke="#357abd" stroke-width="0"/>
                    <path transform="translate(4 4)" fill-rule="evenodd" fill="{color_text}" d="M12,12.5857864 L14.2928932,10.2928932 L15.7071068,11.7071068 L13.4142136,14 L15.7071068,16.2928932 L14.2928932,17.7071068 L12,15.4142136 L9.70710678,17.7071068 L8.29289322,16.2928932 L10.5857864,14 L8.29289322,11.7071068 L9.70710678,10.2928932 L12,12.5857864 Z M15,3.41421356 L15,7 L18.5857864,7 L15,3.41421356 Z M19,9 L15,9 C13.8954305,9 13,8.1045695 13,7 L13,3 L5,3 L5,21 L19,21 L19,9 Z M5,1 L15.4142136,1 L21,6.58578644 L21,21 C21,22.1045695 20.1045695,23 19,23 L5,23 C3.8954305,23 3,22.1045695 3,21 L3,3 C3,1.8954305 3.8954305,1 5,1 Z"/>
                </svg>
                '''

    def svg_from_text(self, symbol, size=(32, 32), color_background="#4a90e2", color_text="#ffffff"):
        text_size = int(math.sqrt(size[0] * size[0] + size[1] * size[1]) * (0.2 if len(symbol) > 4 else 0.2))
        return f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
            <svg xmlns="http://www.w3.org/2000/svg" width="{size[0]}" height="{size[1]}" viewBox="0 0 {size[0]} {size[1]}">
            <rect width="{size[0]}" height="{size[1]}" rx="{text_size//2}" ry="{text_size//2}" fill="{color_background}" stroke-width="0"/>
            <text x="{size[0] // 2}" y="{size[1] // 2}" font-family="{self.platform_font}" font-size="{text_size}" fill="{color_text}" stroke="none" text-anchor="middle" dominant-baseline="middle">
                {symbol}
            </text>
        </svg>'''
                
    tbdef = [
        { "id": Item.TB_Trashcan,   "text": svg_trashcan, "tooltip": "Clear screen (input editor)", },
        { "id": Item.TB_Sep },

        { "id": Item.TB_Delete,     "text": svg_delete,   "tooltip": "Delete all variables", },
        { "id": Item.TB_ReUse,      "text": svg_reuse,    "tooltip": "Re-use last output as new input", },
        { "id": Item.TB_Round,      "text": "R.2",        "tooltip": "Round results by 2 digits", },

        { "id": Item.TB_Sep },
        { "id": Item.TB_Dec,        "text": "DEC",        "tooltip": "Display output as decimal formatted number", },
        { "id": Item.TB_Hex,        "text": "HEX",        "tooltip": "Display output as hexadecimal formatted number", },
        { "id": Item.TB_Bin,        "text": "BIN",        "tooltip": "Display output as binary formatted number", },
        { "id": Item.TB_Frc,        "text": "X/Y",        "tooltip": "Display output as decimal fraction", },

        { "id": Item.TB_Sep },
        { "id": Item.TB_Deg,        "text": "DEG",        "tooltip": "Represent angles in degree", },
        { "id": Item.TB_Rad,        "text": "RAD",        "tooltip": "Represent angles in radian", },
    ]

    def __init__(self, callback = None):
        self.root = tk.Tk()
        self.icon_size   = (36, 36)
        self.get_display_scaling()
        self.root.call('tk', 'scaling', self.display_scaling_factor)
        self.callback    = callback
        self.num_format  = "dec"
        self.reuse       = True
        self.resultValue = 0.0
        self.var         = {}
        
    def closeWindow(self):
        self.callback(Gui.Item.Cmd_onClose, "WM_DELETE_WINDOW")
        self.root.destroy()

    def get_display_scaling(self):
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        width_mm = self.root.winfo_screenmmwidth()
        height_mm = self.root.winfo_screenmmheight()
        scaling_x = round((self.screen_width  / (width_mm  / 25.4)) / 96.0, 1)
        scaling_y = round((self.screen_height / (height_mm / 25.4)) / 96.0, 1)
        self.display_scaling_factor = round(max(scaling_x, scaling_y), 1)
        self.tbIconSize = (int(self.icon_size[0] * self.display_scaling_factor), int(self.icon_size[1] * self.display_scaling_factor))
        self.create_fonts()

    def create_fonts(self):
        if platform.system() == "Windows":
            self.platform_font = "Arial Unicode MS"
        elif platform.system() == "Linux":
            self.platform_font = "DejaVuSans"
        else:
            self.platform_font   = "TkFixedFont"
        self.platform_fixed_font = "TkFixedFont"
        self.font_scaling = self.tbIconSize[1] * (3.0 - self.display_scaling_factor)

        # For screen scaling = 1.0
        self.displayFont  = Font(family=self.platform_fixed_font, size=int(self.font_scaling * 0.32), weight="bold") 
        self.editorFont   = Font(family=self.platform_fixed_font, size=int(self.font_scaling * 0.20), weight="bold") 
        self.varlistFont  = Font(family=self.platform_fixed_font, size=int(self.font_scaling * 0.12), weight="bold") 

        # For screen scaling = 2.0
        # self.editorFont   = Font(family=self.platform_fixed_font, size=int(self.font_scaling * 0.24), weight="bold") 
        # self.displayFont  = Font(family=self.platform_fixed_font, size=int(self.font_scaling * 0.32), weight="bold") 
        # self.varlistFont  = Font(family=self.platform_fixed_font, size=int(self.font_scaling * 0.20), weight="bold") 

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
        sashpos = int(float(pos.get("sashpos", 200)))
        width   = int(float(pos.get("width",   640)))
        height  = int(float(pos.get("height",  480)))
        x       = int(float(pos.get("x",       str(int((self.screen_width  - width)  / 2)))))
        y       = int(float(pos.get("y",       str(int((self.screen_height - height) / 2)))))
        self.__pos = { "x": x, "y": y, "width": width, "height": height, "sashpos": sashpos, }
        return self.__pos

    def get_WindowPos(self) -> dict:
        geometry = self.root.geometry() 
        parts = re.findall(r'(\d+)x(\d+)\+(\d+)\+(\d+)', geometry)
        if parts:
            self.__pos = { "x": parts[0][2], "y": parts[0][3], "width": parts[0][0], "height": parts[0][1], }
        self.__pos["sashpos"] = int(self.paned.sashpos(0))
        return self.__pos

    def set_WindowPos(self, pos = None):
        if type(pos) != dict:
            pos = self.__pos
        self.check_geometry(pos)
        self.root.update_idletasks()
        self.root.after(0, self.set_WindowPos_async)
        
    def set_WindowPos_async(self):
        pos = self.__pos
        self.root.geometry(f"{pos["width"]}x{pos["height"]}+{pos["x"]}+{pos["y"]}")
        self.paned.sashpos(0, pos["sashpos"])
        self.root.update_idletasks()

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
                spacer = tk.Label(self.toolbar, text="", width=-1, height=1)
                spacer.grid(row=0, column=col, padx=6, pady=1)
                self.toolbarButtons.append( { "id": id, "button": spacer } )
            else:
                self.toolbar.columnconfigure(col, weight=1)
                btn = self.create_button(self.toolbar, element["text"], element["tooltip"],
                                         size=self.tbIconSize, compound="center", command=partial(self.callback, id))
                self.toolbarButtons.append( { "id": id, "button": btn } )
                btn.grid(row=0, column=col, padx=0, pady=0)
            col += 1
        self.toolbar.columnconfigure(col, weight=999)
        self.result = tk.Label(self.toolbar, text="0.0", width=-1, height=1, anchor="e",
                               bg="#000000", fg="#00F0F0", relief="raised", font=self.displayFont, padx=8, pady=0)
        self.result.grid(row=0, column=col, padx=2, pady=0, sticky="NSEW")
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
        self.createFunctionWindow()
        self.createEditor()

    def createStatusline(self):
        self.statusline = tk.Label(self.root, text="OK", width=-1, height=1, padx=4, pady=2, anchor="w", bd=1, relief="sunken")
        self.statusline.pack(fill="x", side="bottom", padx=2, pady=2)

    def createFunctionWindow(self):
        self.notebook = ttk.Notebook(self.frame_left)
        self.varlist_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.varlist_frame, text="Variables")
        self.keypad_frame = ScrollableFrame(self.notebook, scrollbar_width=14*self.display_scaling_factor)
        self.notebook.add(self.keypad_frame, text="Key pad")
        self.createVarList()
        self.createKeyboard()
        self.createFunctions()
        self.notebook.pack(expand=1, fill='both')

    def createKeyboard(self):
        self.operations_pad = {
            "0": [ "0", "Digit 0", None ],
            "1": [ "1", "Digit 1", None ],
            "2": [ "2", "Digit 2", None ],
            "3": [ "3", "Digit 3", None ],
            "4": [ "4", "Digit 4", None ],

            "5": [ "5", "Digit 5", None ],
            "6": [ "6", "Digit 6", None ],
            "7": [ "7", "Digit 7", None ],
            "8": [ "8", "Digit 8", None ],
            "9": [ "9", "Digit 9", None ],

            ".": [ ".", "Decimal point", None ],
            "(": [ "(", "Open parenthesis", None ],
            ")": [ ")", "Close parenthesis", None ],
            "[": [ "[", "Open bracket (indexing)", None ],
            "]": [ "]", "Close bracket (indexing)", None ],

            "+": [ "+", "Add", None ],
            "-": [ "-", "Subtract", None ],
            "*": [ "*", "Multiply", None ],
            "/": [ "/", "Division", None ],
            "=": [ "=", "Calculate", None ],
        }
        self.operations_frame = tk.Frame(self.keypad_frame.get())
        self.create_keypad(self.operations_frame, self.operations_pad)
        self.operations_frame.pack(pady=8)
    
    def createFunctions(self):
        self.functions_frame = tk.Frame(self.keypad_frame.get())
        self.math_keyboard = MathWrapper.get_keyboard_list()
        self.create_keypad(self.functions_frame, self.math_keyboard)
        self.functions_frame.pack(pady=8)

    def create_keypad(self, frame_item: tk.Widget, pad_dict: dict):
        row = 0
        col = 0
        for element, values in pad_dict.items():
            btn = self.create_button(frame_item, text=values[0], tooltip=values[1], size=self.tbIconSize, command=partial(self.callback, Gui.Item.Math_Function, element))
            btn.grid(row=row, column=col, padx=2, pady=2)
            pad_dict[element][2] = btn
            col += 1
            if col >= 5:
                col = 0
                row += 1

    def get_keyboard_property(self, key):
        return self.math_keyboard[key]

    def createVarList(self):
        style = ttk.Style()
        metrics = self.varlistFont.metrics()
        row_height = int(metrics["linespace"]) # * self.display_scaling_factor)
        style.configure("Treeview", font=self.varlistFont, rowheight=row_height)
        self.varlist = ttk.Treeview(self.varlist_frame, columns = ("name", "value"), show = "headings")
        self.varlist.heading("name", text = "Name")
        self.varlist.column("name", width = 64)
        self.varlist.heading("value", text = "Value")
        self.varlist.column("value", width = 192)
        self.varlist.tag_configure("even", background="#FFFFFF")
        self.varlist.tag_configure("odd",  background="#E0E0FF")
        self.varlist.bind('<Double-1>', self.handle_VarListEvent)
        self.varlist.tooltip = ToolTip(self.root, self.varlist, "List of all pre-defined and user-defined variables")
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

    def handle_EditorEvent(self, event=None):
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
        start = False
        if string.endswith("="):
            string = string[:-1]
            start = True
        aktuelle_position = self.editor.index("insert")
        self.editor.insert(aktuelle_position, string.strip())
        if start:
            self.handle_EditorEvent()
            if not self.reuse:
                self.editor.insert(self.editor.index("insert lineend"), "\n")

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
        elif self.num_format == "frc":
            result = self.decimalFraction(value)
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
                relief = "sunken" if pressed else "raised"
                image = button.images[1 if pressed else 0]
                button.configure(relief=relief, image=image)
                return pressed
        return False

    def get_ScreenContent(self) -> str:
        return self.editor.get("1.0", "end-1c")

    def set_ScreenContent(self, content: str):
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", content)

    def copyResultToClipboard(self):
        pyperclip.copy(self.result.cget("text"))

    def set_NumberFormat(self, fmt = "dec"):
        self.num_format = fmt

    def decimalFraction(self, value: float):
        max_denominator = 1000000
        full = int(value)
        frac = value - full
        fraction = Fraction(frac).limit_denominator(max_denominator)
        full = f"{full}+" if full != 0 else ""
        return f"({full}{fraction})"
    
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

    def draw_svg(self, svg_string, size=(32, 32), background_color=(0, 0, 0, 0)):
        try:
            png_data = cairosvg.svg2png(bytestring=svg_string.encode('UTF-8'), output_width=size[0], output_height=size[1])
            image_src = Image.open(BytesIO(png_data))
            image = Image.new('RGBA', size, background_color)
            image.paste(image_src)
        except Exception as e:
            image = Image.new('RGBA', size, background_color)
            draw = ImageDraw.Draw(image)
            draw.text((10, 10), f"{e}", fill=(0, 0, 0, 255))
        return ImageTk.PhotoImage(image)

    def create_svg_button(self, parent, svg_string_normal, svg_string_pressed, size=(32, 32), **tk_button_kwargs):
        images = (
            self.draw_svg(svg_string_normal,  size),
            self.draw_svg(svg_string_pressed, size),
        )
        button = tk.Button(parent, image=images[0], **tk_button_kwargs)
        button.images = images
        return button

    def is_svg_string(self, text: str) -> bool:
        return '<svg' in text and '</svg>' in text

    def create_button(self, parent, text="", tooltip=None, size=(32, 32), **tk_button_kwargs):
        if type(text) != str:
            svg_string_normal  = text(self)
            svg_string_pressed = text(self, color_background="#3b6cac")
        elif self.is_svg_string(text):
            svg_string_normal  = text
            svg_string_pressed = text
        else:
            svg_string_normal  = self.svg_from_text(text, size)
            svg_string_pressed = self.svg_from_text(text, size, color_background="#3b6cac")
        btn = self.create_svg_button(parent, svg_string_normal, svg_string_pressed, size, **tk_button_kwargs)
        if tooltip:
            btn.tooltip = ToolTip(self.root, btn, tooltip)
        else:
            btn.tooltip = None
        return btn
