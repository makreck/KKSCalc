import sys, os, math, re, pyperclip
from modules.gui import Gui
from modules.config import Config
from modules.math_wrapper import MathWrapper        
from modules.times import Times
from modules.roman_numbers import RomanNumber
from modules.thermocouple import Thermocouple
from modules.helptext import general_usage

class Calculator:

    __funclist = {
        ".cls":   ( "func_cls",   "Clear editor" ),
        ".del":   ( "func_del",   "Delete user defined variables and restore predefined variables" ),
        ".res":   ( "func_res",   "Reset, delete variables, clear editor" ),
        ".deg":   ( "func_deg",   "Use degrees for trigonometric functions" ),
        ".rad":   ( "func_rad",   "Use radians for trigonometric functions" ),
        ".copy":  ( "func_copy",  "Copy result to clipboard" ),
        ".paste": ( "func_paste", "Paste content from the clipboard" ),
        ".dec":   ( "func_dec",   "Use decimal system for outputs" ),
        ".hex":   ( "func_hex",   "Use hexadecimal system for outputs" ),
        ".bin":   ( "func_bin",   "Use binary system for outputs" ),
        ".frc":   ( "func_frc",   "Use decimal fraction for outputs" ),
        ".round": ( "func_round", "Round results for business use" ),
        ".reuse": ( "func_reuse", "Re-use result for next calculation" ),
        ".rom":   ( "func_roman", "Convert given number into roman digits and vice versa" ),
        ".sum":   ( "func_sum",   "Add variables, opt: base_name, from, to" ),
        ".tcmvc": ( "func_tcmvc", "Convert thermocouple voltage in mV into °Celsius" ),
        ".tccmv": ( "func_tccmv", "Convert °Celsius into thermocouple voltage in mV" ),
        ".dvar":  ( "func_dvar",  "Store currently used variable set as default" ),
        ".udv":   ( "func_udv",   "Update default variables with the currently set values." ),
        ".madd":  ( "func_madd",  "Add a new macro." ),
        ".medit": ( "func_medit", "Edit a macro." ),
        ".mrun":  ( "func_mrun",  "Run a macro." ),
        ".rmv":   ( "func_rmv",   "<varname> Remove variable"),
        ".help":  ( "func_help",  "Show common or specific help" ),
        ".lic":   ( "func_lic",   "Display license file" ),
        ".exit":  ( "func_exit",  "Terminate application" ),
    }

    __pow_substitudes = {
        "⁰": "0",
        "¹": "1",
        "²": "2",
        "³": "3",
        "⁴": "4",
        "⁵": "5",
        "⁶": "6",
        "⁷": "7",
        "⁸": "8",
        "⁹": "9",
        "⁻": "-",
        "⁺": "+",
    }

    __default_varlist = { 
            "date": "2026-01-01",
            "time": "00:00:00",
            "pi":   math.pi,
            "e":    math.e,
        }

    def __init__(self):
        self.cfg   = Config().load()
        self.times = Times()
        self.ro    = RomanNumber()
        self.tc    = Thermocouple()
        self.gui   = Gui(self.guiCallback).app_window(self.cfg.get_WindowPos("MainWindow"))
        self.setupParser()
        self.setupGui()

    def setupParser(self):
        self.clr_Variables()
        self.set_VariableContent(self.cfg.get_VariableContent())
        self.set_AngleMode(self.cfg.get_AngleMode())

    def setupGui(self):
        amode = self.cfg.get_AngleMode()
        self.gui.set_ButtonPressed(Gui.Item.TB_Deg, amode == MathWrapper.AngleMode.DEG)
        self.gui.set_ButtonPressed(Gui.Item.TB_Rad, amode != MathWrapper.AngleMode.DEG)
        self.gui.set_Round(self.gui.set_ButtonPressed(Gui.Item.TB_Round, self.cfg.get_Round()))
        self.gui.set_ReUse(self.gui.set_ButtonPressed(Gui.Item.TB_ReUse, self.cfg.get_ReUse()))
        self.gui.set_VariableContent(self.get_VariableContent())
        self.gui.set_ScreenContent(self.cfg.get_ScreenContent())
        self.gui.set_Result(self.cfg.get_Display())
        self.defineNumberFormat(self.cfg.get_NumberFormat())

    def defineNumberFormat(self, fmt: Gui.NumFormat):
        self.cfg.set_NumberFormat(fmt)
        self.gui.set_NumberFormat(fmt)
        self.gui.set_ButtonPressed(Gui.Item.TB_Dec, fmt == Gui.NumFormat.DEC)
        self.gui.set_ButtonPressed(Gui.Item.TB_Hex, fmt == Gui.NumFormat.HEX)
        self.gui.set_ButtonPressed(Gui.Item.TB_Bin, fmt == Gui.NumFormat.BIN)
        self.gui.set_ButtonPressed(Gui.Item.TB_Frc, fmt == Gui.NumFormat.FRC)
        self.gui.set_Result(self.gui.get_Result())
        return (0.0, "OK", 2 )

    def run(self):
        self.gui.dispatch()
        return self

    def exit(self, event = None):
        self.update_default_variables()
        self.cfg.set_VariableContent(self.get_VariableContent())
        self.cfg.set_WindowPos("MainWindow", self.gui.get_WindowPos())
        self.cfg.set_ScreenContent(self.gui.get_ScreenContent())
        self.cfg.set_Display(self.gui.get_Result())
        self.cfg.save()

    def set_AngleMode(self, amode = MathWrapper.AngleMode.DEG):
        self.set_AngleMode(amode)
        self.cfg.set_AngleMode(amode)
        self.gui.set_ButtonPressed(Gui.Item.TB_Deg, amode == MathWrapper.AngleMode.DEG)
        self.gui.set_ButtonPressed(Gui.Item.TB_Rad, amode != MathWrapper.AngleMode.DEG)

    def do_parse(self, string: str) -> float:
        result = (0.0, "OK", False)
        elements = string.strip().lower().split("=")
        try:
            result = self.parse(elements[-1])
            if (len(elements) > 1) and result[2]:
                self.set_Variable(elements[0], result[0])
            self.gui.set_VariableContent(self.get_VariableContent())
        except Exception as e:
            result = ( 0.0, f"Error: {e}", False )
        return result

    def get_Cmd(self) -> dict:
        return MathWrapper.get_command_list()

    def parse_RomanNumber(self, number) -> float:
        if type(number) == str:
            if self.ro.is_roman_number_string(number):
                return self.ro.roman2decimal(number)
            else:
                try:
                    number = float(number)
                except:        
                    raise ValueError("Not a roman number")
        if type(number) == float or type(number) == int:
            return self.ro.decimal2roman(number)
        return (0.0)

    def __get_variable_unchecked(self, name: str, def_value = 0):
        if not self.is_VariableExisting(name):
            value = def_value
            self.__varlist[name] = value
        else:
            value = self.__varlist.get(name)
        return value

    def get_InitializedVariable(self, name: str) -> tuple:
        if not self.is_ValidVariable(name):
            return (0.0, "Name error", 1)
        value = self.__get_variable_unchecked(self.__filter_varname(name))
        if type(value) == str and value.startswith("#"):
            result = self.do_parse(value)
            if result[1] == 'OK':
                value = result[0]
        return (value, "OK", 1)

    def set_Variable(self, name: str, value = 0.0):
        name = self.__filter_varname(name)
        if name:
            if name == "pi" or name == "e":
                raise ValueError(f"Not allowed to change common constant \"{name}\".")
            self.__varlist[name] = value

    def is_ValidVariable(self, name:str) -> bool:
        name = self.__filter_varname(name)
        if name == None:
            return False
        length = len(name)
        if "[" in name:
            length = name.index("[")
        name = name[:length]
        if name[0].isnumeric():
            return False
        return name.isalnum()

    def is_VariableExisting(self, name: str) -> bool:
        if name == None: return False
        value = self.__varlist.get(name.lower())
        return value != None

    def get_Variable(self, name: str):
        name = self.__filter_varname(name)
        if name == None: return 0.0
        value = self.__varlist.get(name)
        if value == None:
            self.__varlist[name] = 0.0
            return 0.0
        return value

    def set_VariableContent(self, vars = None):
        if type(vars) != dict:
            return
        self.__varlist = { **self.__varlist, **vars }
        return self.__varlist

    def get_VariableContent(self) -> dict:
        return dict(self.__varlist)

    def remove_variable(self, varname: str):
        del(self.__varlist[varname])
        
    def clr_Variables(self):
        self.__varlist = dict(Calculator.__default_varlist)
        self.__varlist.update(self.cfg.get_default_variables())
        return self

    def set_AngleMode(self, mode = MathWrapper.AngleMode.DEG):
        MathWrapper.set_AngleMode(mode)
        self.gui.set_ButtonPressed(Gui.Item.TB_Deg, mode == MathWrapper.AngleMode.DEG)
        self.gui.set_ButtonPressed(Gui.Item.TB_Rad, mode == MathWrapper.AngleMode.RAD)
        return self

    def get_AngleMode(self) -> MathWrapper.AngleMode:
        return MathWrapper.get_AngleMode()

    def cmd(self, command: str):
        command = list(filter(None, command.strip().replace(" ", ",").split(",")))
        cmdFunction = Calculator.__funclist.get(command[0], None)
        if cmdFunction != None:
            func = getattr(self, cmdFunction[0])
            return func(command)
        else:
            raise SyntaxError(f"Invalid command \"{command}\"")

    def func_exit(self, parameters = None):
        self.gui.closeWindow()
        exit()
        
    def func_help(self, parameters = None):
        self.gui.display_popup("Help", self.create_html_help_text())
        return (0.0, "OK", 2 )

    def func_lic(self, parameters = None):
        self.gui.display_popup("License", self.read_license_file())
        return (0.0, "OK", 2 )

    def func_dvar(self, parameters = None):
        self.cfg.store_default_variables(self.get_VariableContent())
        return (0.0, "OK", 2 )

    def func_udv(self, parameters = None):
        self.update_default_variables()
        return (0.0, "OK", 2 )
        
    def func_rmv(self, parameters = None):
        if parameters != None and len(parameters) >= 2:
            self.remove_variable(parameters[1])
            self.gui.set_VariableContent(self.get_VariableContent())
            return (0.0, "OK", 2 )
        else:
            return (0.0, "Error, invalid variable name", 2 )
    
    def func_cls(self, parameters = None):
        self.gui.clear()
        return (0.0, "OK", 0 )

    def func_del(self, parameters = None):
        self.clr_Variables()
        self.gui.set_VariableContent(self.get_VariableContent())
        return (0.0, "OK", 2 )

    def func_res(self, parameters = None):
        self.func_del()
        self.func_cls()
        return (0.0, "OK", 0 )

    def func_deg(self, parameters = None):
        self.set_AngleMode(MathWrapper.AngleMode.DEG)
        return (0.0, "OK", 2 )

    def func_rad(self, parameters = None):
        self.set_AngleMode(MathWrapper.AngleMode.RAD)
        return (0.0, "OK", 2 )

    def func_copy(self, parameters = None):
        self.gui.copyResultToClipboard()
        return (0.0, "OK", 2 )

    def func_paste(self, parameters = None):
        self.pasteFromClipboard(*parameters if parameters else None)
        return (0.0, "OK", 2 )

    def func_dec(self, parameters = None):
        return self.defineNumberFormat(Gui.NumFormat.DEC)

    def func_hex(self, parameters = None):
        return self.defineNumberFormat(Gui.NumFormat.HEX)

    def func_bin(self, parameters = None):
        return self.defineNumberFormat(Gui.NumFormat.BIN)

    def func_frc(self, parameters = None):
        return self.defineNumberFormat(Gui.NumFormat.FRC)

    def func_round(self, parameters = None):
        self.gui.set_Round(self.gui.set_ButtonPressed(Gui.Item.TB_Round, self.cfg.set_Round(not self.cfg.get_Round())))
        return (0.0, "OK", 2 )

    def func_reuse(self, parameters = None):
        self.gui.set_ReUse(self.gui.set_ButtonPressed(Gui.Item.TB_ReUse, self.cfg.set_ReUse(not self.cfg.get_ReUse())))
        return (0.0, "OK", 2 )

    def func_tcmvc(self, parameters = None):
        if len(parameters) != 3:
            return (0.0, "Error, invalid parameters")
        result = self.parse(parameters[2])
        return ( self.tc.mV_to_Celsius(parameters[1], result[0]), "OK", 1 )

    def func_tccmv(self, parameters = None):
        if len(parameters) != 3:
            return (0.0, "Error, invalid parameters")
        result = self.parse(parameters[2])
        return ( self.tc.Celsius_to_mV(parameters[1], result[0]), "OK", 1 )

    def func_roman(self, parameters = None):
        if parameters == None or len(parameters) < 2:
            raise ValueError("Invalid parameter list")
        text = str(parameters[1]).strip().strip("\"")
        for i in range(len(text)):
            if not self.ro.is_roman_digit(text[i].upper()):
                parameters[1] = text[:i]
                parameters.append(text[i:])
                break
        p = list(filter(None, parameters))[1:]
        sum = 0
        mode = "DecimalToRoman"
        for text in p:
            op = "+"
            if self.ro.is_roman_number_string(text):
                result = (self.parse_RomanNumber(text), "OK", 1)
                mode = "RomanToDecimal"
            else:
                if text[0] == "*": op = "*"
                if text[0] == "/": op = "/"
                if op != "+": text = text[1:]
                result = self.__parse(text)

            if result[1] == "OK":
                if op == "+":
                    sum += result[0]
                elif op == "*":
                    sum *= result[0]
                elif op == "/" and result[0] != 0:
                    sum /= result[0]
                else:
                    raise ZeroDivisionError(f"Parsing error with \"{text}\"")
        if mode == "DecimalToRoman":
            sum = self.ro.decimal2roman(sum)
        return (sum, "OK", 1)

    def var_get_index(self, name):
        if not "[" in name or not "]" in name:
            return -1
        idx = int(name[name.find("[")+1:name.rfind("]")])
        return idx

    def enum_vars(self, flt=None, start=0, end=-1):
        for name, value in self.__varlist.items():
            i = self.var_get_index(name)
            if name != "pi" and name != "e" and (flt != None and i != -1 and i >= start and (end < 0 or i <= end)):
                yield value
        
    def func_sum(self, parameters = None):
        flt   = None
        start = 0
        end   = -1
        if len(parameters) > 1:
            flt = parameters[1]
            if len(parameters) > 2:
                start = int(self.do_parse(parameters[2])[0])
                if len(parameters) > 3:
                    end = int(self.do_parse(parameters[3])[0])
            s = sum(self.enum_vars(flt, start, end))
        else:
            pass
        return (s, "OK", 1)

    def func_madd(self, parameters = None):
        self.gui.macro_editor()
        return (0.0, "OK", 2 )

    def func_medit(self, parameters = None):
        if parameters and len(parameters) > 1:
            name = parameters[1]
        else:
            name = "default"
        cmd = self.cfg.get_Macro(name)
        self.gui.macro_editor(name, cmd)
        return (0.0, "OK", 2 )

    def func_mrun(self, parameters = None):
        if parameters and len(parameters) > 1:
            name = parameters[1]
        else:
            name = "default"
        self.run_macro(name, self.cfg.get_Macro(name))
        return (0.0, "OK", 2 )
    
    # Filter sub-expressions in variable names, parse and insert results
    def __filter_varname(self, name: str) -> str:
        if not name: return None
        name = name.strip().replace("_", "").replace(",", ".").lower()
        if name[0].isnumeric(): return 

        cnt = name.count("[")
        if cnt != name.count("]"):
            raise SyntaxError("Error, brackets not matching")
        
        if cnt == 0:
            return name
        
        while True:
            end     = name.find("]")
            begin   = name.rfind("[", 0, end)
            prev    = name.rfind("[", 0, begin)
            formula = name[begin+1:end]
            if not formula.isnumeric():
                result = self.__parse(formula)
                if result[1] != "OK":
                    raise ValueError(f"Error, unable to parse \"{formula}\"")
                value = result[0]
                if type(value) == float:
                    value = int(value)
                name = name[:begin+1] + str(value) + name[end:]
                continue

            sub_name = name[prev+1:end+1]
            cnt = name.count("[")
            if cnt < 2:
                return sub_name
            
            value = self.__get_variable_unchecked(sub_name)
            if type(value) == float:
                value = int(value)
            name = name[:prev+1] + str(value) + name[end+1:]

    def handle_number_grouping(self, formula):
        if "," in formula and "." in formula:
            s = ''.join(re.sub(r'[^0-9+-]', '', formula))
            if s.isnumeric():
                i1 = formula.rfind(",")
                i2 = formula.rfind(".")
                if abs(i1 - i2) == 4:
                    formula = formula.replace(",", ".")
                    while formula.count(".") > 1:
                        i = formula.find(".")
                        formula = formula[:i] + formula[i+1:]
        else:
            formula = formula.replace(",", ".")
        return formula
        
    def __prepare_parsing(self, formula: str) -> str:
        formula = formula.replace("^", "**").strip()
        
        # Check digit grouping
        formula = self.handle_number_grouping(formula)
        
        # Filter odd brackets
        begin = formula.count("(")
        end = formula.count(")")
        if begin != end:
            while begin < end:
                formula = "(" + formula
                begin += 1
            while end < begin:
                formula = formula + ")"
                end += 1

        # Replace power variants with parsable versions
        sub = ""
        begin = 0
        while begin < len(formula):
            rep = Calculator.__pow_substitudes.get(formula[begin], "")
            if rep:
                if begin == 0:
                    formula = rep + formula[1:]
                    begin += 1
                    continue
                sub += rep
                end = begin + 1
                while (end < len(formula)) and (rep := Calculator.__pow_substitudes.get(formula[end], "")):
                    sub += rep
                    end += 1
                if formula[begin - 1] == "(":
                    formula = formula[:begin-1] + "**(" + sub + formula[end:]
                else:
                    formula = formula[:begin] + "**" + sub + formula[end:]
                begin += len(sub)
            begin += 1

        # Parse special formats like date/time and roman numbers            
        while True:
            i = formula.find("#")
            if i > -1:
                iso, iso_len = self.times.parseToISO(formula[i+1:])
                if iso:
                    factor = str(self.times.get_Factor(iso))
                    formula = formula[:i] + factor + formula[i + 1 + iso_len:]
                else:
                    ro_digit = formula[i+1]
                    if self.ro.is_roman_digit(ro_digit):
                        ro_num, ro_len = self.ro.parseRomanNumberString(formula[i+1:])
                        formula = formula[:i] + str(ro_num) + formula[i + 1 + ro_len:]
                    else:
                        break
            else:
                break
        return formula

    # Parser main entry
    def parse(self, formula: str) -> float:
        if not formula: return ( 0.0, "Error", False )
        return self.__parse(self.__prepare_parsing(formula))

    # Sub-parser for already prepared strings
    def __parse(self, formula: str) -> tuple:
        while True:
            if self.is_VariableExisting(formula):
                return self.get_InitializedVariable(formula)
            if "[" in formula:
                end = formula.find("]")
                begin = formula.rfind("[", 0, end) - 1
                while begin > -1 and formula[begin].isalnum():
                    begin -= 1
                name = self.__filter_varname(formula[begin+1:end+1])
                value = self.get_InitializedVariable(name)
                formula = formula[:begin+1] + str(value[0]) + formula[end+1:]
                continue
            if formula.startswith(".") and not formula[1].isnumeric():
                result = self.cmd(formula)
                formula = str(result[0])
                if result[1] != "OK" or result[2] != 1 or self.ro.is_roman_number_string(formula):
                    return result
            try:
                return ( eval(formula, self.get_updated_varlist(), self.get_Cmd()), "OK", True )
            except NameError as ne:
                name = (str(ne).split("'"))[1]
                self.set_Variable(name, 0.0)
                formula = formula.replace(name, "0.0")
            except Exception as e:
                return ( 0.0, f"Error: {e}", False )

    def get_updated_varlist(self):
        varlist = self.get_VariableContent()
        varlist["date"]=self.times.get_current_date_value()
        varlist["time"]=self.times.get_current_time_value()
        return varlist
        
    def parse_number(self, text: str):
        if self.ro.is_roman_number_string(text):
            return (self.parse_RomanNumber(text), "OK", 1)
        else:
            return self._parse(text)

    def put_edit_string(self, string: str):
        self.gui.put_EditString(string)

    def asset_path(self, filename):
        if getattr(sys, 'frozen', False):
            return os.path.join(sys._MEIPASS, filename)
        return os.path.join(filename)

    def read_license_file(self) -> str:
        path = self.asset_path("LICENSE")
        with open(path, 'r', encoding='utf-8') as f:
            license_text = f.read()
        return license_text
        
    def handle_keyboard_event(self, math_function):
        self.put_edit_string(f"{math_function}(" if len(math_function) > 1 else math_function)

    def pasteFromClipboard(self, fu=".paste", varname=None, *index_list):
        try:
            parameter_list = list(filter(lambda s: len(s) > 0, pyperclip.paste().strip().replace("\t", " ").split(" ")))
            if index_list:
                index_list = list(map(lambda x: int(float(x)), index_list))
                parameter_list = [parameter_list[i] if 0 <= i < len(parameter_list) else None for i in index_list]
            for n, element in enumerate(parameter_list):
                if self.times.is_DateTimeString(element):
                    element = "#" + element
                elif self.ro.is_roman_number_string(element):
                    element = "#" + element
                else:
                    element = self.handle_number_grouping(element)
                if varname:
                    s = (f"{varname}[{n}]={element}")
                else:
                    s = element
                self.gui.add_EditString(s)
                self.do_parse(s)
        except Exception as e:
            print(e)
            
    def create_html_help_text(self) -> str:
        text = '<html><body>'

        text += general_usage

        text += '<p><h2>Command functions:</h2>'
        text += '<ul style="list-style-type: none;">'
        for key, value in self.__funclist.items():
            text += f'<li style="margin-bottom: 4px;"><b>{key}</b>   {value[1]}</li>'
        text += '</ul></p>'
        
        text += '<p><h2>Math functions:</h2>'
        text += '<ul style="list-style-type: none;">'
        math_functions = MathWrapper.get_help_list()
        for key, hint in math_functions.items():
            text += f'<li style="margin-bottom: 4px;"><b>{key}(x)</b>   {hint}</li>'
        text += '</ul></p>'

        text += '</body></html>'

        return text

    def interval_update(self):
        self.__varlist["date"] = self.times.get_current_date()
        self.__varlist["time"] = self.times.get_current_time()
        self.gui.set_VariableContent(self.get_VariableContent())

    def handle_varlist_event(self, event):
        self.put_edit_string(event[1])

    def update_default_variables(self):
        varlist = self.get_VariableContent()
        default_vars = self.cfg.get_default_variables()
        for varname in default_vars.keys():
            value = varlist[varname]
            default_vars[varname] = value
        self.cfg.store_default_variables(default_vars)

    def run_macro(self, name="default", data=[]):
        for command in data:
            result = self.do_parse(command)
            if result[1] == "OK":
                self.gui.set_Result(result[0])

    def handle_close_macro_editor(self, event):
        if len(event) == 2:
            self.cfg.set_Macro(name=event[0], macro=event[1])

    def handle_delete_macro(self, name):
        self.cfg.delete_Macro(name)

    def handle_hotkey(self, hotkey: str):
        if hotkey.startswith("F"):
            macro_names = self.cfg.get_Macro_List()
            macro_index = int(hotkey[1:3]) - 1
            if 0 <= macro_index < len(macro_names):
                self.cmd(f".mrun {macro_names[macro_index]}")

    def guiCallback(self, id: Gui.Item, event = None):
        match id:
            case Gui.Item.Math_Function:
                self.handle_keyboard_event(event)
            case Gui.Item.VarList:
                self.handle_varlist_event(event)
            case Gui.Item.Timer:
                self.interval_update()
            case Gui.Item.Result:
                pass
            case Gui.Item.Editor:
                return self.do_parse(event)
            case Gui.Item.EditorMacro:
                self.handle_close_macro_editor(event)
            case Gui.Item.EditorDelMacro:
                self.handle_delete_macro(event)
            case Gui.Item.Cmd_onClose:
                self.exit()
            case Gui.Item.Cmd_getMacros:
                return (self.cfg.get_Macro_List(), "OK", 1)
            case Gui.Item.Cmd_getMacCode:
                pass
            case Gui.Item.Cmd_hotkey:
                self.handle_hotkey(event)
            case Gui.Item.Menu_Clear:
                self.cmd(".cls")
            case Gui.Item.Menu_Delete:
                self.cmd(".del")
            case Gui.Item.Menu_Reset:
                self.cmd(".res")
            case Gui.Item.Menu_DefVars:
                self.cmd(".dvar")
            case Gui.Item.Menu_DefUpdate:
                self.cmd(".udv")
            case Gui.Item.Menu_Help:
                self.cmd(".help")
            case Gui.Item.Menu_License:
                self.cmd(".lic")
            case Gui.Item.Menu_Copy:
                self.cmd(".copy")
            case Gui.Item.Menu_Exit:
                self.cmd(".exit")
            case Gui.Item.Menu_MacroAdd:
                self.cmd(".madd")
            case Gui.Item.Menu_MacroEdit:
                self.cmd(f".medit {event}")
            case Gui.Item.Menu_MacroRun:
                self.cmd(f".mrun {event}")

            case Gui.Item.Popup_Varl_rmv:
                self.cmd(f".rmv {event}")

            case Gui.Item.TB_Trashcan:
                self.cmd(".cls")
            case Gui.Item.TB_Delete:
                self.cmd(".del")
            case Gui.Item.TB_ReUse:
                self.cmd(".reuse")
            case Gui.Item.TB_Round:
                self.cmd(".round")
            case Gui.Item.TB_Dec:
                self.cmd(".dec")
            case Gui.Item.TB_Hex:
                self.cmd(".hex")
            case Gui.Item.TB_Bin:
                self.cmd(".bin")
            case Gui.Item.TB_Frc:
                self.cmd(".frc")
            case Gui.Item.TB_Deg:
                self.cmd(".deg")
            case Gui.Item.TB_Rad:
                self.cmd(".rad")
            case _:
                print(f"GUI callback error: {id}")
        return None
