#Code by Sergio1260

from os import system as cmd
from subprocess import check_output
from colors import color
from glob import glob

lstext = []
mctime = {}

def create_file(file):
    from os.path import exists
    if not exists(file):
        if file.endswith(chr(92)):
            try: check_output('mkdir "'+file[:len(file)-1]+'"')
            except: raise PermissionError
        else: open(file, "w")
    else: print("\n  " + color(file, "G") + color(" already exists\n", "R"))

def delete_file(file):
    from os.path import isfile
    file = glob(file, recursive=False)
    if not len(file)==0:
        for x in file:
            try:
                if isfile(x):
                    check_output('DEL /f /q "'+x+'"', shell=True)
                else: check_output('RD /s /q "'+x+'"', shell=True)
            except: raise PermissionError
    else: print(color("\n   File/dir not found\n","R"))

def flush_file(arg):
    file = glob(arg, recursive=False)
    if not len(file) == 0:
        for x in file: open(x, "w")
    else: print(color("\n   It doesn't exist\n", "R"))

def write_to_file(file, extra, extra2):
    file = open(file, extra2, encoding="UTF-8")
    file.write(extra)
    file.close()

def change_permissions(exp, extra):
    try: check_output('ICACLS ' + exp + ' ' + extra, shell=True)
    except: pass

def list_permissions(exp):
    try:
        files = glob(exp[1:len(exp)-1], recursive=False)
        for exp in files:
            ext=[[str(check_output('ICACLS "'+exp+'" 2>nul', shell=True),
                      encoding="cp857").replace(exp,"")]]
            ext.append(exp); lstext.append(ext)
    except: pass

def change_permissions_alt(exp, extra):
    try: check_output('CACLS ' + exp + ' ' + extra + ' 2>nul', shell=True)
    except: pass

def modcrtime(arg,directory):
    global mctime
    from os.path import getmtime, getctime
    from datetime import datetime as dt
    arg=arg[1:len(arg)-1]
    files=glob(arg, recursive=False)
    for x in files:
        try: mod=dt.fromtimestamp(getmtime(x)).strftime("%d-%m-%Y %H:%M:%S")
        except: mod="##-##-#### ##:##:##"
        try: crea=dt.fromtimestamp(getctime(x)).strftime("%d-%m-%Y %H:%M:%S")
        except: crea="##-##-#### ##:##:##"
        mctime[x]=[mod,crea]
    
def work(exp, mode, extra="", extra2=""):
    if mode == 1:
        file = exp[1:len(exp)-1]
        if "*" in file or "?" in file:
            print(color("\n   Error\n", "R"))
        else: create_file(exp[1:len(exp)-1])
    elif mode == 2: file = exp[1:len(exp)-1]; delete_file(file)
    elif mode == 3: flush_file(exp[1:len(exp)-1])
    elif mode == 4: write_to_file(exp[1:len(exp)-1], extra, extra2)
    elif mode == 5: change_permissions(exp, extra)
    elif mode == 6: list_permissions(exp)
    elif mode == 7: change_permissions_alt(exp, extra)
    elif mode == 8: modcrtime(exp, extra)

def extra(mode, arg1, directory, extra="", extra2=""):
    global lstext, mctime
    from sys import path
    extpth = path[0] + "\\import\\extras" + chr(92)
    arg1=arg1.replace("'in'","\n")
    if " in " in arg1:
        fro = arg1.find(" in ")
        dire = arg1[:fro].replace("\n","in")
        dire=dire.split("::")
        lstext = []
        if not chr(92) in arg1[fro+3:] and len(arg1[fro+3:]) == 2 or not arg1[:-1] == chr(92):
            direct = arg1[fro+4:] + chr(92)
        else: direct = arg1[fro+4:]
        if not ":" in direct: direct = '"'+directory+direct+'"'
        try:
            for x in dire:
                exp = '"'+direct+x+'"'
                exp = str(exp).replace(chr(92)+chr(92), chr(92))
                work(exp, mode)
            if mode == 6: return lstext
            elif mode == 8: return mctime
        except PermissionError: print(color("\n   Permission denied\n", "R"))
        except: print(color("\n   Error\n", "R"))
    else:
        arg1=arg1.replace("\n","in")
        dires = arg1.split("::")
        lstext = []
        try:
            for x in dires:
                if ":" + chr(92) in x: exp = '"'+x+'"'
                else: exp = '"'+directory+x+'"'
                exp = str(exp).replace(chr(92)+chr(92), chr(92))
                work(exp, mode, extra, extra2)
            if mode == 6: return lstext
            elif mode == 8: return mctime
        except PermissionError: print(color("\n   Permission denied\n", "R"))
        except: print(color("\n   Error\n", "R"))
