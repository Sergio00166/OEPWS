 #Code by Sergio1260

from os import system as cmd
from os import environ, getcwd
from sys import setrecursionlimit, path, argv
from subprocess import check_output

version="alfa v0.1.68.4"

def clsmenu(): cmd("cls"); print(menu,end="\n\n")

def var(arg1):
    direct=directory[:len(directory)-1]
    arg1=arg1.replace("'$dir'","\f").replace("$dir",direct)
    arg1=arg1.replace("\f","$dir").replace("'$ver'","\f")
    arg1=arg1.replace("$ver",version).replace("\f","$ver")
    for key, value in environ.items():
        if not key=="PATH":
            arg1=arg1.replace(("'$"+key.lower()+"'"), "\f")
            arg1=arg1.replace(("$"+key.lower()), value)
            arg1=arg1.replace("\f", ("$"+key.lower()))
    return arg1

def cli(args):
    global directory
    try:
        if not len(oldir)==1:
            if not directory==oldir[1]: oldir.append(directory)
        else: oldir.append(directory)
        if not args:
            print(fix+directory+flechas, end="")
            try: a=str(input())
            except: a=""
        else: a=args+" "
        a=forvar(a, directory)
        inp=a.replace("';'","\f").split(";")
        for a in inp:
            a=var(a+" ").replace("\f",";").replace("';'", ";")
            a=a.lstrip().rstrip()
            if " " in a:
                arg=a[:a.find(" ")]
                arg1=a[a.find(" ")+1:].lstrip().rstrip()
            else: arg=a; arg1=""
            if arg=="exit": 
                database("mp3","-quit","","")
                exit()
            elif arg=="clear": clsmenu()
            else:
                if not arg=="":
                    if arg=="sudo": arg1=arg1.replace(";","';'")
                    try: directory=database(arg,arg1,directory,str(oldir[0]))
                    except KeyboardInterrupt: pass
                    except: print(ferror)
                    if arg=="flmgr": clsmenu()
                    if not len(oldir)==1:
                        if not directory==oldir[1]: oldir.pop(0)
        if args: input("Press any key to exit . . . ")
    except KeyboardInterrupt: pass
    
def main(args):
    global directory
    if args=="#-FIXSUDIRECT-#":
        directory=userdir.replace("\\\\","\\"); args=""
    if not len(args)==0:
        if args[:1]==";":
            clsmenu()
            directory=args[1:]
            while True: cli(False)
        else: cli(args)
    else:
        while True: cli(False)
