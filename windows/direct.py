#Code by Sergio1260

from colors import color
from subprocess import check_output
from other import fixaddr

def fmgr(directory):
    from subprocess import Popen, PIPE
    from sys import path
    ext = path[0]+"\\import\\extras\\lf.exe -print-last-dir "+directory
    proces = Popen(ext, shell=True, stdout=PIPE)
    dirt = proces.communicate()[0].decode("utf-8").splitlines()
    return dirt[len(dirt)-1]

def eject_dsk(arg1, directory):
    from os import system as cmd
    drive = fix= None
    if arg1[1:] == ":\\": drive = arg1[:len(arg1) - 1]
    elif arg1[1:] == ":": drive = arg1
    elif len(arg1) == 1: drive = arg1 + ":"
    raw = str(check_output("fsutil fsinfo drives", shell=False))
    raw = raw[raw.find(": ") + 2:raw.find("\\r\\n'")]
    raw = raw.replace("\\\\", "")
    raw = raw.split(" ")
    if not drive == None:
        for x in raw:
            if x == drive:
                fix = x
        if not fix == None:
            try:
                cmd("powershell powershell (new-object -COM Shell.Application).NameSpace(17)"
                    +".ParseName('"+fix+"').InvokeVerb('Eject') exit")
                if directory.split(chr(92))[0] == fix:
                    raw = str(check_output("echo %userprofile%", shell=True), encoding="cp857")
                    directory = raw[:len(raw)-2]
            except: print(color("\n   Error while ejecting ", "R") + color(fix, "M") + "\n")
        else: print("\n   " + color("The drive ", "R") + color(drive, "M") + color(" doesn't exist", "R") + "\n")
    else: print(color("\n   Bad syntax\n", "R"))
    return directory

def goto_dir(arg1, directory, oldir):
    from sys import path

    try:
        if arg1 in ["home","dl","doc","desk"]:
            home = str(check_output("echo %USERPROFILE%", shell=True))
            home = home[2:len(home) - 5].replace(chr(92) + chr(92), chr(92))
            if arg1 == "dl": directory = home + "\\Downloads" + chr(92)
            elif arg1 == "doc": directory = home + "\\Documents" + chr(92)
            elif arg1 == "desk": directory = home + "\\Desktop" + chr(92)
            elif arg1 == "home": directory = home
        elif arg1 == "prev": directory = oldir
        elif arg1.split(" ")[0] == "back":
            tloop = arg1.split(" ")
            if not len(tloop) == 1: times = int(tloop[1].replace(" ", ""))
            else: times = 1
            for x in range(0, times): directory += ".." + chr(92)
        elif arg1.split(" ")[0] == "down":
            fix = arg1[arg1.find("down ") + 5:]
            args = arg1.split(chr(92)); top = ""
            sep = directory.split(chr(92))
            for x in sep:
                if x == fix or fix in x:
                    top = sep.index(x)
            if not top == "":
                directory = ""
                for x in range(0, top + 1):
                    directory = directory + sep[x] + chr(92)
            else: print(color("\n   Error\n", "R"))   
        elif arg1 == "-": directory = directory[:directory.find(":") + 1] + chr(92)
        elif ":\\" in arg1: directory = arg1
        elif arg1 == ".\\": directory = path[0]
        else: print(color("\n   Bad Syntax\n", "R"))
        return directory
    except: print(color("\n   Error\n", "R"))


def direct(arg,arg1,directory,oldir):
    prevdir=[]; olddir=directory
    if arg=="cd": directory+=arg1+chr(92)
    elif arg=="go": directory=goto_dir(arg1, directory, oldir)
    elif arg=="eject": directory=eject_dsk(arg1, directory)
    elif arg=="flmgr": directory=fmgr(directory)
    fix=fixaddr(directory)
    if not fix==None: return fix
    else: return olddir
    
