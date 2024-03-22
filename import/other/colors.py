#Styles.css in pyhton :)

def color(arg="",color=""):
    from sys import path
    path.append('import/')
    from colorama import init, Fore, Back, Style
    init(autoreset = False)
    if color=="B": return Fore.BLUE + Style.BRIGHT + arg + Style.RESET_ALL
    elif color=="Bnr": return Fore.BLUE + Style.BRIGHT + arg
    elif color=="G": return Fore.GREEN + Style.BRIGHT + arg + Style.RESET_ALL
    elif color=="Gnr": return Fore.GREEN + Style.BRIGHT + arg
    elif color=="G-": return Fore.GREEN + Style.DIM + arg + Style.RESET_ALL
    elif color=="R": return Fore.RED + Style.BRIGHT + arg + Style.RESET_ALL
    elif color=="Rnr": return Fore.RED + Style.BRIGHT + arg
    elif color=="W": return Fore.WHITE + Style.BRIGHT + arg + Style.RESET_ALL
    elif color=="Ynr": return Fore.YELLOW + Style.BRIGHT + arg
    elif color=="Y": return Fore.YELLOW + Style.BRIGHT + arg + Style.RESET_ALL
    elif color=="Y-": return Fore.YELLOW + Style.DIM + arg + Style.RESET_ALL
    elif color=="M": return Fore.MAGENTA + Style.NORMAL + arg + Style.RESET_ALL
    elif color=="Mnr": return Fore.MAGENTA + Style.NORMAL + arg
    elif color=="C": return Fore.CYAN + Style.NORMAL + arg + Style.RESET_ALL
    elif color=="B-": return Fore.BLUE + Style.NORMAL + arg
    elif color=="bW": return Back.CYAN + Style.BRIGHT + arg + Style.RESET_ALL
    elif color=="bWnr": return Back.CYAN + Style.BRIGHT + arg
    elif color=="By": return Fore.BLUE + Style.BRIGHT + arg + Fore.YELLOW + Style.BRIGHT + Style.RESET_ALL
    elif color=="W": return Fore.CYAN + Style.BRIGHT + arg + Style.RESET_ALL
    elif color=="nrY": return Fore.YELLOW + Style.BRIGHT + arg
    else: return Style.RESET_ALL
