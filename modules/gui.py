import io, platform, pyperclip, re, subprocess
import tkinter as tk
from tkinterweb import HtmlFrame
from pathlib import Path
from itertools import groupby
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
from modules.app_tools import AppTools
from modules.svg_source import SVG_Source

# OS relating ...
if platform.system() == "Windows":
    # On Windows, cairosvg is not working properly. So, we always need
    # ready for use PNG images for the buttons!
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPM
elif platform.system() == "Linux":
    # On Linux, cairosvg is available and working properly. So, we can
    # use the internal SVG resources to build the PNG images we need
    # for running on the other operating systems.
    import cairosvg
else:
    # On other OS, like MacOS, it is currently unknown if cairosvg library
    # is available. So, we also use the PNG images only
    pass

class Gui():

    class Item(Enum):
        Cmd_onClose    = "close",
        Cmd_getMacros  = "get.macro.list"
        Cmd_getMacCode = "get.macro.code"
        Cmd_hotkey     = "event.hotkey"
        VarList        = "event.variable",
        Editor         = "event.editor"
        EditorMacro    = "event.editor.macro"
        EditorDelMacro = "event.editor.macro.delete"
        Result         = "event.result"
        Timer          = "timer.event"
        Menu_Clear     = "menu.clear",
        Menu_Delete    = "menu.delete",
        Menu_Reset     = "menu.reset",
        Menu_DefVars   = "menu.default_vars"
        Menu_DefUpdate = "menu.default_vars_update"
        Menu_Help      = "menu_help",
        Menu_License   = "menu_license",
        Menu_Copy      = "menu.copy",
        Menu_Exit      = "menu.exit",
        Menu_MacroAdd  = "menu.macro.add"
        Menu_MacroEdit = "menu.macro.edit"
        Menu_MacroRun  = "menu.macro.run"
        Menu_MacroDel  = "menu.macro.delete"
        Popup_VarRem = "popup.varlist.remove_var"
        TB_Sep         = "separator",
        TB_Trashcan    = "button.clear",
        TB_Delete      = "button.delete"
        TB_ReUse       = "button.reuse",
        TB_Round       = "button.round",
        TB_Dec         = "button.decimal",
        TB_Hex         = "button.hexadecimal",
        TB_Bin         = "button.binary",
        TB_Frc         = "button.fraction"
        TB_Deg         = "button.degrees",
        TB_Rad         = "button.radians",
        Math_Function  = 9000,

    class NumFormat(Enum):
        DEC = "DEC"
        HEX = "HEX"
        BIN = "BIN"
        FRC = "FRC"

    menudef = [
        { "cascade": "File",  "text": "Exit",             "icon": SVG_Source.svg_exit,     "id": Item.Menu_Exit,      },

        { "cascade": "Edit",  "text": "Clear",            "icon": SVG_Source.svg_trashcan, "id": Item.Menu_Clear,     },
        { "cascade": "Edit",  "text": "Delete",           "icon": SVG_Source.svg_delete,   "id": Item.Menu_Delete,    },
        { "cascade": "Edit",  "text": "Reset",            "icon": SVG_Source.svg_reset,    "id": Item.Menu_Reset,     },
        { "cascade": "Edit",  "text": "_sep_",            "icon": None,                    "id": None                 },
        { "cascade": "Edit",  "text": "Set default vars", "icon": None,                    "id": Item.Menu_DefVars,   },
        { "cascade": "Edit",  "text": "Update def. vars", "icon": None,                    "id": Item.Menu_DefUpdate, },
        { "cascade": "Edit",  "text": "_sep_",            "icon": None,                    "id": None                 },
        { "cascade": "Edit",  "text": "Copy",             "icon": SVG_Source.svg_copy,     "id": Item.Menu_Copy,      },

        { "cascade": "Macro", "text": "Add macro",        "icon": None,                    "id": Item.Menu_MacroAdd,  },
        { "cascade": "Macro", "text": "Edit macro",       "icon": None,                    "id": Item.Menu_MacroEdit, },
        { "cascade": "Macro", "text": "Run macro",        "icon": None,                    "id": Item.Menu_MacroRun,  },

        { "cascade": "Help",  "text": "Help usage",       "icon": None,                    "id": Item.Menu_Help,      },
        { "cascade": "Help",  "text": "Display license",  "icon": None,                    "id": Item.Menu_License,   },
    ]

    tbdef = [
        { "id": Item.TB_Trashcan,   "text": SVG_Source.svg_trashcan, "tooltip": "Clear screen (input editor)", },
        { "id": Item.TB_Sep },

        { "id": Item.TB_Delete,     "text": SVG_Source.svg_delete,   "tooltip": "Delete user defined variables and restore predefined variables", },
        { "id": Item.TB_ReUse,      "text": SVG_Source.svg_reuse,    "tooltip": "Re-use last output as new input", },
        { "id": Item.TB_Round,      "text": "R.2",                   "tooltip": "Round results by 2 digits", },

        { "id": Item.TB_Sep },
        { "id": Item.TB_Dec,        "text": "DEC",                   "tooltip": "Display output as decimal formatted number", },
        { "id": Item.TB_Hex,        "text": "HEX",                   "tooltip": "Display output as hexadecimal formatted number", },
        { "id": Item.TB_Bin,        "text": "BIN",                   "tooltip": "Display output as binary formatted number", },
        { "id": Item.TB_Frc,        "text": "X/Y",                   "tooltip": "Display output as decimal fraction", },

        { "id": Item.TB_Sep },
        { "id": Item.TB_Deg,        "text": "DEG",                   "tooltip": "Represent angles in degree", },
        { "id": Item.TB_Rad,        "text": "RAD",                   "tooltip": "Represent angles in radian", },
    ]

    def __init__(self, callback = None):
        self.root = tk.Tk()
        self.get_display_scaling()
        self.root.call('tk', 'scaling', self.display_scaling_factor)
        self.callback    = callback
        self.num_format  = Gui.NumFormat.DEC
        self.reuse       = True
        self.resultValue = 0.0
        self.var         = {}
        self.icons       = {}
        
    def closeWindow(self):
        self.callback(Gui.Item.Cmd_onClose, "WM_DELETE_WINDOW")
        self.root.destroy()

    def interval_timer(self):
        self.callback(Gui.Item.Timer)
        self.timer_id = self.root.after(1000, self.interval_timer)
        
    def manage_icon_size(self):
        self.icon_size    = (36, 36)
        self.tbIconSize   = (int(self.icon_size[0] * self.display_scaling_factor), int(self.icon_size[1] * self.display_scaling_factor))
        self.font_scaling = self.tbIconSize[1] * (3.0 - self.display_scaling_factor)

    def manage_fonts(self):
        if platform.system() == "Windows":
            self.platform_font = "Arial Unicode MS"
            self.font_scaling *= 1.5
            self.root.option_add("*Font", ('TkFixedFont', 14))
            self.root.option_add("*Menu.Font", ('TkFixedFont', 14))
        elif platform.system() == "Linux":
            self.platform_font = "DejaVuSans"
        else:
            self.platform_font   = "TkFixedFont"
        self.platform_fixed_font = "TkFixedFont"
        self.displayFont  = Font(family=self.platform_fixed_font, size=int(self.font_scaling * 0.32), weight="bold") 
        self.editorFont   = Font(family=self.platform_fixed_font, size=int(self.font_scaling * 0.20), weight="bold") 
        self.varlistFont  = Font(family=self.platform_fixed_font, size=int(self.font_scaling * 0.14), weight="bold") 

    def query_display_scaling_factor(self) -> float:
        self.dpi = round(self.root.winfo_fpixels('1i'), 0)
        tk_scaling = self.root.tk.call('tk', 'scaling')
        if platform.system() == "Windows":
            self.dpi = round(72.0 * tk_scaling, 0)
        elif platform.system() == "Linux":
            try:
                out = subprocess.check_output(["xrdb", "-query"], text=True)
                out = out.strip().replace("\t", " ").split("\n")
                for entry in out:
                    if "Xft.dpi: " in entry:
                        self.dpi = float(entry[9:])
                        break
            except:
                pass
        else:
            pass
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.display_scaling_factor = round(self.dpi / 96.0, 0)

    def get_display_scaling(self):
        self.query_display_scaling_factor()
        self.manage_icon_size()
        self.manage_fonts()

    def hide_widget(self, widget):
        widget.withdraw()
        widget.attributes('-alpha', 0.0)
        widget.update_idletasks()

    def unhide_widget(self, widget):
        widget.deiconify()
        widget.after_idle(lambda: widget.attributes('-alpha', 1.0))
        widget.update_idletasks()

    def app_window(self, pos = {} ):
        self.hide_widget(self.root)
        self.check_geometry(pos)
        self.createWindow()
        self.createMenu()
        self.createToolbar()
        self.createInfoLine()
        self.createStatusLine()
        self.createPaned()
        self.set_WindowPos()
        self.set_ButtonPressed(Gui.Item.TB_Deg, True)
        self.set_ButtonPressed(Gui.Item.TB_Rad, False)
        self.bind_hotkeys()
        self.timer_id = self.root.after(1000, self.interval_timer)
        return self

    def bind_hotkeys(self):
        for i in range(1, 13):
            self.root.bind_all(f'<F{i}>', self.hotkey)
        
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
        self.unhide_widget(self.root)

    def dispatch(self):
        tk.mainloop()
        
    def createWindow(self, title="KKSCalc"):
        self.root.protocol("WM_DELETE_WINDOW", self.closeWindow)
        self.root.title(title)
        icon_file = AppTools().get_ImageResourcePath(image_file="app_icon.png")
        if Path(icon_file).exists():
            try:
                self.app_icon = ImageTk.PhotoImage(file=icon_file)
                self.root.iconphoto(False, self.app_icon)
            except:
                pass
        
    def createMenu(self):
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        last_cascade = ""
        index = 0
        for element in Gui.menudef:
            cascade = element.get("cascade", None)
            text    = element.get("text", "")
            id      = element.get("id", -1)
            if cascade != last_cascade:
                index = 0
                last_cascade = cascade
                menu_cascade = tk.Menu(self.menubar, tearoff=False)
                self.menubar.add_cascade(label=last_cascade, menu=menu_cascade)        
            else:
                index += 1
            if text == "_sep_":
                menu_cascade.add_separator()
            else:
                icon = self.create_menu_icon(element.get("icon", None))
                self.icons[text] = icon
                text = " " + text
                if id == Gui.Item.Menu_MacroEdit:
                    self.branch_macro_edit = tk.Menu(self.menubar, tearoff=False, postcommand=partial(self.populate_dynamic, text, id))
                    menu_cascade.add_cascade(label=text, image=icon, compound="left", menu=self.branch_macro_edit)
                elif id == Gui.Item.Menu_MacroRun:
                    self.branch_macro_run = tk.Menu(self.menubar, tearoff=False, postcommand=partial(self.populate_dynamic, text, id))
                    menu_cascade.add_cascade(label=text, image=icon, compound="left", menu=self.branch_macro_run)
                else:
                    menu_cascade.add_command(label=text, image=icon, compound="left", command=partial(self.callback, id))

    def populate_dynamic(self, text: str, id):
        if id == Gui.Item.Menu_MacroEdit:
            menu = self.branch_macro_edit
        elif id == Gui.Item.Menu_MacroRun:
            menu = self.branch_macro_run
        else:
            return
        menu.delete(0, 'end')
        macro_list = []
        result = self.callback(Gui.Item.Cmd_getMacros, 0.0)
        if result[1] == "OK":
            macro_list = result[0]
            for i, name in enumerate(macro_list):
                entry = f"F{i+1}  {name}" if id == Gui.Item.Menu_MacroRun else name
                menu.add_command(label=entry, command=partial(self.callback, id, name))

    def createToolbar(self):
        self.toolbar = tk.Frame(self.root, bd=1, relief="sunken")
        self.toolbar.pack(side="top", fill="x", padx=4)
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

    def createInfoLine(self):
        self.frame_infoline = tk.Frame(self.root)
        self.frame_infoline.pack(side="top", fill="x", padx=4)
        self.frame_infoline.macro_btn = []
        self.update_infoline()

    def createPaned(self):
        self.paned = ttk.PanedWindow(self.root, orient="horizontal")
        self.paned.pack(fill="both", expand=True, padx=4)
        self.frame_left = tk.Frame(self.paned, bg="lightblue")
        self.frame_left.pack(fill="both", expand=True)
        self.paned.add(self.frame_left)
        self.frame_right = tk.Frame(self.paned, bg="lightgreen")
        self.frame_right.pack(fill="both", expand=True)
        self.paned.add(self.frame_right)
        self.createFunctionWindow()
        self.createEditor()

    def createStatusLine(self):
        self.statusline = tk.Label(self.root, text="OK", width=-1, height=1, padx=4, pady=2, anchor="w", bd=1, relief="sunken")
        self.statusline.pack(fill="x", side="bottom", padx=2, pady=2)

    def createFunctionWindow(self):
        style = ttk.Style(self.root)
        style.configure("TNotebook.Tab", font=(self.platform_font, int(self.font_scaling * 0.14), "bold"))
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
        self.varlist.tag_configure("odd",  background="#9fcfff")
        self.varlist.bind('<Double-1>', self.handle_VarListEvent)
        self.varlist.bind("<Button-3>", self.handle_VarListPopup)        
        self.varlist.tooltip = ToolTip(self.root, self.varlist, "List of all pre-defined and user-defined variables")
        self.varlist.pack(padx=4.0, pady=4.0, fill="both", expand=True)

    def createEditor(self):
        self.editor = tk.Text(self.frame_right, borderwidth=0, font=self.editorFont)
        self.editor.tag_config("negative", foreground="red")
        self.editor.tag_config("positive", foreground="blue")
        self.editor.tag_config("neutral",  foreground="gray")
        self.editor.pack(padx=4.0, pady=4.0, fill="both", expand=True)
        self.editor.bind("<Return>", self.handle_EditorEvent)

    def get_keyboard_property(self, key):
        return self.math_keyboard[key]

    def make_macro_button(self, i, item, btn_cx):
        f_key = f"F{i+1}"
        fu_btn = tk.Button(self.frame_infoline, text=f"{f_key}: {item}", width=btn_cx + 3, border=1,
            compound="left", anchor="w", padx=4, bg="#fa75a8", fg="white", font=self.varlistFont, relief="groove",
            command=partial(self.callback, Gui.Item.Cmd_hotkey, f_key))
        macro_tooltip = f"Call macro \"{item}\" by pressing this button or {f_key} or type \".{item}\"<Enter> in the editor window."
        fu_btn.tooltip = ToolTip(self.root, fu_btn, macro_tooltip)
        fu_btn.grid(row=0, column=i*2+1, padx=0, pady=2, sticky="nwse")
        return fu_btn
    
    def make_macro_menu_button(self, i, item):
        menu_btn = tk.Menubutton(self.frame_infoline, text="▼", border=1, padx=2,
            bg="#fa75a8", fg="white", font=self.varlistFont, compound="right", anchor="e", relief="groove")
        menu = tk.Menu(menu_btn, tearoff=0)
        menu_btn["menu"] = menu
        menu.add_command(label="Edit macro", command=partial(self.callback, Gui.Item.Menu_MacroEdit, item))
        menu.add_command(label="Delete macro", command=partial(self.callback, Gui.Item.Menu_MacroDel, item))
        menu_btn.grid(row=0, column=i*2, padx=0, pady=3, sticky="nwse")
        return menu_btn

    def update_infoline(self):
        macro_list = self.get_MacroFunctionList()
        btn_cx = 8
        for item in macro_list:
            btn_cx = max(len(item), btn_cx)
        for item in self.frame_infoline.macro_btn:
            item.destroy()
        self.frame_infoline.macro_btn = []
        for i, item, in enumerate(macro_list):
            self.frame_infoline.macro_btn.append(self.make_macro_menu_button(i, item))
            self.frame_infoline.macro_btn.append(self.make_macro_button(i, item, btn_cx))

    def handle_ResultEvent(self, event):
        self.callback(Gui.Item.Result, 0.0)
        
    def handle_VarListPopup(self, event):
        itemID = self.varlist.identify_row(event.y)
        if itemID:
            value = self.varlist.item(itemID, 'values')
            print(f"{itemID}: {value[0]}")
            self.varlist.selection_set(itemID)
            self.varlist.focus(itemID)
            menu = tk.Menu(self.root, tearoff=0)
            menu.add_command(label="Delete variable", command=partial(self.callback, Gui.Item.Popup_VarRem, value[0]))
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()

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
        if type(value) == tuple:
            value = value[-1]
        self.resultValue = float(value)
        if self.round:
            value = round(value, 2)
        if self.num_format == Gui.NumFormat.BIN:
            result = self.float2fractional(value, 2, 8 if not self.round else 2)
        elif self.num_format == Gui.NumFormat.HEX:
            result = self.float2fractional(value, 16, 4 if not self.round else 2)
        elif self.num_format == Gui.NumFormat.FRC:
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
        self.root.update_idletasks()

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

    def set_NumberFormat(self, fmt = NumFormat.DEC):
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
        self.unhide_widget(widget)

    def macro_editor(self, name="default", cmd=[]):
        self.original_macro_name = name
        text = "\n".join(cmd)
        self.macro_editor = tk.Toplevel(self.root)
        self.hide_widget(self.macro_editor)
        self.macro_editor.title("Macro editor")
        self.macro_editor.grab_set()
        self.macro_editor.protocol("WM_DELETE_WINDOW", self.on_macro_closing)
        self.macro_name = tk.Text(self.macro_editor, width=-1, height=1, relief="raised", font=self.editorFont)
        self.macro_name.grid(row=0, column=0, padx=2, pady=2, sticky="NSEW")
        self.macro_name.insert(self.macro_name.index("insert lineend"), name)
        self.macro_text = tk.Text(self.macro_editor, borderwidth=0, font=self.editorFont, relief="groove")
        self.macro_text.grid(row=1, column=0, padx=2, pady=2, sticky="NSEW")
        self.macro_text.insert(self.macro_text.index("insert lineend"), text + "\n")
        self.center_window(self.macro_editor, self.root)

    def on_macro_closing(self):
        content = self.macro_text.get("1.0", tk.END)
        cmd = content.strip().split("\n")
        cmd = list(map(lambda line: line.strip(), cmd))
        name = self.macro_name.get("1.0", tk.END).strip().lower()
        if not name:
            cmd = ['']
        if name != self.original_macro_name and self.original_macro_name != "default":
            self.callback(Gui.Item.EditorDelMacro, self.original_macro_name)
        self.macro_editor.destroy()
        del self.original_macro_name
        del self.macro_name
        del self.macro_text
        del self.macro_editor
        if name:
            if cmd == ['']:
                self.callback(Gui.Item.EditorDelMacro, name)
                cmd = None
            else:
                self.callback(Gui.Item.EditorMacro, (name, cmd))
        self.update_infoline()

    def hotkey(self, event):
        self.callback(Gui.Item.Cmd_hotkey, event.keysym)

    def get_MacroFunctionList(self):
        result = self.callback(Gui.Item.Cmd_getMacros, 0.0)
        if result[1] != "OK":
            return []
        return result[0]

    def display_popup(self, title = "Message", text = "Text."):
        dialog_window = tk.Toplevel(self.root)
        self.hide_widget(dialog_window)
        dialog_window.title(title)
        dialog_window.grab_set()
        if "<html>" in text:
            html_widget = HtmlFrame(dialog_window, messages_enabled=False)
            html_widget.load_html(text)
            html_widget.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        else:        
            scrolled_text = scrolledtext.ScrolledText(dialog_window, wrap=tk.WORD, width=80, height=20, bg="lightgrey")
            scrolled_text.insert(tk.END, text)
            scrolled_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.center_window(dialog_window, self.root)

    def get_filename_from_tooltip(self, tooltip):
        return ''.join(key for key, group in groupby(re.sub(r'[^a-z0-9._-]', '_', tooltip.strip().lower()).strip("_").replace("_-_", "_")))

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

    def save_images(self, button, folder=None, filename="button"):
        n = 0
        for image in button.images:
            pil_image_out = ImageTk.getimage(image)
            path = self.get_button_image_path(folder, filename, n)
            print(f"Save image: \"{path}\"")
            pil_image_out.save(path)
            n += 1

    def create_button(self, parent, text="", tooltip=None, size=(32, 32), **tk_button_kwargs):
        folder = f"/buttons_{self.display_scaling_factor}"
        # Button and menu images are generated from SVG sources now also in Windows.
        # It is no needed to read them from the files. Optionally, the following section
        # can be re-enabled, and the save section below also, to re-enable using images
        # once generated and stored in a file.
        #
        # if tooltip:
            # filename = self.get_filename_from_tooltip(tooltip)
            # il = []
            # for n in range(2):
            #     path = Path(self.get_button_image_path(folder, filename, n))
            #     if path.exists():
            #         image_data = Image.open(path)
            #         il.append(ImageTk.PhotoImage(image_data))
            # if len(il) >= 2:
            #     images = (il[0], il[1], )
            #     btn = tk.Button(parent, image=images[0], **tk_button_kwargs)
            #     btn.images = images
            #     btn.tooltip = ToolTip(self.root, btn, tooltip)
            #     return btn
            #
        if type(text) != str:
            svg_string_normal  = text(self, size=size)
            svg_string_pressed = text(self, size=size, color_background="#3b6cac")
        elif self.is_svg_string(text):
            svg_string_normal  = text
            svg_string_pressed = text
        else:
            svg_string_normal  = SVG_Source.svg_from_text(self, symbol=text, size=size, platform_font=self.platform_font)
            svg_string_pressed = SVG_Source.svg_from_text(self, symbol=text, size=size, color_background="#3b6cac", platform_font=self.platform_font)
        btn = self.create_svg_button(parent, svg_string_normal, svg_string_pressed, size, **tk_button_kwargs)
        if tooltip:
            btn.tooltip = ToolTip(self.root, btn, tooltip)
            # Enable this to store the images in PNG files.
            #
            # self.save_images(btn, folder, filename)
            #
        else:
            btn.tooltip = None
        return btn
        
    def get_button_image_path(self, folder=None, filename=None, level=0):
        button_file = f"{filename}_{level}.png"
        return AppTools().get_ImageResourcePath(image_file=button_file, sub_folder=folder)

    def create_menu_icon(self, icon):
        size = int(self.font_scaling * 0.24 + 0.5)
        icon_size = (size, size)
        if icon == None:
            return ImageTk.PhotoImage(Image.new('RGBA', icon_size, "#00000000"))
        elif type(icon) == str:
            svg = SVG_Source.svg_from_text(self, symbol=icon, size=icon_size, color_background="#e0e0e0", color_text="#000000", platform_font=self.platform_font)
            svg_image = self.draw_svg(svg_string=svg, color_background="#e0e0e0", color_text="#000000")
        else:
            svg = icon(self, color_background="#e0e0e0", color_text="#000000")
            svg_image = self.draw_svg(svg_string=svg)
        image = ImageTk.getimage(svg_image)
        image = image.resize(icon_size, Image.LANCZOS)
        return ImageTk.PhotoImage(image)

    def draw_svg(self, svg_string, size=(32, 32), color_background=(0, 0, 0, 0), color_text=(0, 0, 0, 255)):
        if platform.system() == "Windows":
            
            try:
                svg_io = io.StringIO(svg_string)
                drawing = svg2rlg(svg_io)
                renderPM.drawToFile(drawing, "temp.png", fmt="PNG")
                img = Image.open("temp.png")
                return ImageTk.PhotoImage(img)
            except Exception as e:
                error_text = str(e)

        elif platform.system() == "Linux":
            try:
                png_data = cairosvg.svg2png(bytestring=svg_string.encode('UTF-8'), output_width=size[0], output_height=size[1])
                image_src = Image.open(BytesIO(png_data))
                image = Image.new('RGBA', size, color_background)
                image.paste(image_src)
            except Exception as e:
                error_text = str(e)
        else:
            error_text = "Not supported OS"

        image = Image.new('RGBA', size, color_background)
        draw = ImageDraw.Draw(image)
        draw.text((10, 10), f"{error_text}", fill=color_text)
        return ImageTk.PhotoImage(image)
