#Code by Sergio1260

from glob import glob
from colors import color
from multiprocessing import cpu_count, Pool
from itertools import chain
from functools import partial
from other import fixaddr
from sys import setrecursionlimit
from os.path import isdir
import re
from other import fixcrdir

setrecursionlimit(10**6) # increase the recursion limit

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
        arg1=arg1.replace("'in'","\n")
        if "in " in arg1:
            ins=arg1.find(" in "); buff=arg1[ins+4:]
            buff2=str(arg1[:ins]).split("::")
            if not buff[len(buff)-1]==chr(92): buff+=chr(92)
        else: buff2=str(arg1).split("::")
        for x in buff2:
            if x.endswith(chr(92)):
                x=x[:len(x)-1]
                onlydir=True
            else: onlydir=False
            pattern=re.compile(x)
            if "in " in arg1:
                if not ":"+chr(92) in buff: buff=directory+buff
                if not buff[len(buff)-1:]==chr(92): buff+=chr(92)
            elif ":\\" in x:
                buff=""; fix=x.split(chr(92))
                fix.pop(); x=fix[len(fix)-1]; fix.pop()
                for i in fix: buff+=i+chr(92)
            else: buff=directory
            buff=fixaddr(buff)
            if not buff==None:
                x=x.replace("\n","in")
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
