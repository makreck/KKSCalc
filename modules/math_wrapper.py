import math
import random
from enum import Enum

class MathWrapper:
    class AngleMode(Enum):
        RAD = "radians",
        DEG = "degrees",

    __amode = AngleMode.DEG
    
    def __init__(self, angle_mode = AngleMode.DEG):
        MathWrapper.set_AngleMode(angle_mode)
    
    def get_command_list() -> dict:
        return { key: value[0] for key, value in MathWrapper.__math_functions.items() }

    def get_keyboard_list() -> dict:
        return { key: [ value[1], value[2], None ] for key, value in MathWrapper.__math_functions.items() if value[3] }
        
    def get_math_functions() -> dict:
        return MathWrapper.__math_functions

    def get_count_of_commands() -> int:
        return len(MathWrapper.__math_functions)
    
    def get_function_of(cmd: str):
        return MathWrapper.__math_functions[cmd][0]

    def get_symbol_of(cmd: str) -> str:
        return MathWrapper.__math_functions[cmd][1]

    def get_description_of(cmd: str) -> str:
        return MathWrapper.__math_functions[cmd][2]
        
    def get_AngleMode() -> AngleMode:
        return MathWrapper.__amode
    
    def set_AngleMode(angle_mode = AngleMode.DEG):
        MathWrapper.__amode = angle_mode
        
    def __from_degrees(x: float) -> float:
        if MathWrapper.__amode == MathWrapper.AngleMode.DEG:
            return math.radians(x)
        else:
            return x

    def __from_radians(x: float) -> float:
        if MathWrapper.__amode == MathWrapper.AngleMode.DEG:
            return math.degrees(x)
        else:
            return x

    # Trigonometric
    def __f_sin(x: float) -> float:
        return math.sin(MathWrapper.__from_degrees(x))

    def __f_asin(x: float) -> float:
        return MathWrapper.__from_radians(math.asin(x))

    def __f_cos(x: float) -> float:
        return math.cos(MathWrapper.__from_degrees(x))

    def __f_acos(x: float) -> float:
        return MathWrapper.__from_radians(math.acos(x))

    def __f_tan(x: float) -> float:
        return math.tan(MathWrapper.__from_degrees(x))

    def __f_atan(x: float) -> float:
        return MathWrapper.__from_radians(math.atan(x))

    def __f_cot(x: float) -> float:
        return 1.0 / MathWrapper.__from_radians(math.tan(x))

    def __f_acot(x: float) -> float:
        return MathWrapper.__from_radians(math.atan(1 / x) if x != 0.0 else math.pi / 2.0)

    # Hyperbolic functions
    def __f_sinh(x: float) -> float:
        return math.sinh(x)

    def __f_arsinh(x: float) -> float:
        return math.asinh(x)

    def __f_cosh(x: float) -> float:
        return math.cosh(x)

    def __f_arcosh(x: float) -> float:
        return math.acosh(x)

    def __f_tanh(x: float) -> float:
        return math.tanh(x)

    def __f_artanh(x: float) -> float:
        return 0.5 * math.log((1 + x) / (1 - x))        

    def __f_coth(x: float) -> float:
        if x == 0.0:
            raise ValueError("coth(0) undefined")
        return 1.0 / math.tanh(x)

    def __f_arcoth(x: float) -> float:
        return 0.5 * math.log((x + 1) / (x - 1))        

    # Secans related
    def __f_sec(x: float) -> float:
        return 1.0 / MathWrapper.__f_cos(x)

    def __f_asec(x: float) -> float:
        if abs(x) < 1:
            raise ValueError("asec(x) defined only for |x| >= 1")
        return math.acos(1 / x)

    def __f_csc(x: float) -> float:
        return 1.0 / math.sin(MathWrapper.__from_degrees(x))

    def __f_acsc(x: float) -> float:
        if abs(x) < 1:
            raise ValueError("acsc(x) defined only for |x| >= 1")
        return math.asin(1 / x)

    # Other math functions
    def __f_int(x: float) -> float:
        return float(int(x))

    def __f_abs(x: float) -> float:
        return abs(x)

    def __f_floor(x: float) -> float:
        return math.floor(x)

    def __f_ceil(x: float) -> float:
        return math.ceil(x)

    def __f_rem(x: float) -> float:
        return x - int(x)

    def __f_rnd(x = 0.0) -> float:
        if x != 0.0:
            random.seed(x)
        return random.random()

    def __f_sgn(x: float) -> float:
        if x < 0.0:
            return -1.0
        elif x > 0.0:
            return +1.0 
        else:
            return 0.0

    def __f_mod(x: float) -> float:
        return x - math.floor(x)

    def __f_sqr(x: float) -> float:
        return math.sqrt(x)

    def __f_cbr(x: float) -> float:
        return math.cbrt(x)

    def __f_log10(x: float) -> float:
        return math.log10(x)

    def __f_log2(x: float) -> float:
        return math.log2(x)

    def __f_loge(x: float) -> float:
        return math.log(x)

    def __f_loge(x: float) -> float:
        return math.ln(x)

    def __f_exp(x: float) -> float:
        return math.exp(x)

    def __f_fac(x: float) -> float:
        return math.factorial(x)

    def __f_erf(x: float) -> float:
        return math.erf(x)

    def __f_erfc(x: float) -> float:
        return math.erfc(x)

    def __f_gamma(x: float) -> float:
        return math.gamma(x)

    def __f_lgamma(x: float) -> float:
        return math.lgamma(x)

    def __f_rgamma(x: float) -> float:
        return 1.0 / math.gamma(x)

    # Global math command table for wrapped commands
    __math_functions = {
            "sqrt":   (__f_sqr,    "√",        "Square root", True,  ),
            "sqr":    (__f_sqr,    "√",        "Square root", False, ),
            "cbr":    (__f_cbr,    "∛",        "Cubic root",  True,  ),

            "ln":     (__f_loge,   "logₑ",     "Natural logarithm (base e)", False, ),
            "log":    (__f_loge,   "logₑ",     "Natural logarithm (base e)", True, ),
            "log2":   (__f_log2,   "log₂",     "Base 2 logarithm",           True, ),
            "log10":  (__f_log10,  "log₁₀",    "Base 10 logarithm",          True, ),
            "exp":    (__f_exp,    "eˣ",       "e to the power of x",        True, ),

            "sin":    (__f_sin,    "sin",      "Sine function", True, ),
            "cos":    (__f_cos,    "cos",      "Cosine function", True, ),
            "tan":    (__f_tan,    "tan",      "Tangent function", True, ),
            "cot":    (__f_cot,    "cot",      "Cotangent function", True, ),
            "asin":   (__f_asin,   "sin⁻¹",    "Arcsine function x", True, ),
            "acos":   (__f_acos,   "cos⁻¹",    "Arccosine function", True, ),
            "atan":   (__f_atan,   "tan⁻¹",    "Arctangent function", True, ),
            "acot":   (__f_acot,   "cot⁻¹",    "Arccotangent function", True, ),

            "sinh":   (__f_sinh,   "sinh",     "Hyperbolic sine function", True, ),
            "cosh":   (__f_cosh,   "cosh",     "Hyperbolic cosine function", True, ),
            "tanh":   (__f_tanh,   "tanh",     "Hyperbolic tangent function", True, ),
            "coth":   (__f_coth,   "coth",     "Hyperbolic cotangent function", True, ),
            "asinh":  (__f_arsinh, "sinh⁻¹",   "Hyperbolic arcus sine function", True, ),
            "acosh":  (__f_arcosh, "cosh⁻¹",   "Hyperbolic arcus cosine function", True, ),
            "atanh":  (__f_artanh, "tanh⁻¹",   "Hyperbolic arcus tangent function", True, ),
            "acoth":  (__f_arcoth, "coth⁻¹",   "Hyperbolic arcus cotangent function", True, ),

            "sec":    (__f_sec,    "sec",      "Secant function", True, ),
            "csc":    (__f_csc,    "csc",      "Cosecant function", True, ),
            "asec":   (__f_asec,   "sec⁻¹",    "Arcus secant function", True, ),
            "acsc":   (__f_acsc,   "csc⁻¹",    "Arcus cosecant function", True, ),

            "int":    (__f_int,    "int",      "Integer of x", True, ),
            "abs":    (__f_abs,    "|x|",      "Absolute value", True, ),
            "floor":  (__f_floor,  "⌊x⌋",      "Floor of x", True, ),
            "ceil":   (__f_ceil,   "⌈x⌉",      "Ceiling of x", True, ),

            "mod":    (__f_mod,    "mod",      "Modulo", True, ),
            "sgn":    (__f_sgn,    "sgn",      "Signum function", True, ),
            "rem":    (__f_rem,    "rem",      "Reminder of x", True, ),
            "rnd":    (__f_rnd,    "rnd",      "Random number function", True, ),
            "fac":    (__f_fac,    "x!",       "Faculty function", True, ),
            
            "erf":    (__f_erf,    "erf",      "Error Function, (2/√π) ∫₀ˣ e⁻ᵗ² dt", True, ),
            "erfc":   (__f_erfc,   "erfc",     "Error Function Complement, 1 - erf(x)", True, ),
            "gamma":  (__f_gamma,  "Γ",        "Gamma Function", True, ),
            "lgamma": (__f_lgamma, "ln(Γ(x))", "Log Gamma Function", True, ),
            "rgamma": (__f_rgamma, "1/Γ",      "Reciprocal Gamma Function", True, ),
            
        }
