#Code by Sergio1260

from os import system as cmd
from subprocess import check_output
from colors import color
from glob import glob

lstext = []

def create_file(file):
    from os.path import exists
    if not exists(file):
        if file.endswith(chr(92)):
            cmd('mkdir "' + file[:len(file)-1] + '" 2>nul')
        else: open(file, "w")
    else: print("\n  " + color(file, "G") + color(" already exists\n", "R"))

def delete_file(file):
    from os.path import isfile
    file = glob(file, recursive=False)
    for x in file:
        if isfile(x): cmd('DEL /f /q "' + x + '" >nul 2>nul')
        else: cmd('RD /s /q "' + x + '" >nul 2>nul')

def fix_files(exp):
    from other import fixfiles
    file = fixfiles(exp[1:len(exp)-1])
    if not len(file) == 0:
        fix = glob(file, recursive=False)
        if not len(fix) == 0:
            for x in fix:
                open(x, "w")
        else: print(color("\n   It doesn't exist\n", "R"))
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

def work(exp, mode, extra="", extra2=""):
    global lstext
    if mode == 1:
        file = exp[1:len(exp)-1]
        if "*" in file or "?" in file:
            print(color("\n   Error\n", "R"))
        else: create_file(exp[1:len(exp)-1])
    elif mode == 2: file = exp[1:len(exp)-1]; delete_file(file)
    elif mode == 3: fix_files(exp[1:len(exp)-1])
    elif mode == 4: write_to_file(exp[1:len(exp)-1], extra, extra2)
    elif mode == 5: change_permissions(exp, extra)
    elif mode == 6: list_permissions(exp)
    elif mode == 7: change_permissions_alt(exp, extra)

def extra(mode, arg1, directory, extra="", extra2=""):
    global lstext
    from sys import path
    extpth = path[0] + "\\import\\extras" + chr(92)
    arg1=arg1.replace("'in'","\n")
    if "in " in arg1:
        fro = arg1.find("in ")
        dire = arg1[:fro].replace("\n","in")
        dire=dire.split("::")
        lstext = []
        if not chr(92) in arg1[fro+3:] and len(arg1[fro+3:]) == 2 or not arg1[:-1] == chr(92):
            direct = arg1[fro+4:] + chr(92)
        else: direct = arg1[fro+4:]
        if not ":" in direct:
            direct = directory + direct
        try:
            for x in dire:
                exp = '"' + direct + x + '"'
                exp = str(exp).replace(chr(92)+chr(92), chr(92))
                work(exp, mode)
            if mode == 6:
                return lstext
        except PermissionError: print(color("\n   Permission denied\n", "R"))
        except: print(color("\n   Error\n", "R"))
    else:
        arg1=arg1.replace("\n","in")
        dires = arg1.split("::")
        lstext = []
        try:
            for x in dires:
                if ":" + chr(92) in x:
                    exp = '"' + x + '"'
                else:
                    exp = '"' + directory + x + '"'
                exp = str(exp).replace(chr(92)+chr(92), chr(92))
                work(exp, mode, extra, extra2)
            if mode == 6: return lstext
        except PermissionError: print(color("\n   Permission denied\n", "R"))
        except: print(color("\n   Error\n", "R"))
