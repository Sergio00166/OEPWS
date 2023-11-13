#Code by Sergio1260

from os import system as cmd
from colors import color
from subprocess import check_output

def sys_repair(arg1):
    from other import isadmin
    if isadmin():
        if arg1=="-sys" or arg1=="":
            cmd("START /B /WAIT sfc /scannow")
            cmd("START /B /WAIT DISM /Online /Cleanup-Image /RestoreHealth")
            print("")
        elif "-dsk " in arg1: cmd("CHKDSK "+arg1[arg1.find("-dsk")+5:]+" /f /r /x")
    else: print(color("\n   This feature requires admin mode\n","R"))

def list_volumes():
    raw=str(check_output("fsutil fsinfo drives", shell=False))
    raw=raw[raw.find(": ")+2:raw.find("\\r\\n'")]
    raw=raw.replace(chr(92)+chr(92),chr(92))
    print(color("\n  Volumes: ","G") + color(raw,"B")+"\n")

def kill_proc(arg1):
    if "." in arg1: cmd("TASKKILL /F /IM "+arg1+" >nul 2>nul")
    else: cmd("TASKKILL /F /IM "+arg1+".exe"+" >nul 2>nul")

def print_text(arg1):
    arg1=arg1.replace("\\\\n","\fn").replace("\\\\f","\ff")
    arg1=arg1.replace("\\f","\n").replace("\\\\t","\ft")
    arg1=arg1.replace("\\\\b","\fb").replace("\\\\r","\fr")
    arg1=arg1.replace("\\n","\n").replace("\\t","\t")
    arg1=arg1.replace("\\b","\b").replace("\\r","\r")
    arg1=arg1.replace("\fn","\\n").replace("\ft","\\t")
    arg1=arg1.replace("\fb","\\b").replace("\ff","\\f")
    arg1=arg1.replace("\fr","\\r").replace("\\\\","\\")
    for x in arg1.split("\n"): print(x)

def speedtest():
    from sys import path
    cmd("START /B /WAIT " + path[0] +
        "\\import\\extras\\speedtest.exe")
    print("")
        
def pwdgen(arg1):
    from random import randint as rand
    try:
        a=""
        for x in range(0,int(arg1)):
            a += chr(rand(32,126))
        print(color("\n  Genarated Password:","G"), a, "\n")
    except: print(color("\n   Error\n","R"))

def weather(arg1):
    if not arg1=="": print("");cmd("curl -s wttr.in/"+arg1);print("")
    else: print(color("\n  You must provide a city name\n","R"))

def memusage():
    from psutil import virtual_memory
    from other import readable
    ram=virtual_memory()
    p_free=str(readable(ram.free))
    p_total=str(readable(ram.total))
    p_used=str(readable(ram.used))
    print(color("\n   Total: ","G")+color(str(p_total),"B"),end="")
    print(color("  Used: ","G")+color(str(p_used),"B"),end="")
    print(color("  Free: ","G")+color(str(p_free),"B"), end="\n\n")

def extras(arg,arg1,directory):
    if arg=="repair": sys_repair(arg1)
    elif arg=="volumes": list_volumes()
    elif arg=="time":
        import time
        print(color("\n  The time is: ","Y-")
              +color(time.strftime('%H:%M:%S',
              time.localtime()),"B")+"\n")
    elif arg=="kill": kill_proc(arg1)
    elif arg=="flushdns": cmd("ipconfig /flushdns > nul")
    elif arg=="shutdown": cmd("shutdown /s /t 0")
    elif arg=="restart": cmd("shutdown /r /t 0")   
    elif arg=="print": print_text(arg1)
    elif arg=="speedtest": speedtest()
    elif arg=="pwdgen": pwdgen(arg1)
    elif arg=="weather": weather(arg1)
    elif arg=="mem": memusage()
