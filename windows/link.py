#Code by Sergio1260

from subprocess import check_output
from colors import color
from os import system as cmd

def mklnk(dirname,name,refer,rpth):
    cmd("powershell $WshShell=New-Object -comObject WScript.Shell;"+
        "$Shortcut=$WshShell.CreateShortcut('"+dirname+chr(92)+name+".lnk')"
        ";$Shortcut.TargetPath='"+refer+"';$Shortcut.WorkingDirectory='"
        +rpth+"';$Shortcut.Save()")

def create_link(arg, arg1, directory):
    try:
        if arg1=="links":symb = True
        else: symb = False
        if " to " in arg1:
            refer = arg1[arg1.find(" to ") + 4:]
            if " in " in refer:
                exe = refer[:refer.find(" in ")]
                dip = refer[refer.find(" in ") + 4:]
                if dip[len(dip) - 1:len(dip)] == chr(92):
                    dip = dip[:len(dip) - 1]
                refer = dip + chr(92) + exe
            else:
                if not ":" in refer:
                    refer = directory + refer
            if " in " in arg1:
                dirname = arg1[arg1.find(" in ") + 3:arg1.find(" to ")]
                dirname = str(dirname).replace(chr(92) + chr(92), chr(92))
                name = arg1[:arg1.find(" in ")]
            else:
                drt = arg1[:arg1.find(" to ")]
                if chr(92) in drt:
                    dirt = drt.split(chr(92))
                    direct = ""
                    name = dirt[len(dirt) - 1]
                    dirt.pop()
                    for x in dirt:
                        direct += x + chr(92)
                    if ":" in drt: dirname = direct
                    else: dirname = directory + direct
                else: dirname = directory; name = drt
            if not ":" + chr(92): refer = directory + refer
            refer = str(refer).replace(chr(92) + chr(92), chr(92))
            fix = refer.split(chr(92))
            fix.pop()
            rpth = ""
            for x in fix: rpth += x + chr(92)
            if symb:
                check_output("powershell New-Item -ItemType SymbolicLink -Path '" +
                             dirname + "' -Name '" + name + "' -Value '" + refer + "'", shell=False)
            else: mklnk(dirname, name, refer, rpth)
        else: print(color("\n   Bad syntax\n", "R"))
    except: print(color("\n   Error\n", "R"))
