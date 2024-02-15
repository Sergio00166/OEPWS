#Code by Sergio1260

from colors import color
from subprocess import check_output as cmd
from glob import glob
from syntax import parse_syntax

def mklnk(dirname,name,refer,rpth):
    cmd("powershell $WshShell=New-Object -comObject WScript.Shell;"+
        "$Shortcut=$WshShell.CreateShortcut('"+dirname+chr(92)+name+".lnk')"
        ";$Shortcut.TargetPath='"+refer+"';$Shortcut.WorkingDirectory='"
        +rpth+"';$Shortcut.Save()", shell=True)

def create_link(arg, arg1, directory):
    try:
        if arg=="links": symb = True
        else: symb = False
        arg1=arg1.split('" to "')
        refer=parse_syntax(arg1[0]+'"',directory,["in",None])
        refer=glob(refer[0],recursive=False)
        
        file=parse_syntax('"'+arg1[1],directory,["in",None])[0]
        name=file.split(chr(92))[-1]
        dirname=chr(92).join(file.split(chr(92))[:-1])
        dirname=glob(dirname,recursive=False)
        
        if not (len(refer)==0 or len(dirname)==0):
            refer = refer[0]; dirname = dirname[0]
            rpth=chr(92).join(refer.split(chr(92))[:-1])
            if symb:
                cmd("powershell New-Item -ItemType SymbolicLink -Path '"+
                    dirname+"' -Name '"+name+"' -Value '"+refer+"'", shell=True)
            else: mklnk(dirname, name, refer, rpth)
        else: print(color("\n   The file/dir doesn't exist\n", "R"))
        
    except SyntaxError: print(color("\n   Bad syntax\n", "R"))
    #except: print(color("\n   Error\n", "R"))
