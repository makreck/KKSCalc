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

import time
from datetime import datetime as dt

class Times:
    gregorianCalendarBegin_ISO = "1582-02-24T00:00:00"
    seconds_per_day = 24.0 * 60.0 * 60.0
    
    def __init__(self):
        pass
    
    def get_Factor(self, iso_date: str) -> float:
        iso_date, _ = self.parseToISO(iso_date)
        if not iso_date:
            return 0.0
        if iso_date.startswith("T"):
            t = iso_date[1:].split(":")
            h = int(t[0])
            m = int(t[1])
            s = int(t[2])
            return (h * 3600 + m * 60 + s) / Times.seconds_per_day
        diff = dt.fromisoformat(iso_date) - dt.fromisoformat(Times.gregorianCalendarBegin_ISO)
        return diff.days + (diff.seconds / Times.seconds_per_day)

    def get_DayDiff(self, iso1: str, iso2: str) -> float:
        return self.get_Factor(iso2) - self.get_Factor(iso1)
    
    def parse_date(self, string) -> tuple:
        if type(string) != str:
            string = str(string)

        i = string.find("#")
        if i > -1:
            while i > 0 and not string[i].isnumeric():
                i -= 1
            string = string[:i+1]
        parts = string.strip().upper().replace("T", " ").split(" ")

        date_parts = []
        time_parts = []        
        for s in parts:
            n = s.count(":")
            if n == 1 or n == 2:
                time_parts = s.split(":")
                continue
            
            n = s.count(".")
            if n >= 1:
                date_parts = s.split(".")
                continue

            n = s.count("-")
            if n >= 1:
                date_parts = s.split("-")
                continue

        length = -1
        time_parts = time_parts[:3]
        for i in range(min(3, len(time_parts))):
            length = length + 1 + min(2, len(time_parts[i]))
        date_parts = date_parts[:3]
        for i in range(min(3, len(date_parts))):
            length = length + 1 + min(4, len(date_parts[i]))

        if len(date_parts) > 0:
            while len(date_parts) < 3:
                date_parts.append(0)
            for i in range(len(date_parts)):
                try:
                    date_parts[i] = max(1, int(float(date_parts[i])))
                except:
                    date_parts[i] = 1
            if date_parts[0] < 1582 and date_parts[1] < 1582 and date_parts[2] < 1582:
                date_parts = []
            else:    
                if date_parts[1] >= 1582:
                    date_parts[0], date_parts[1] = date_parts[1], date_parts[0]
                if date_parts[2] >= 1582:
                    date_parts[0], date_parts[2] = date_parts[2], date_parts[0]

        if len(time_parts) > 0:
            for i in range(len(time_parts)):
                try:
                    time_parts[i] = int(float(time_parts[i]))
                except:
                    time_parts[i] = 0
            while len(time_parts) < 3:
                time_parts.append(0)
            
        return (date_parts, time_parts, length)

    def parseToISO(self, string: str) -> str:
        date_parts, time_parts, length = self.parse_date(string.upper())
        if date_parts and time_parts:
            return ( f"{date_parts[0]:04d}-{date_parts[1]:02d}-{date_parts[2]:02d}T{time_parts[0]:02d}:{time_parts[1]:02d}:{time_parts[2]:02d}", length )
        elif date_parts:
            return ( f"{date_parts[0]:04d}-{date_parts[1]:02d}-{date_parts[2]:02d}", length )
        elif time_parts:            
            return ( f"T{time_parts[0]:02d}:{time_parts[1]:02d}:{time_parts[2]:02d}", length )
        else:
            return ( "", length )
        
    def is_DateTimeString(self, string: str) -> bool:
        date_parts, time_parts, length = self.parse_date(string)
        return len(date_parts) > 0 or len(time_parts) > 0

    def get_currentDatetime(self):
        string, _ = self.parseToISO(dt.fromtimestamp(time.time()))
        return string

    def parse(self, parts: tuple):
        dat = ""
        if len(parts[0]) == 3:
            d = parts[0]
            dat = f"{d[0]-d[1]-d[2]}"
        tim = ""
        if len(parts[1]) >= 2:
            t = parts[1]
            if len(t) < 3:
                t.append("00")
            tim = f"{t[0]:t[1]:s[2]}"
        return (dt.combine(date=dat, time=tim) - dt.fromisoformat(Times.gregorianCalendarBegin_ISO)).seconds / Times.seconds_per_day

    def get_current_time(self):
        return dt.now().strftime("#T%H:%M:%S")        

    def get_current_date(self):
        return dt.now().strftime("#%Y-%m-%d")        

    def get_current_time_value(self):
        return self.get_Factor(self.get_current_time()[1:])

    def get_current_date_value(self):
        s = self.get_current_date()[1:]
        return self.get_Factor(s)
    