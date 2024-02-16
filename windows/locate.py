#Code by Sergio1260

from glob import glob
from colors import color
from multiprocessing import cpu_count, Pool
from itertools import chain
from functools import partial
from sys import setrecursionlimit
from os.path import isdir, isabs
import re

setrecursionlimit(10**6) # increase the recursion limit

def parse_basic_syntax(code, directory, mode="in"):
    sep='" '+mode+' "'
    try:
        if sep in code:
            code=code.split(sep);args=code[0][1:]
            file=code[1][:-1].split('" "')
        else: args=code[1:-1]; file=[directory]
        args=args.split('" "')
        return args, file
    except: raise SyntaxError

def fileonly(arg):
    arg=arg.split(chr(92))
    return arg[len(arg)-1]

def worker(arg,pattern,onlydir):
    filepath = glob(arg+chr(92)+"*", recursive=False)
    if len(filepath)>0:
        out=[]
        for x in filepath:
            if pattern.search(fileonly(x)):
                if onlydir:
                    if isdir(x): out.append(x)
                else: out.append(x)
        return out
    else: return []

def lister(arg): return glob(arg+"**"+chr(92), recursive=False)

def main(arg,arg1,directory):
    try:
        print(""); 
        if arg=="locatenr": recurse=False
        else: recurse=True

        buff2,buff = parse_basic_syntax(arg1, directory, "in")
        buff = buff[0]
        if not isabs(buff): buff=directory+buff
        if not buff.endswith(chr(92)): buff+=chr(92)
        
        for x in buff2:
            if x.endswith(chr(92)):
                x=x[:len(x)-1]
                onlydir=True
            else: onlydir=False
            pattern=re.compile(x)
            if not buff==None:
                if recurse==True:
                    prew=glob(buff+"**"+chr(92), recursive=False)
                    pool=Pool(processes=cpu_count()-1); tree=[buff]
                    while not len(prew)==0:
                        tree+=prew
                        ext=pool.map_async(lister,prew)
                        prew=list(chain(*ext.get()))    
                    searcher = partial(worker, pattern=pattern,onlydir=onlydir)
                    ext=pool.map_async(searcher,tree); filepath=[]
                    filepath=ext.get()
                else:
                    filepath=glob(buff+"*", recursive=False); out=[]
                    for z in filepath:
                        if pattern.search(fileonly(z)):
                            if onlydir:
                                if isdir(z): out.append(z)
                            else: out.append(z)
                    filepath=[out]
                if recurse: filepath=[list(chain(*filepath))]
                yellow=color("","nrY"); reset=color()
                if not len(filepath[0])==0:
                    if onlydir: x+=chr(92)
                    print("┌─> "+color(x,"M")+color(" is located ","G")+"("+color("inside ","G")
                          +color(buff,"B")+")"+color(" on: ","G")+"\n│")
                    for z in filepath:
                        for i in z:
                            i=i.replace(buff,"")
                            i=i.replace("\\\\","\\").replace("\\\\","\\")
                            print("├  "+yellow+i+reset)
                        print("└─")      
                else:
                    if not recurse: ext=" in"
                    else: ext=" inside "
                    print("  "+color(x,"M")+color(" does not exist"+ext,"R")+" "+color(buff,"B"))
            print("")
    
    except: print(color("   Error\n","R"))
