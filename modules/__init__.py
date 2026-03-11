# Dependencies (all):

import sys, os, math, platform, re, pyperclip, random, json, time, subprocess
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


# For using cairosvg ...
if platform.system() == "Windows":
    # On Windows, cairosvg is not working properly. So, we always need
    # ready for use PNG images for the buttons!
    pass
elif platform.system() == "Linux":
    # On Linux, cairosvg is available and working properly. So, we can
    # use the internal SVG resources to build the PNG images we need
    # for running on the other operating systems.
    import cairosvg
else:
    # On other OS, like MacOS, it is currently unknown if cairosvg library
    # is available. So, we also use the PNG images only
    pass
