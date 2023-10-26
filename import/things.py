#Code by Sergio1260

def things(arg, arg1, directory):
    status=True
    if arg=="ls":
        from list_tree import ls
        ls(arg1, directory)
    elif arg=="sys":
        from sysinfo import sysinfo
        sysinfo()
    elif "sort(" in arg:
        from sort import sort
        sort(arg,arg1,directory)
    elif arg=="sl":
        from colors import color
        print("\n"+color("   You write it wrong","R")+"\n")
    elif "read" in arg:
        from readfile import readfile
        readfile(arg,arg1,directory)
    elif arg=="natives":
        from os import system as cmd
        cmd("powershell "+arg1)
    elif arg=="tree":
        from list_tree import tree
        tree(arg1, directory)
    elif arg=="benchmk":
        from benchmk import main
        main()
    elif arg=="calc":
        from clicalc import main as clicalc
        from os import system as cmd
        from sys import path
        if not arg1=="": clicalc(arg1)
        else: cmd("START /B /WAIT "+path[0]+"\\windows\\clicalc.py")
    elif arg=="locate" or arg=="locatenr":
        from locate import main
        main(arg,arg1,directory)
    elif arg=="from":
        from find import main
        main(arg1,directory)
    elif arg=="perfmon":
        from sys import path
        from os import system as cmd
        from other import isadmin
        from colors import color
        if isadmin():
            exe="import\\extras\\btop4win\\btop4win.exe"
            cmd("START /B /WAIT "+path[0]+"\\"+exe)
            cmd("title OEPWS shell")
        else: print("\n"+color("   This feature requires admin mode","R")+"\n")
    elif arg=="stress":
        from stress import main
        main()
    elif arg=="cal":
        from cal import calendar
        calendar(arg1)
    elif arg=="dskperf":
        from dskperf import main
        main(arg1,directory)
    elif arg=="ip":
        from ip_info import main as ipinfo
        ipinfo()
    elif arg=="link" or arg=="links":
        from link import create_link
        create_link(arg, arg1, directory)
    elif arg=="size":
        from sizes import size
        size(arg1,directory) 
    elif arg=="dskinfo":
        from sizes import dskinfo
        dskinfo(arg1, directory)
    elif arg=="copy":
        from copyp import main
        main(arg1,directory)
    elif arg=="move":
        from move import main
        main(arg1,directory)
    elif arg=="rename":
        from rename import main
        main(arg1,directory)
    elif arg=="depend":
        from os import system as cmd
        from sys import path
        cmd("powershell Set-ExecutionPolicy -Scope CurrentUser"+
            "-ExecutionPolicy Bypass -Force; "+path[0]+
            '\\import\\powershell\\depend.ps1')
    else: status=False
    
    return status
