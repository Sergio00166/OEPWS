#Code by Sergio00166

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


def filter_wk(data,pattern,onlydir):
    out = []
    for x in data:
        if pattern.search(fileonly(x)):
            if onlydir:
                if isdir(x): out.append(x)
            else: out.append(x)
    return out


def list_wk(path):
    path, dirs = path+chr(92)+"*", []
    out = glob(path,recursive=False,include_hidden=True)
    if len(out)>0:
        for x in out:
            if isdir(x): dirs.append(x)
        return [dirs,out]
    else: return [[],[]]


def proc(x,buff,recurse):
    if x.endswith(chr(92)):
        x=x[:len(x)-1]
        onlydir=True
    else: onlydir=False
    pattern=re.compile(x)
    prew,filepath = list_wk(buff[:-1])

    if not buff==None and recurse:
        pool=Pool(processes=cpu_count())
        while not len(prew)==0:
            ext = pool.map_async(list_wk,prew).get()
            prew = [] # Clear buffer
            for x in ext: prew+=x[0]; filepath+=x[1]

        flwk = partial(filter_wk,pattern=pattern,onlydir=onlydir)
        out = pool.map_async(flwk,filepath).get()
        out = list(chain(*out))
        
        return out,onlydir
    return prew,[]


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
                if not recurse: ext=" in "
                else: ext=" inside "
                print("  "+color(x,"M")+color(" does not exist"+ext,"R")+color(buff,"B"))
        print("")
    
    except: print(color("   Error\n","R"))
