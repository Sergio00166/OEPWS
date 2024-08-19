#Code by Sergio00166

import calendar
from datetime import date, datetime
from colors import color

cl = calendar.TextCalendar()

months = [
    "January                   February                   March",
    "April                      May                       June",
    "July                     August                  September",
    "October                   November                  December"
]

def colours(cal, fix=True):
    calendar_str = ""
    cal = cal.split("\n")
    for x in cal: calendar_str += "   " + x + " \n"
    calendar_str = calendar_str[:len(calendar_str) - 1]
    top = calendar_str[:calendar_str.find("\n")]
    days = calendar_str[calendar_str.find("\n"):calendar_str.find("Su") + 3]
    rest = calendar_str[calendar_str.find("Su") + 3:]
    if fix == True: print("\n" + color(top, "G") + color(days, "R") + color(rest, "Y"))
    else:
        day = color(fix, "B")
        fix = rest.split(fix)
        out = color(fix[0], "Y") + day + color(fix[1], "Y")
        print("\n" + color(top, "G") + color(days, "R") + out)

def format_year(arg):
    for x in range(0, 4): arg = arg.replace(months[x], color(months[x], "G"))
    arg = arg.replace("Mo Tu We Th Fr Sa Su", color("Mo Tu We Th Fr Sa Su", "R"))
    cal = arg.split("\n")
    calendar_str = "\n    " + color(cal[0], "B") + "\n"
    for y in cal[1:]:
        if "0" in y or "1" in y: calendar_str += "    " + color(y, "Y") + "\n"
        else: calendar_str += "    " + y + "\n"
    print(calendar_str)

def calendar(arg1):
    current_year = date.today().year
    current_month = date.today().month

    try:

        if "this year" in arg1:
            calendar = cl.formatyear(int(current_year))
            format_year(calendar)

        elif "this month" in arg1:
            calendar = cl.formatmonth(int(current_year), int(current_month))
            colours(calendar)
            
        elif "month" in arg1:
            mes = int(arg1[arg1.find("month") + 6:])
            calendar = cl.formatmonth(int(current_year),mes)
            colours(calendar)
        
        elif "year" in arg1 and "month" in arg1:
            if arg1.find("year") <= arg1.find("month"):
                year = arg1[arg1.find("year") + 5:arg1.find("month") - 1]
                mes = arg1[arg1.find("month") + 6:]
            else:
                mes = arg1[arg1.find("month") + 5:arg1.find("year") - 1]
                year = arg1[arg1.find("year") + 5:]
            calendar = cl.formatmonth(int(year), int(mes))
            colours(calendar)

        elif "today" in arg1:
            day = str(int(datetime.today().strftime('%d')))
            calendar = cl.formatmonth(int(current_year), int(current_month))
            if len(day) == 1:
                if "  " + day in calendar: day = "  " + day
                else: day = " " + day + " "
            else: colours(calendar, day)

        else: print(color("\n   Bad syntax\n", "R"))

    except: print(color("\n   Bad syntax\n", "R"))

