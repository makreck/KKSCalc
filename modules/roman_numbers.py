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
        return digit in RomanNumber.__roman_digits
        
    def roman2decimal(self, roman_number: str) -> float:
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
                raise ValueError(f"Error, invalid digit \"{c}\".")
        return sum

    def decimal2roman(self, value: float) -> str:
        integer = int(round(float(value)))
        roman_number = ""
        for key in RomanNumber.__roman_digits.keys():
            value = RomanNumber.__roman_digits[key]
            count = integer // value
            roman_number += key * count
            integer %= value
        return roman_number            
