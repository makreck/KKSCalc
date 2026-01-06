import sys
from modules.gui import Gui
from modules.parser import Parser
from modules.config import Config
from modules.math_wrapper import MathWrapper        

class Calculator:
    
    def __init__(self):
        self.parser = Parser()
        self.cfg = Config().load()
        self.gui = Gui(self.guiCallback).app_window(self.cfg.get_WindowPos("MainWindow"))
        self.setupFunctionList()
        self.setupParser()
        self.setupGui()
        
    def setupParser(self):
        self.parser.set_VariableContent(self.cfg.get_VariableContent())
        self.parser.set_AngleMode(self.cfg.get_AngleMode())
        
    def setupGui(self):
        amode = self.cfg.get_AngleMode()
        self.gui.set_ButtonPressed(Gui.Item.TB_Deg, amode == MathWrapper.AngleMode.DEG)
        self.gui.set_ButtonPressed(Gui.Item.TB_Rad, amode != MathWrapper.AngleMode.DEG)
        self.gui.set_Round(self.gui.set_ButtonPressed(Gui.Item.TB_Round, self.cfg.get_round()))
        self.gui.set_ReUse(self.gui.set_ButtonPressed(Gui.Item.TB_ReUse, self.cfg.get_reuse()))
        self.gui.set_VariableContent(self.parser.get_VariableContent())
        self.gui.set_ScreenContent(self.cfg.get_ScreenContent())
        self.defineNumberFormat(self.cfg.get_NumberFormat())

    def setupFunctionList(self):
        self.funclist = {
            ".cls":   ( self.func_cls,   "Clear editor" ),
            ".del":   ( self.func_del,   "Delete variables" ),
            ".res":   ( self.func_res,   "Reset, delete variables, clear editor" ),
            ".deg":   ( self.func_deg,   "Use degrees for trigonometric functions" ),
            ".rad":   ( self.func_rad,   "Use radians for trigonometric functions" ),
            ".copy":  ( self.func_copy,  "Copy result to clipboard" ),
            ".dec":   ( self.func_dec,   "Use decimal system for outputs" ),
            ".hex":   ( self.func_hex,   "Use hexadecimal system for outputs" ),
            ".bin":   ( self.func_bin,   "Use binary system for outputs" ),
            ".round": ( self.func_round, "Round results for business use" ),
            ".reuse": ( self.func_reuse, "Re-use result for next calculation" ),
            ".help":  ( self.func_help,  "Show common or specific help" ),
            ".exit":  ( self.func_exit,  "Terminate application" ),
            }

    def func_exit(self, parameters = None):
        self.gui.closeWindow()
        exit()
        
    def func_help(self, parameters = None):
        print("Help: ", parameters)
        return (0.0, "OK", 2 )
        
    def func_cls(self, parameters = None):
        print("\033c") # *** clear terminal output
        self.gui.clear()
        return (0.0, "OK", 0 )

    def func_del(self, parameters = None):
        self.parser.clr_Variables()
        self.gui.set_VariableContent(self.parser.get_VariableContent())
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
        self.cfg.set_VariableContent(self.parser.get_VariableContent())
        self.cfg.set_WindowPos("MainWindow", self.gui.get_WindowPos())
        self.cfg.set_ScreenContent(self.gui.get_ScreenContent())
        self.cfg.save()

    def cmd(self, command: str):
        command = command.strip().replace(" ", ",").split(",")
        cmdFunction = self.funclist.get(command[0], None)
        if cmdFunction != None:
            return cmdFunction[0](command)
        else:
            raise SyntaxError(f"Invalid command \"{command}\"")

    def set_AngleMode(self, amode = MathWrapper.AngleMode.DEG):
        self.parser.set_AngleMode(amode)
        self.cfg.set_AngleMode(amode)
        self.gui.set_ButtonPressed(Gui.Item.TB_Deg, amode == MathWrapper.AngleMode.DEG)
        self.gui.set_ButtonPressed(Gui.Item.TB_Rad, amode != MathWrapper.AngleMode.DEG)
        
    def guiCallback(self, id: Gui.Item, event = None):
        match id:
            case Gui.Item.VarList:
                self.gui.put_EditString(event[1])
            case Gui.Item.Result:
                self.gui.set_Result(0.0)
            case Gui.Item.Editor:
                return self.parse(event)
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
    
    def parse(self, string: str) -> float:
        result = (0.0, "OK", False)
        elements = string.strip().lower().replace(",", ".").split("=")
        try:
            formula = elements[-1]
            if formula.startswith("."):
                result = self.cmd(formula)
            else:            
                formula = formula.replace(" ", "")
                result = self.parser.parse(formula)
                if (len(elements) > 1) and result[2]:
                    self.parser.set_Variable(elements[0], result[0])
            self.gui.set_VariableContent(self.parser.get_VariableContent())
        except Exception as e:
            result = ( 0.0, f"Error: {e}", False )
        return result


