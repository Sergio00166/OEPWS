#Code by Sergio1260

from subprocess import Popen as cmd
from syntax import parse_syntax
from colors import color
from os.path import isdir
#def cmd(arg): print(arg)

def copy(arg1,directory):
    try:
        print("")
        fich, dest = parse_syntax(arg1, directory, ["from","to"])
        for y in dest:
            y=y.replace(chr(92),chr(92)+chr(92))
            for x in fich:
                if x[len(x)-1:]==chr(92) or isdir(x):
                    if x[len(x)-1:]==chr(92): x=x[:len(x)-1]
                    exp='robocopy /E /NJH /NFL /MT "'+x+'" "'+y+'"'
                else: exp='xcopy /Y "'+x+'" "'+y+'"'
                cmd(exp, shell=True).communicate()
        print("")            
    except SyntaxError: print(color("   Bad Syntax\n", "R"))
    except: print(color("   Error\n", "R"))

def move(arg1,directory):
    try:
        print("")
        fich, dest = parse_syntax(arg1, directory, ["from","to"])
        if len(dest)>1: raise ValueError
        dest=dest[0]
        for x in fich:
            if x[len(x)-1:]==chr(92) or isdir(x):
                if x[len(x)-1:]==chr(92): x=x[:len(x)-1]
                exp='robocopy /E /MOVE /NJH /NFL /MT "'+x+'" "'+dest+'"'
            else: exp='move /Y "'+x+'" "'+dest+'"'
            cmd(exp, shell=True).communicate()
        print("")           
    except SyntaxError: print(color("   Bad Syntax\n", "R"))
    except ValueError: print(color("   Too many destinations\n", "R"))
    except: print(color("   Error\n", "R"))

def rmov(arg1,directory):
    try:
        print("")
        fich, dest = parse_syntax(arg1, directory, ["from","to"])
        for x in range(0,len(fich)):
            exp='move "'+fich[x]+'" "'+dest[x]+'"'
            exp=str(exp).replace(chr(92)+chr(92),chr(92))
            cmd(exp, shell=True).communicate()
        print("")
    except SyntaxError: print(color("   Bad Syntax\n", "R"))
    except: print(color("   Error\n", "R"))


def cmr(arg,arg1,directory):
    if arg=="copy": copy(arg1,directory)
    elif arg=="move": move(arg1,directory)
    elif arg=="rmov": rmov(arg1,directory)

    
