#Code by Sergio00166

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
from syntax import parse_syntax

setrecursionlimit(10**6) # increase the recursion limit

green=color(color="Gnr")
blue=color(color="Bnr")
yellow=color(color="Ynr")
red=color(color="Rnr")
magenta=color(color="Mnr")
reset=color()

def fixfiles(arg): return glob(arg, recursive=False)

def readwork1(fic):
    ext=""; text=color("","Ynr")
    for x in fic:
        ext+=text+x+reset
        if not x[len(x)-1:]=="\n":
            ext+="\n"
    return ext
         
def readwork2(fic):
    cont=1; ext="\n│\n"; text=color("","Ynr")
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
            banner=green+"File "+reset+blue+file+reset
            if not len(fic)==0:
                if mode[0]: return "\n# "+banner+"\n\n"+readwork1(fic)
                elif mode[1]: return readwork1(fic)
                elif mode[2]:
                    outb="\n┌─ "+banner+"\n└─ "+yellow+"lines: "+reset
                    return outb+blue+str(len(fic))+reset+"\n"
                else: return "\n┌── "+banner+readwork2(fic)
            else:
                if mode[1]: return ""
                else: return "\n# "+banner+magenta+" > "+reset+red+"EMPTY FILE"+reset+"\n"
        except: return ""
    else: return ""

def main(arg1, directory, args):
    out = parse_syntax(arg1, directory, ["from",None])
    lista = []
    for x in out: lista+=glob(x,recursive=False)
    
    if not len(lista)==0:
        if args[1]: print("")
        if len(lista)>1:
            pool=Pool(processes=cpu_count())
            worker=partial(readwk, mode=args, direct=directory)
            exp=pool.map_async(worker,lista)
            out=exp.get()
            pool.close()
            for x in out: print(x, end="")
            print("")
        else: print(readwk(lista[0],args, directory))
    else: print(color("\n   It doesn't exist\n","R"))

def readfile(arg,arg1,directory):
    args=[False,False,False]
    if arg=="readc": args[1]=True
    if arg=="readn": args[0]=True
    if arg=="readcl": args[2]=True
    main(arg1, directory, args)
       
