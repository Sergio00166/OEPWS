#Code by Sergio00166

from colors import color
from os.path import isdir
from other import fixcrdir
from syntax import parse_syntax
from os import system as cmd

def when(arg1, directory):
    from os.path import getmtime, getctime
    from datetime import datetime as dt
    from glob import glob
    
    green=color("","Gnr"); blue=color("","Bnr")
    yellow=color("","Ynr"); reset=color(); mctime={}
    
    try:
        arg = parse_syntax(arg1,directory,["in",None])
        for y in arg:
            files=glob(y, recursive=False)
            for x in files:
                try: mod=dt.fromtimestamp(getmtime(x)).strftime("%d-%m-%Y %H:%M:%S")
                except: mod=color("Cannot get mtime","R")
                try: crea=dt.fromtimestamp(getctime(x)).strftime("%d-%m-%Y %H:%M:%S")
                except: crea=color("Cannot get ctime","R")
                mctime[x]=[mod,crea]       
        print("")
        for x in mctime:
            file=fixcrdir(x).replace(directory,"")
            if len(file)==0: file=fixcrdir(x)
            if isdir(x): fltp=" Directory "
            else: fltp=" File "
            out= ("┌─"+green+fltp+reset+blue+file+reset+"\n│")
            out+=("\n├"+yellow+" Modificated: "+reset+mctime[x][0]+reset)
            out+=("\n├"+yellow+" Created:     "+reset+mctime[x][1]+reset+"\n└─\n")
            print(out)
            
    except SyntaxError: print(color("\n   Syntax Error\n","R"))              
    except: print(color("\n   Error\n","R"))


def chmod(arg1, directory):
    #chmod [user1:r],[user2:f] for file
    try:
        file=arg1[arg1.find('] for "')+6:]
        args=arg1[:arg1.find("[")]
        perms=arg1[arg1.find("["):arg1.find(" for ")]
        perms=perms.split(",")
        for x in perms:
            x=x.replace("[","").replace("]","")
            fix=x.split(":"); user=fix[0]; perm=fix[1]
            file=parse_syntax(file,directory,["in",None])
            for i in perm:
                if not (i=="" or i=="n"):
                    for z in file:
                        if args=="set ":
                            cmda='"'+z+'" '+"/E /P "+user+":N"
                            cmd('CACLS '+cmda+' 2>nul')
                        cmda='"'+z+'" '+"/E /G "+user+":"+i
                        cmd('CACLS '+cmda+' 2>nul')
                        
    except SyntaxError: print(color("\n   Syntax Error\n","R"))              
    except: print(color("\n   Error\n","R"))


def chown(arg1, directory):
    #chmown user1 for file
    try:
        from other import isadmin
        if isadmin():
            file=arg1[arg1.find(" for ")+5:]
            user=arg1[:arg1.find(" for ")]
            file=parse_syntax(file,directory,["in",None])
            for x in file: cmd('ICACLS "'+x+'" /setowner '+user+" 2>nul")
        else: print(color("\n   You must be admin to do that\n","R"))
        
    except SyntaxError: print(color("\n   Syntax Error\n","R"))
    except: print(color("\n   Error\n","R"))

