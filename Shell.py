#Code by Sergio1260

from os import system as cmd
from os import environ, getcwd
from sys import setrecursionlimit, path, argv
from subprocess import check_output

version="alfa v0.1.68.2"; line=" -"

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
    if not len(oldir)==1:
        if not directory==oldir[1]: oldir.append(directory)
    else: oldir.append(directory)
    if not args:
        print(fix+directory+flechas, end="")
        try: a=str(input())
        except: a=""
    else: a=args+" "
    a=forvar(a, directory)
    inp=a.replace("';'","\f").split(";"); cont=0
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
                except: print(ferror)
                if arg=="flmgr": clsmenu()
                if not len(inp)==1 and not cont==len(inp)-1:
                    if not args==False and cont==0: cont+=1
                    else: print(line); cont+=1
                if not len(oldir)==1:
                    if not directory==oldir[1]: oldir.pop(0)
    if args: input("Press any key to exit . . . ")
    
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
        
if __name__ == "__main__":
    setrecursionlimit(10**6)
    for x in path:
        if "site-packages" in x: path.remove(x)
    for x in path:
        if "site-packages" in x: path.remove(x)
    path.append(path[0]+chr(92)+"import")
    from colors import color
    menu=str(color(" OEPWS by Sergio1260 ","G")+"\n "+
             color(version,"R")+color(" on ","G")+
             color("Windows OS","B"))
    clsmenu(); from forvar import main as forvar
    flechas=str(color(" >> ","G-"))
    ferror=color("\n  FATAL ERROR\n","R")
    raw=str(check_output("echo %userprofile%",shell=True))
    userdir=raw[2:len(raw)-4].replace(chr(92)+chr(92),chr(92))
    userdir=userdir.replace(chr(92),chr(92)+chr(92))
    path.append(path[0] + chr(92) + 'windows')
    from database import database
    user=str(check_output("whoami")); oldir=[]
    user=user[2:len(user)-5]; args=" ".join(argv[1:])
    user=user[user.find(chr(92)+chr(92))+2:]
    del raw; directory=getcwd()+chr(92)
    directory=directory.replace("\\\\","\\")
    oldir.append(directory)
    fix="\r "+str(color(user,"B"))+str(color(" ","B-"))

    main(args)
    
