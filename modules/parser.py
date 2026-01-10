import math
from modules.math_wrapper import MathWrapper
from modules.times import Times
from modules.roman_numbers import RomanNumber
from modules.thermocouple import Thermocouple

class Parser:
    
    __default_varlist = { 
            "pi": math.pi,
            "e":  math.e,
        }

    __exponental_specials    = "⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺"
    __exponental_substitudes = "0123456789-+"
    
    def __init__(self):
        self.times = Times()
        self.ro = RomanNumber()
        self.tc = Thermocouple()
        self.clr_Variables()
    
    def get_Cmd(self) -> dict:
        return MathWrapper.get_CommandList()

    def parse(self, formula: str) -> float:
        if not formula:
            return ( 0.0, "Error", False )
        formula = formula.replace("^", "**")
        return self.__parse_partial(self.__filter_brackets(self.__substitude_specials(formula)))

    def __substitude_specials(self, formula: str) -> str:
        pos = -1
        for i in range(len(formula)):
            n = Parser.__exponental_specials.find(formula[i])
            if n != -1:
                if pos == -1: pos = i
                formula = formula.replace(Parser.__exponental_specials[n], Parser.__exponental_substitudes[n])                
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
                        result = self.get_initialized_variable(inner)
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
            self.__varlist[name] = float(value)

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
        return name

    def get_initialized_variable(self, name: str) -> tuple:
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
        value = self.__varlist.get(name)
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
        self.__varlist = dict(Parser.__default_varlist)
        return self
    
    def set_AngleMode(self, mode = MathWrapper.AngleMode.DEG):
        MathWrapper.set_AngleMode(mode)    
        return self
        
    def get_AngleMode(self) -> MathWrapper.AngleMode:
        return MathWrapper.get_AngleMode()
    