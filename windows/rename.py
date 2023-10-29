#Code by Sergio1260

from subprocess import check_output as cmd
from sys import path
from colors import color
from other import fixaddr, fixfiles
from os.path import isdir
#def cmd(arg, shell): print(arg)

def main(arg1,directory):
    try:
        arg1=arg1.replace("'from'","\n")
        arg1=arg1.replace("'to'","\f")
        to=arg1.find(" to ")
        if " from " in arg1:
            fro=arg1.find(" from ")
            fich=arg1[:fro-1]
            fich=fich.replace("\f","to").replace("\n","from")
            fich=fich.split("::")
            direct=arg1[fro+6:to]
            direct=fixaddr(direct, True)
            if not direct==None:
                dest=dest.replace("\f","to").replace("\n","from")
                dest=dest.split("::")
                for x in range(0,len(fich)):
                    if not ":\\" in fich[x]:
                        if chr(92) in fich[x]:
                             fix=fich[x].split(chr(92))
                             path=fix; path.pop(); buff=""
                             for i in path: buff+=i+chr(92)
                             fl=direct+chr(92)+fich[x]
                             dt=direct+chr(92)+buff+dest[x]
                             
                        else:
                            fl=direct+chr(92)+fich[x]
                            dt=direct+chr(92)+dest[x]
                    else:
                        fl=fich[x]
                        tmp=fl.split(chr(92))
                        tmp.pop(); buff=""
                        for i in tmp: buff=buff+i+chr(92)
                        buff=fixaddr(buff, True)
                    exp='move "'+fl+'" "'+dt+'"'
                    exp=str(exp).replace(chr(92)+chr(92),chr(92))
                    cmd(exp+" 2>nul", shell=True)
            else: print(color("\n   Error\n", "R"))
        else:
            fich=arg1[:to]
            fich=fich.replace("\f","to").replace("\n","from")
            fich=fich.split("::")
            dest=arg1[to+4:]
            dest=dest.replace("\f","to").replace("\n","from")
            dest=dest.split("::")
            for x in range(0,len(fich)):
                if ":"+chr(92) in fich[x]:
                    dirt=fich[x].split(chr(92));file=dirt.pop(); direct=""
                    for i in dirt: direct+=i+chr(92)
                    direct=fixaddr(direct, True)
                    if not direct==None:
                        exp='move "'+direct+file+'" "'+direct+dest[x]+'"'
                else: exp='move "'+directory+fich[x]+'" "'+directory+dest[x]+'"'
                exp=str(exp).replace(chr(92)+chr(92),chr(92))
                cmd(exp+" 2>nul", shell=True)
    except: print(color("\n   Error\n", "R"))
