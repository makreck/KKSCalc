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

class RomanNumber:
    def __init__(self):
        pass      

    __roman_digits = { 
                    "ↈ": 100000,
                    "ↇ":  50000,
                    "ↂ": 10000,
                    "ↁ":  5000,
                    "M":  1000,
                    "CM": 900,
                    "D":  500,
                    "CD": 400,
                    "C":  100,
                    "L":  50,
                    "X":  10,
                    "IX": 9,
                    "V":  5,
                    "IV": 4,
                    "I":  1,
                    }

    def is_roman_digit(self, digit: str) -> bool:
        return digit.upper() in RomanNumber.__roman_digits
        
    def is_roman_number_string(self, string: str) -> bool:
        for c in string:
            if not self.is_roman_digit(c):
                return False
        return True
        
    def roman2decimal(self, roman_number: str) -> float:
        return self.parseRomanNumberString(roman_number)[0]
    
    def parseRomanNumberString(self, roman_number: str) -> tuple:
        roman_number = roman_number.strip().upper()
        sum = 0
        i = 0
        while i < len(roman_number):
            if (i < (len(roman_number) - 1)):
                cc = roman_number[i:i + 2]
                if self.is_roman_digit(cc):
                    sum += RomanNumber.__roman_digits[cc]
                    i += 2
                    continue
            c = roman_number[i]
            if self.is_roman_digit(c):
                sum += RomanNumber.__roman_digits[c]        
                i += 1
            else:
                break
        return (sum, i,)

    def decimal2roman(self, value: float) -> str:
        integer = int(round(float(value), 0))
        roman_number = ""
        for key in RomanNumber.__roman_digits.keys():
            value = RomanNumber.__roman_digits[key]
            count = integer // value
            roman_number += key * count
            integer %= value
        return roman_number            
