#Code by Sergio1260

from colors import color
from dirfil_main import extra
from os.path import isdir
from other import fixcrdir
from files2 import *

def delete(arg1, directory):
    if not arg1=="": extra(2,arg1,directory)
    else: print(color("\n   Error\n","R"))

def when(arg1, directory):
    green=color("","Gnr"); blue=color("","Bnr")
    yellow=color("","Ynr"); reset=color()
    ext=extra(8,arg1,directory); print("")
    for x in ext:
        if not x.endswith(chr(92)):
            x=x+chr(92); fix=True
        else: fix=False
        file=x.replace(directory,"")
        if len(file)==0: file=fixcrdir(x)
        if fix: x=x[:len(x)-1]
        if isdir(x): fltp=" Directory "
        else: fltp=" File "
        out= ("┌─"+green+fltp+reset+blue+file+reset+"\n│")
        out+=("\n├"+yellow+" Modificated: "+reset+ext[x][0]+reset)
        out+=("\n├"+yellow+" Created:     "+reset+ext[x][1]+reset+"\n└─\n")
        print(out)

def chmod(arg1, directory):
    #chmod [user1:r],[user2:f] for file
    file=arg1[arg1.find(" for ")+5:]
    args=arg1[:arg1.find("[")]
    perms=arg1[arg1.find("["):arg1.find(" for ")]
    perms=perms.split(",")
    for x in perms:
        x=x.replace("[","").replace("]","")
        fix=x.split(":"); user=fix[0]; perm=fix[1]
        if args=="set ": extra(7,file,directory,"/E /P "+user+":N")
        for i in perm:
            if not (i=="" or i=="n"):
                extra(7,file,directory,"/E /G "+user+":"+i)

def chown(arg1, directory):
    #chmown user1 for file
    from other import isadmin
    if isadmin():
        file=arg1[arg1.find(" for ")+5:]
        user=arg1[:arg1.find(" for ")]
        extra(5,file,directory,"/setowner "+user)
    else: print(color("\n   You must be admin to do that\n","R"))

def files(arg,arg1,directory):
    if arg=="new":
        if not arg1=="": extra(1,arg1,directory)
        else: print(color("\n   Error\n","R"))
    elif arg=="no": delete(arg1, directory)
    elif arg=="when": when(arg1, directory)
    elif arg=="edit": edit_file(arg1, directory)
    elif arg=="write": write_to_file(arg1, directory)
    elif arg=="flush": extra(3,arg1,directory)
    elif arg=="chmod": chmod(arg1, directory)           
    elif arg=="chown": chown(arg1, directory)     
    elif arg=="lsacl": lsacl(arg1, directory)
