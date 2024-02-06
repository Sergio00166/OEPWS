#Code by Sergio1260

from glob import glob
from os.path import isfile
from multiprocessing import cpu_count
from multiprocessing import Pool
from functools import partial
from colors import color
from sys import setrecursionlimit
from other import fixfiles as fixfl
from time import sleep as delay
from other import fixcrdir

setrecursionlimit(10**6) # increase the recursion limit

def fixfiles(arg): return glob(arg, recursive=False)

def readwork1(fic):
    ext=""; text=color("","Ynr"); reset=color()
    for x in fic:
        ext+=text+x+reset
        if not x[len(x)-1:]=="\n":
            ext+="\n"
    return ext
         
def readwork2(fic):
    cont=1; ext="\n│\n"; text=color("","Ynr"); reset=color()
    for x in fic:
        if len(str(cont))==1: fix="├──"
        if len(str(cont))==2: fix="├─"
        if len(str(cont))==3: fix="├"
        if x[len(x)-1]=="\n": x=x[:len(x)-1]
        ext+=(fix+str(cont)+"  "+text+x+reset+"\n"); cont+=1
    return ext+"└───\n"

def readwk(x, mode, direct):
    x=fixfl(x)
    if isfile(x):
        try:
            try: fic=open(x, "r", encoding="UTF-8").readlines()
            except: fic=open(x, "r", encoding="mbcs").readlines()
            file=x.replace(direct,"")
            banner=color("File ","G")+color(file,"B")
            if not len(fic)==0:
                if mode[0]: return "\n# "+banner+"\n\n"+readwork1(fic)
                elif mode[1]: return readwork1(fic)
                else: return "\n┌── "+banner+readwork2(fic)
            else:
                if mode[1]: return ""
                else: return "\n# "+banner+color(" > ","M")+color("EMPTY FILE","R")+"\n"
        except: return "\n   "+color("Error reading ","R")+color(fixcrdir(x+chr(92)),"B")+"\n"
    else: return ""

def main(arg1, directory, args):
    arg1=arg1.lstrip().rstrip()
    arg1=arg1.replace("'from'","\n")
    if "from " in arg1:
        direct=arg1[arg1.find("from ")+5:]
        if not ":\\" in direct: direct=directory+chr(92)+direct
        if not direct[len(direct)-1]==chr(92):
            direct+=chr(92)
        arg1=arg1[:arg1.find("from ")]
    else: direct=directory
    fix=arg1.replace("\n","from").rstrip().split("::")
    for arg1 in fix:
        if not ":\\" in arg1: arg1=direct+arg1
        lista=fixfiles(arg1)
        if not len(lista)==0:
            if args[1]: print("")
            if len(lista)>1:
                pool=Pool(processes=cpu_count())
                worker=partial(readwk, mode=args, direct=directory)
                exp=pool.map_async(worker,lista)
                for x in exp.get(): print(x, end="")
                print("")
            else: print(readwk(lista[0],args, directory))
        else: print(color("\n   It doesn't exist\n","R"))

def readfile(arg,arg1,directory):
    args=[False,False,False]
    if arg=="readc": args[1]=True
    if arg=="readn": args[0]=True
    main(arg1, directory, args)
       
