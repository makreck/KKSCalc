# ==============================================================================
#
#  PROJECT:     "KKSCalc" KKS Desktop Calculator Tool
#  COPYRIGHT:   (C)2025-2026 KKS-Elektronik,  M. Kreck, <makreck@googlemail.com>
#
#  This program is free software: you can redistribute it and/or modify it under
#  the terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  This program is distributed in the hope that it will be useful,   but WITHOUT
#  ANY WARRANTY, without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE, see the GNU General Public License for details.
#
#  You should have received a copy of the  GNU General Public License along with
#  this program. If not, see <https://www.gnu.org/licenses/>.
#  
#  ==============================================================================

# Dependencies (all):

import sys, io, os, math, platform, re, pyperclip, random, json, time, subprocess
import tkinter as tk

from datetime import datetime as dt
from tkinterweb import HtmlFrame
from pathlib import Path
from fractions import Fraction
from tkinter import ttk
from tkinter.font import Font
from tkinter import scrolledtext
from itertools import groupby
from functools import partial
from enum import Enum
from PIL import Image, ImageDraw, ImageTk
from io import BytesIO

from modules.config import Config
from modules.math_wrapper import MathWrapper        
from modules.times import Times
from modules.roman_numbers import RomanNumber
from modules.thermocouple import Thermocouple
from modules.tooltip import ToolTip
from modules.scollframe import ScrollableFrame
from modules.gui import Gui
from modules.app_tools import AppTools
from modules.calculator import Calculator
from modules.helptext import general_usage


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
