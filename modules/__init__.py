import sys, os, math, platform, re, pyperclip, cairosvg, random, json, time
import tkinter as tk

from datetime import datetime as dt
from tkinterweb import HtmlFrame
from pathlib import Path
from fractions import Fraction
from tkinter import ttk
from tkinter.font import Font
from tkinter import scrolledtext
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
from modules.calculator import Calculator
