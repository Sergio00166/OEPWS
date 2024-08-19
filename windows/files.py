#Code by Sergio00166

from colors import color
from os.path import isdir, isfile
from other import fixcrdir
from syntax import parse_syntax
from os import system as cmd
from glob import glob

from files1 import *
from files2 import *


def delete(arg1, directory):
    if not arg1=="":
        try:
            file = parse_syntax(arg1,directory,["from",None]); files=[]
            if not len(file)==0:
                for x in file: files.extend(glob(x, recursive=False, include_hidden=True))
                for x in files: 
                    if isfile(x): cmd('DEL /Q /F "'+x+'" >nul 2>nul')
                    else: cmd('RD /s /q "'+x+'" >nul 2>nul')
        except SyntaxError: print(color("\n   Syntax Error\n","R"))
    else: print(color("\n   Error\n","R"))


def flush(arg1,directory):
    from glob import glob
    try:
        arg=parse_syntax(arg1,directory,["in",None])
        for x in arg:
            file = glob(x, recursive=False)
            if not len(file) == 0:
                for x in file: open(x, "w")
            else: print(color("\n   It doesn't exist\n", "R"))
            
    except SyntaxError: print(color("\n   Syntax Error\n","R"))
    except: print(color("\n   Error\n","R"))

  
def newfile(arg1,directory):
    from os.path import exists
    
    try:
        file=parse_syntax(arg1,directory,["in",None])
        for x in file:
            if not exists(x):
                if x.endswith(chr(92)):
                    try: cmd('mkdir "'+x[:-1]+'" 2>nul >nul')
                    except: raise PermissionError
                else: fic=open(x, "w"); fic.close()
            else: print("\n  "+color(file,"G")+color(" already exists\n","R"))
            
    except SyntaxError: print(color("\n   Syntax Error\n","R"))
    except PermissionError: print(color("\n   Permission denied\n", "R"))
    except: print(color("\n   Error\n","R"))


def files(arg,arg1,directory):
    if arg=="new":
        if not arg1=="": newfile(arg1,directory)
        else: print(color("\n   Error\n","R"))
    elif arg=="no": delete(arg1, directory)
    elif arg=="when": when(arg1, directory)
    elif arg=="write": write_to_file(arg1, directory)
    elif arg=="flush": flush(arg1,directory)
    elif arg=="chmod": chmod(arg1, directory)           
    elif arg=="chown": chown(arg1, directory)     
    elif arg=="lsacl": lsacl(arg1, directory)
