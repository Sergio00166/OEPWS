#Code by Sergio1260

from subprocess import check_output as cmd
from sys import path
from colors import color
from other import fixaddr, fixfiles
from os.path import isdir
from glob import glob
#def cmd(arg, shell): print(arg)

def main(arg1,directory):
    try:
        arg1=arg1.replace("'from'","\n")
        arg1=arg1.replace("'to'","\f")
        to=arg1.find(" to ")
        if " from " in arg1:
            fro=arg1.find(" from ")
            fich=arg1[:fro].split("::")
            dest=arg1[to+4:].split("::")
            direct=arg1[fro+6:to]
            if not ":\\" in direct: direct=directory+direct
            if not chr(92) in direct[len(direct)-1:]: direct+=chr(92)
            for y in dest:
                y=y.replace("\n","from").replace("\f","to")
                if not ":\\" in y: y=directory+y
                y=fixfiles(y)
                for x in fich:
                    fix=fixfiles(direct)
                    x=x.replace("\n","from").replace("\f","to")
                    if not ":\\" in x: x=fix+x
                    else: x=x
                    if len(glob(x, recursive=False))>0:
                        if not len(fix)==0:
                            if x[len(x)-1:]==chr(92) or isdir(x):
                                if x[len(x)-1:]==chr(92): x=x[:len(x)-1]
                                exp='robocopy /E "'+x+'" "'+y+'"'
                            else: exp='xcopy "'+x+'" "'+y+'"'   
                            try: cmd(exp)
                            except: pass
                    else: print("\n   "+color("The target ","R")+color(x,"B")+color(" do not exist","R")+"\n")
        else:
            fich=arg1[:to].split("::")
            dest=arg1[to+4:].split("::")
            for y in dest:
                y=y.replace("\n","from").replace("\f","to")
                if not ":\\" in y: y=directory+y
                fix=fixfiles(y)
                if "*" in fix or "?" in fix:
                    y=fixaddr(y)
                for x in fich:
                    x=x.replace("\n","from").replace("\f","to")
                    if not ":\\" in x: x=directory+x
                    else: x=x
                    if len(glob(x, recursive=False))>0:
                        if x[len(x)-1:]==chr(92) or isdir(x):
                            if x[len(x)-1:]==chr(92): x=x[:len(x)-1]
                            exp='robocopy /E "'+x+'" "'+y+'"'
                        else: exp='xcopy "'+x+'" "'+y+'"'
                        try: cmd(exp)
                        except: pass
                    else: print("\n   "+color("The target ","R")+color(x,"B")+color(" do not exist","R")+"\n")

    except: print(color("\n   Error\n", "R"))
