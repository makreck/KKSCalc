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
    
    def get_CommandList() -> dict:
        return MathWrapper.__cmdlist

    def get_AngleMode():
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
    def __f_abs(x: float) -> float:
        return abs(x)

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

    def __f_log(x: float) -> float:
        return math.log(x)

    def __f_exp(x: float) -> float:
        return math.exp(x)

    def __f_floor(x: float) -> float:
        return math.floor(x)

    def __f_ceil(x: float) -> float:
        return math.ceil(x)

    def __f_fac(x: float) -> float:
        return math.factorial(x)

    # Global math command table for wrapped commands
    __cmdlist = {
            "sin":    __f_sin,
            "asin":   __f_asin,
            "cos":    __f_cos,
            "acos":   __f_acos,
            "tan":    __f_tan,
            "atan":   __f_atan,
            "cot":    __f_cot,
            "acot":   __f_acot,

            "sinh":   __f_sinh,
            "arsinh": __f_arsinh,
            "cosh":   __f_cosh,
            "arcosh": __f_arcosh,
            "tanh":   __f_tanh,
            "artanh": __f_artanh,
            "coth":   __f_coth,
            "arcoth": __f_arcoth,

            "sec":    __f_sec,
            "asec":   __f_asec,
            "csc":    __f_csc,
            "acsc":   __f_acsc,

            "sqrt":   __f_sqr,
            "sqr":    __f_sqr,
            "cbr":    __f_cbr,
            "ln":     __f_log,
            "log":    __f_log,
            "log10":  __f_log10,
            "exp":    __f_exp,
            "int":    __f_floor,
            "floor":  __f_floor,
            "ceil":   __f_ceil,
            "mod":    __f_mod,
            "sgn":    __f_sgn,
            "abs":    __f_abs,
            "rnd":    __f_rnd,
            "fac":    __f_fac,
            }
