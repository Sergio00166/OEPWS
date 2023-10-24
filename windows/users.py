#Code by Sergio1260

from os import system as cmd
from sys import path
from colors import color
from subprocess import check_output
from other import createuserexec, extusr, extgrp, isadmin

def switch_user(arg1, directory):
    createuserexec()
    try:
        print("")
        pth = path[0] + "\\import\\fixcmd\\start.cmd"
        print(color(" Password: ", "G"), end="")
        check_output("runas /user:"+arg1+' "'+pth+' #-FIXSUDIRECT-#"')
        print("\n")
    except: print(color("\r   Cannot log in\n", "R"))

def root(arg1,directory):
    from sys import path
    from os import system as cmd
    createuserexec()
    if not arg1=="":
        root=str(check_output("whoami"))
        ext=("start /B "+path[0]+"\\import\\extras"+
            "\\nircmdc.exe elevatecmd runassystem "
            +path[0]+"\\import\\fixcmd\\start.cmd")
        if not root=="b'nt authority\\system\r\n'":
            if arg1=="su": cmd(ext+" ;"+directory)
            else: cmd(ext+" go "+directory+"; "+arg1.replace("&",","))
        else: print(color("\n  You are root\n", "R"))

def sudo(arg1, directory):
    createuserexec()
    try:
        if isadmin(): print(color("\n  You are admin\n", "R"))
        else:
            if arg1 == "su":
                createuserexec()
                cmd(path[0] + "\\import\\fixcmd\\admin.lnk ;"+directory)
            else: cmd(path[0] + '\\import\\fixcmd\\admin.lnk go '+directory+"; "+arg1.replace("&", ";"))
    except: pass

def add_user(arg1):
    from other import adminname
    from getpass import getpass
    admin = False
    if "-sudo" in arg1:
        admin = True
        arg1 = arg1.replace("-sudo", "")
    if isadmin():
        if not extusr(arg1):
            try:
                print("")
                print(color("   Write a password: ", "G"), end="")
                pwd = getpass("")
                print(color("   Rewrite the password: ", "G"), end="")
                pwd1 = getpass("")
                while not pwd == pwd1:
                    print(color("   Rewrite the password: ", "G"), end="")
                    pwd1 = getpass("")
                print("")
                check_output("net user /add " + arg1 + " " + pwd, shell=True)
                if admin == True:
                    cmd('net localgroup ' + adminname() + " " + arg1 + ' /add')
            except: pass
        else: print(color("\n   User ", "R") + color(arg1, "B") + color(" already exists\n", "R"))
    else: print(color("\n   You must be admin to do that\n", "R"))

def delete_user(arg1):
    try:
        if isadmin():
            if extusr(arg1): cmd("NET USER " + arg1 + " /DELETE >nul")
            else: print(color("\n   User ", "R") + color(arg1, "B") + color(" doesn't exist\n", "R"))
        else: print(color("\n   You must be admin to do that\n", "R"))
    except: pass

def list_users():
    from other import lsusr
    print("\n┌─ "+color("Users on this computer:", "G")+" \n│")
    for x in lsusr():
        print("├  "+color(x, "B"))
    print("└─\n")

def list_groups():
    from other import lsgrp
    print("\n┌─ "+color("Groups on this computer:", "G")+" \n│")
    for x in lsgrp():
        print("├  "+color(x, "B"))
    print("└─\n")

def add_group(arg1):
    try:
        if isadmin():
            if not extgrp(arg1):
                cmd("net localgroup " + arg1 + " /add >nul")
            else: print(color("\n   Group ", "R") + color(arg1, "B") + color(" already exists\n", "R"))
        else: print(color("\n   You must be admin to do that\n", "R"))
    except: pass

def delete_group(arg1):
    try:
        if isadmin():
            if extgrp(arg1): cmd("net localgroup " + arg1 + " /del >nul")
            else: print(color("\n   Group ", "R") + color(arg1, "B") + color(" doesn't exist\n", "R"))
        else: print(color("\n   You must be admin to do that\n", "R"))
    except: pass

def users(arg, arg1, directory):
    if arg == "su": switch_user(arg1, directory)
    elif arg == "deluser": delete_user(arg1)
    elif arg == "lsusr": list_users()
    elif arg == "sudo": sudo(arg1, directory)
    elif arg == "root": root(arg1, directory)
    elif arg == "addgroup": add_group(arg1)
    elif arg == "delgroup": delete_group(arg1)
    elif arg == "lsgrp": list_groups()
    elif arg == "crex": createuserexec()
