#Code by Sergio1260

from glob import glob
from colors import color
from multiprocessing import cpu_count, Pool
from itertools import chain
from functools import partial
from sys import setrecursionlimit
from os.path import isdir, isabs
from syntax import parse_basic_syntax
import re

setrecursionlimit(10**6) # increase the recursion limit


def fileonly(arg):
    arg=arg.split(chr(92))
    return arg[len(arg)-1]

def worker(arg,pattern,onlydir):
    filepath = glob(arg+chr(92)+"*", recursive=False)
    if len(filepath)>0:
        out=[]; dirs=[]
        for x in filepath:
            if isdir(x): dirs.append(x)
            if pattern.search(fileonly(x)):
                if onlydir:
                    if isdir(x): out.append(x)
                else: out.append(x)
        return [dirs,out]
    else: return [[],[]]

def proc(x,buff,recurse):
    if x.endswith(chr(92)):
        x=x[:len(x)-1]
        onlydir=True
    else: onlydir=False
    pattern=re.compile(x)
    if not buff==None:
        if recurse==True:
            pool=Pool(processes=cpu_count()-1)
            prew,filepath = worker(buff,pattern,onlydir)
            while not len(prew)==0:
                lister = partial(worker, pattern=pattern,onlydir=onlydir)
                ext=pool.map_async(lister,prew).get()
                prew = list(chain.from_iterable([sublista[0] for sublista in ext]))
                filepath += list(chain.from_iterable([sublista[1] for sublista in ext]))
        else:
            filepath=[]
            for z in glob(buff+"*", recursive=False):
                if pattern.search(fileonly(z)):
                    if onlydir:
                        if isdir(z): filepath.append(z)
                    else: filepath.append(z)
            
    return filepath,onlydir

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
            filepath,onlydir = proc(x,buff,recurse)
            yellow=color("","nrY"); reset=color()
            if not len(filepath)==0:
                print("┌─> "+color(x,"M")+color(" is located on:","G")+"\n│")
                for i in filepath:
                    i=i.replace("\\\\","\\").replace("\\\\","\\")
                    print("├  "+yellow+i+reset)
                print("└─")      
            else:
                if not recurse: ext=" in"
                else: ext=" inside "
                print("  "+color(x,"M")+color(" does not exist"+ext,"R")+color(buff,"B"))
        print("")
    
    except: print(color("   Error\n","R"))
