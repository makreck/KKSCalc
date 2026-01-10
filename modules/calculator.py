import sys, math
from modules.gui import Gui
from modules.config import Config
from modules.math_wrapper import MathWrapper        
from modules.times import Times
from modules.roman_numbers import RomanNumber
from modules.thermocouple import Thermocouple

class Calculator:

    __funclist = {
        ".cls":   ( "func_cls",   "Clear editor" ),
        ".del":   ( "func_del",   "Delete variables" ),
        ".res":   ( "func_res",   "Reset, delete variables, clear editor" ),
        ".deg":   ( "func_deg",   "Use degrees for trigonometric functions" ),
        ".rad":   ( "func_rad",   "Use radians for trigonometric functions" ),
        ".copy":  ( "func_copy",  "Copy result to clipboard" ),
        ".dec":   ( "func_dec",   "Use decimal system for outputs" ),
        ".hex":   ( "func_hex",   "Use hexadecimal system for outputs" ),
        ".bin":   ( "func_bin",   "Use binary system for outputs" ),
        ".round": ( "func_round", "Round results for business use" ),
        ".reuse": ( "func_reuse", "Re-use result for next calculation" ),
        ".rom":   ( "func_roman", "Convert given number into roman digits" ),
        ".tcmvc": ( "func_tcmvc", "Convert thermocouple voltage in mV into °Celsius" ),
        ".tccmv": ( "func_tccmv", "Convert °Celsius into thermocouple voltage in mV" ),
        ".help":  ( "func_help",  "Show common or specific help" ),
        ".exit":  ( "func_exit",  "Terminate application" ),
    }

    __default_varlist = { 
            "pi": math.pi,
            "e":  math.e,
        }

    __exponental_specials    = "⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺"
    __exponental_substitudes = "0123456789-+"

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
        self.gui.set_Round(self.gui.set_ButtonPressed(Gui.Item.TB_Round, self.cfg.get_round()))
        self.gui.set_ReUse(self.gui.set_ButtonPressed(Gui.Item.TB_ReUse, self.cfg.get_reuse()))
        self.gui.set_VariableContent(self.get_VariableContent())
        self.gui.set_ScreenContent(self.cfg.get_ScreenContent())
        self.defineNumberFormat(self.cfg.get_NumberFormat())

    def defineNumberFormat(self, fmt: str):
        fmt = fmt[:3].strip().lower()
        self.cfg.set_NumberFormat(fmt)
        self.gui.set_NumberFormat(fmt)
        self.gui.set_ButtonPressed(Gui.Item.TB_Dec, fmt == "dec")
        self.gui.set_ButtonPressed(Gui.Item.TB_Hex, fmt == "hex")
        self.gui.set_ButtonPressed(Gui.Item.TB_Bin, fmt == "bin")
        self.gui.set_Result(self.gui.get_Result())
        return (0.0, "OK", 2 )

    def run(self):
        self.gui.dispatch()
        return self

    def get_configFile(self):
        path = sys.path[0] + "/KKSCalc.cfg"

    def exit(self, event = None):
        self.cfg.set_VariableContent(self.get_VariableContent())
        self.cfg.set_WindowPos("MainWindow", self.gui.get_WindowPos())
        self.cfg.set_ScreenContent(self.gui.get_ScreenContent())
        self.cfg.save()

    def set_AngleMode(self, amode = MathWrapper.AngleMode.DEG):
        self.set_AngleMode(amode)
        self.cfg.set_AngleMode(amode)
        self.gui.set_ButtonPressed(Gui.Item.TB_Deg, amode == MathWrapper.AngleMode.DEG)
        self.gui.set_ButtonPressed(Gui.Item.TB_Rad, amode != MathWrapper.AngleMode.DEG)

    def do_parse(self, string: str) -> float:
        result = (0.0, "OK", False)
        elements = string.strip().lower().replace(",", ".").split("=")
        try:
            result = self.parse(elements[-1]) # **** .replace(" ", ""))
            if (len(elements) > 1) and result[2]:
                self.set_Variable(elements[0], result[0])
            self.gui.set_VariableContent(self.get_VariableContent())
        except Exception as e:
            result = ( 0.0, f"Error: {e}", False )
        return result

    def get_Cmd(self) -> dict:
        return MathWrapper.get_CommandList()

    def parse(self, formula: str) -> float:
        if not formula:
            return ( 0.0, "Error", False )
        if formula.startswith("."):
            result = self.cmd(formula)
            formula = str(result[0])
            if result[1] != "OK" or result[2] != 1 or self.ro.is_roman_number_string(formula):
                return result
        formula = formula.replace("^", "**")
        return self.__parse_partial(self.__filter_brackets(self.__substitude_specials(formula)))

    def __substitude_specials(self, formula: str) -> str:
        pos = -1
        for i in range(len(formula)):
            n = Calculator.__exponental_specials.find(formula[i])
            if n != -1:
                if pos == -1: pos = i
                formula = formula.replace(Calculator.__exponental_specials[n], Calculator.__exponental_substitudes[n])                
        if pos > -1:
            formula = formula[:pos] + "**" + formula[pos:]
        return formula        

    def __replaceSpecialParts(self, formula: str) -> str:
        while True:
            i = formula.find("#")
            if i > -1:
                ro_digit = formula[i+1]
                if self.ro.is_roman_digit(ro_digit):
                    ro_num, ro_len = self.ro.parseRomanNumberString(formula[i+1:])
                    formula = formula[:i] + str(ro_num) + formula[i + 1 + ro_len:]
                else:
                    iso, iso_len = self.times.parseToISO(formula[i+1:])
                    if iso:
                        factor = str(self.times.get_Factor(iso))
                        formula = formula[:i] + factor + formula[i + 1 + iso_len:]
                    else:
                        break
            else:
                break
        return formula

    def __parse_partial(self, formula: str) -> float:
        formula = self.__replaceSpecialParts(formula)
        flag = True
        while flag:
            flag = False
            count  = 0
            start  = 0
            length = len(formula)
            for i in range(length):
                c = formula[i]
                if c == "[":
                    if count == 0:
                        start = i + 1
                    count += 1
                if c == "]":
                    count -= 1
                    if count == 0:
                        k = start
                        while (k >= 0) and (formula[k].isalnum()): k -= 1
                        inner = formula[k-1:i+1]
                        result = self.get_InitializedVariable(inner)
                        if result[1]:
                            inner_value = result[0]
                            formula = formula.replace(inner, str(inner_value))
                        else:
                            inner = formula[start:i]
                            inner_value = self.__parse_partial(inner)
                            formula = formula[:start] + str(inner_value[0]) + formula[i:]
                        flag = True
                        break
            if count > 0:
                for i in range(count):
                    formula = formula + "]"
        return self.__parse(formula)

    def __parse(self, formula: str) -> float:
        while True:
            if self.is_VariableExisting(formula):
                result = self.get_InitializedVariable(formula)
                if result[1]:
                    return (result[0], "OK", 1)
            try:
                return ( eval(formula, self.get_VariableContent(), self.get_Cmd()), "OK", True )
            except NameError as ne:
                name = (str(ne).split("'"))[1]
                self.set_Variable(name, 0.0)
            except Exception as e:
                return ( 0.0, f"Error: {e}", False )

    def __filter_brackets(self, string: str) ->str:
        begin = string.count("(")
        end = string.count(")")
        if begin != end:
            while begin < end:
                string = "(" + string
                begin += 1
            while end < begin:
                string = string + ")"
                end += 1
        return string

    def __filter_varname(self, name: str) -> str:
        if not name:
            return None
        
        name = name.strip().replace("_", "").replace(",", ".").lower()
        if name[0].isnumeric():
            return 
        _name = ""
        cmp = ""
        flag = False
        for c in name:
            if c == cmp: continue
            if c == '[': 
                cmp = c
                flag = True
            if c == ']': 
                if not cmp: continue
                cmp = ""
            _name += c

        if flag:
            if cmp: _name += "]"
            start = _name.find("[")
            end = _name.find("]", start + 1)
            substr = _name[start+1:end]
            index = str(int(self.parse(substr)[0]))
            _name = _name[0:start+1] + index + _name[end:]

        name = ""
        for c in _name:
            if c.isalnum() or c == '_' or c == '[' or c == ']':
                name += c

        return name

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

    def set_Variable(self, name: str, value = 0.0):
        name = self.__filter_varname(name)
        if name:
            if name == "pi" or name == "e":
                raise ValueError(f"Not allowed to change common constant \"{name}\".")
            self.__varlist[name] = value # *** float(value)

    def normalize_variable_name(self, name: str) -> str:
        length = len(name)
        dot = 0
        if ("[" in name) and ("]" in name):
            length = name.index("[")
            end = name.index("]")
            var_index = name[length+1:end]
            for c in var_index:
                if c == ".":
                    dot += 1
                    if dot > 1:
                        return None
                if not c.isnumeric() and c != ".":
                    return None
            index = int(float(var_index))
            name = f"{name[:length]}[{str(index)}]"
        return name.lower()

    def get_InitializedVariable(self, name: str) -> tuple:
        if not self.is_ValidVariable(name):
            return (0.0, False)
        name = self.normalize_variable_name(name)
        if not self.is_VariableExisting(name):
            self.set_Variable(name, 0.0)
            return (0.0, True)
        value = self.__varlist.get(name)
        if value == None:
            return (0.0, False)
        return (value, True)

    def is_ValidVariable(self, name:str) -> bool:
        name = self.normalize_variable_name(name)
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

    def clr_Variables(self):
        self.__varlist = dict(Calculator.__default_varlist)
        return self

    def set_AngleMode(self, mode = MathWrapper.AngleMode.DEG):
        MathWrapper.set_AngleMode(mode)    
        return self

    def get_AngleMode(self) -> MathWrapper.AngleMode:
        return MathWrapper.get_AngleMode()

    def cmd(self, command: str):
        command = command.strip().replace(" ", ",").split(",")
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
        print("Help: ", parameters)
        return (0.0, "OK", 2 )
        
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

    def func_dec(self, parameters = None):
        return self.defineNumberFormat("dec")

    def func_hex(self, parameters = None):
        return self.defineNumberFormat("hex")

    def func_bin(self, parameters = None):
        return self.defineNumberFormat("bin")

    def func_round(self, parameters = None):
        self.gui.set_Round(self.gui.set_ButtonPressed(Gui.Item.TB_Round, self.cfg.set_round(not self.cfg.get_round())))
        return (0.0, "OK", 2 )

    def func_reuse(self, parameters = None):
        self.gui.set_ReUse(self.gui.set_ButtonPressed(Gui.Item.TB_ReUse, self.cfg.set_reuse(not self.cfg.get_reuse())))
        return (0.0, "OK", 2 )

    def func_roman(self, parameters = None):
        if parameters == None or len(parameters) < 2:
            raise ValueError("Invalid parameter list")
        text = str(parameters[1]).upper().strip().strip("\"")
        try:
            number = int(float(text))
        except:
            if not self.ro.is_roman_number_string(text):
                result = self.parse(text)
                number = result[0] # *** int(float(result[0]))
            else:
                number = text
        return (self.parse_RomanNumber(number), "OK", 1 )

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

    def guiCallback(self, id: Gui.Item, event = None):
        match id:
            case Gui.Item.VarList:
                self.gui.put_EditString(event[1])
            case Gui.Item.Result:
                self.gui.set_Result(0.0)
            case Gui.Item.Editor:
                return self.do_parse(event)
            case Gui.Item.Cmd_onClose:
                self.exit()

            case Gui.Item.Menu_Clear:
                self.cmd(".cls")
            case Gui.Item.Menu_Delete:
                self.cmd(".del")
            case Gui.Item.Menu_Reset:
                self.cmd(".res")
            case Gui.Item.Menu_Exit:
                self.cmd(".exit")
            case Gui.Item.TB_Trashcan:
                self.cmd(".cls")
            case Gui.Item.TB_Delete:
                self.cmd(".del")
            case Gui.Item.TB_ReUse:
                self.cmd(".reuse")
            case Gui.Item.TB_Round:
                self.cmd(".round")
            case Gui.Item.TB_Copy:
                self.cmd(".copy")
            case Gui.Item.TB_Dec:
                self.cmd(".dec")
            case Gui.Item.TB_Hex:
                self.cmd(".hex")
            case Gui.Item.TB_Bin:
                self.cmd(".bin")
            case Gui.Item.TB_Deg:
                self.cmd(".deg")
            case Gui.Item.TB_Rad:
                self.cmd(".rad")

            case _:
                print(f"GUI callback error: {id}")
        return None
