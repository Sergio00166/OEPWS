#Code by Sergio1260

from subprocess import check_output
from sys import path
from colors import color

def fixcrdir(fix):
    fix=fix.split("\\")
    return fix[len(fix)-2]

def readable(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"

def createuserexec():
    from link import mklnk
    fic=open(path[0]+"\\import\\fixcmd\\start.cmd","w")
    fic.write("@echo off\ntitle OEPWS shell\nshift\nstart /B /WAIT "+path[0]+"\\Shell.py %*%")
    dirt=path[0]+"\\import\\fixcmd"; mklnk(dirt,"admin",dirt+"\\start.cmd",dirt)
    mkadlnk(dirt+"\\admin.lnk")

def mkadlnk(arg):
    with open(arg, 'rb') as file:
        bytes_data = bytearray(file.read())
    bytes_data[0x15] = bytes_data[0x15] | 0x20
    with open(arg, 'wb') as file:
        file.write(bytes_data)

def fixaddr(arg, silent=False):
    from glob import glob
    from os.path import isfile
    fix=glob(arg, recursive=False)
    if not len(fix)==0 and not len(fix)>1:
        fix=fix[0]
        if not isfile(fix):
            try:
                ext=str(check_output('cd /D "'+fix+'" 2>nul && cd', shell=True), encoding="cp857")
                ext=ext[:len(ext)-2]
                if not ext[len(ext)-1]==chr(92): ext+=chr(92)
                return ext
            except:
                if not silent: print(color("\n   Permision Denied\n","R")); return None
        else:
            if not silent: print(color("\n   It isn't a valid directory\n","R")); return None
    else:
        if len(fix)>1 and not silent: print(color("\n   Too many arguments\n","R")); return None
        elif not silent: print(color("\n   The dir doesn't exist\n","R")); return None

def fixfiles(arg):
    arg=arg.split(chr(92))
    file=arg.pop(); buff=""
    for x in arg: buff+=x+chr(92)
    arg=fixaddr(buff)
    if not arg==None:
        return arg+file
    else: return ""

def adminname():
    raw=Popen('net localgroup', shell=True, stdout=PIPE)
    ext=str(raw.communicate()[0], encoding="cp857")
    ext=ext[ext.find("-\\r\\n*")+6:]; ext=ext[:ext.find("\\r\\n")]
    return ext.lower()

def lsusr():
    from subprocess import Popen, PIPE
    raw=Popen('net user', shell=True, stdout=PIPE)
    raw=str(raw.communicate()[0], encoding="cp857")
    raw=raw[raw.find("----\r")+6:]; fix=[]; raw=raw.split("\n")
    raw.pop(); raw.pop(); raw.pop(); fix=[]
    for x in raw:
        x=x.split("         ")
        for i in x:
            i=i.rstrip().lstrip()
            if not i=="": fix.append(i)
    return fix

def lsgrp():
    from subprocess import Popen, PIPE
    raw=Popen('net localgroup', shell=True, stdout=PIPE)
    raw=str(raw.communicate()[0], encoding="cp857")
    raw=raw[raw.find("----\r")+6:]; fix=[]; raw=raw.split("\n")
    raw.pop(); raw.pop(); raw.pop(); raw.pop(0)
    for x in raw: fix.append(x[1:].replace("\n",""))
    return fix

def extusr(arg):
    for x in lsusr():
        if x==arg: return True
    return False

def extgrp(arg):
    for x in lsgrp():
        if x==arg:
            return True
    return False

def isadmin():
    try:
        open("C:\\tmp","w")
        try: cmd("DEL /F C:\\tmp 2>nul >nul")
        except: pass
        return True
    except: return False
    
