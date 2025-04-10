#Code by Sergio00166


def things(arg, arg1, directory):
    status=True
    
    if arg=="ls":
        from list_tree import ls
        ls(arg1, directory)

    elif arg=="sys":
        from sysinfo import sysinfo
        sysinfo()
        
    elif arg=="www":
        from os import system as cmd
        from sys import path
        cmd(path[0]+"\\import\\extras\\elinks\\elinks.exe "+arg1)
        cmd("title OEPWS shell"); print("\r\033c")

    elif arg=="sztree":
        from os import system as cmd
        from sys import path
        if arg1.strip()=="": arg1=directory
        cmd(path[0]+"\\import\\extras\\gdu.exe "+arg1)
        cmd("title OEPWS shell"); print("\r\033c")        
        
    elif "sort(" in arg:
        from sort import sort
        sort(arg,arg1,directory)
        
    elif arg=="sl":
        from colors import color
        print("\n"+color("   You write it wrong","R")+"\n")
        
    elif "read" in arg:
        from readfile import readfile
        readfile(arg,arg1,directory)
        
    elif arg=="#":
        from os import system as cmd
        dirt=directory[:len(directory)-1]
        if arg1=="": arg1="powershell"
        cmd('powershell cd "'+dirt+'"; '+arg1)
        
    elif arg=="tree":
        from list_tree import tree
        tree(arg1, directory)
        
    elif arg=="stress" or arg=="benchmk":
        from sys import path
        from os import system as cmd
        exe="import\\extras\\pyCPUBench.py"
        exe="START /B /WAIT "+path[0]+"\\"+exe
        if arg=="stress": exe+=" stress"
        cmd(exe)
        
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
        
    elif arg in ["copy","move","rmov"]:
        from cmr import cmr
        cmr(arg,arg1,directory)
        
    elif arg=="printf": print(arg1)
    
    elif arg=="depend":
        from os import system as cmd
        from sys import path
        cmd("powershell Set-ExecutionPolicy -Scope CurrentUser"+
            "-ExecutionPolicy Bypass -Force; "+path[0]+
            '\\import\\powershell\\depend.ps1')
         
    elif arg=="edit":
        from sys import path
        from syntax import parse_syntax
        from colors import color
        from os import system as cmd
        nano=path[0]+"\\import\\extras\\pBTE\\pBTE.py "
        files=parse_syntax(arg1,directory,["from",None])
        fix=files[0].replace("\\\\","\\")
        if len(files)==1 and fix==directory:
            files = [directory+'NewFile']
        try: cmd("START /B /WAIT python "+nano+'"'+'" "'.join(files)+'"')
        except: print(color("\n   Error\n","R"))
        
    else: status=False
    
    return status
