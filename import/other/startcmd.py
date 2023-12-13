#Code by Sergio1260

from multiprocessing import Pool
from glob import glob
from itertools import chain
from functools import partial
from os import system as cmd
from sys import path

from multiprocessing import cpu_count

def fixaddr(arg):
    fixdrt=""
    for x in arg.split("\\"):
        if not x=="":
            if " " in x: x="'"+x+"'"
            fixdrt+=x+chr(92)
    return fixdrt[:len(fixdrt)-1]

def worker(arg, arg2):
    filepath=glob(arg+chr(92)+arg2+".exe", recursive=False)
    if len(filepath)>0: return filepath
    else: return []
                
def lister(arg): return glob(arg+"**"+chr(92), recursive=False)

def proc(buff):
    prew=glob(buff+"**"+chr(92), recursive=False)
    pool=Pool(processes=cpu_count()-1); tree=[buff]
    while not len(prew)==0:
        tree+=prew
        ext=pool.map_async(lister,prew)
        prew=list(chain(*ext.get()))
    return tree

def startcmd(val,arg2, directory):
    paths=["C:\\Program Files\\", "C:\\Program Files (x86)\\"]
    tree=[]; pool=Pool(processes=cpu_count())
    for x in paths: tree+=proc(x)
    searcher = partial(worker, arg2=val)
    ext=pool.map_async(searcher,tree); out=[]
    out=list(chain(*ext.get()))
    if not len(out)==0:
        out=out[0].replace("\\\\","\\")
        if arg2=="": text=('start /D "'+directory+'" /WAIT /B " " "'+out+'"')
        else: text=('start /D "'+directory+'" /WAIT /B " " "'+out+'" '+arg2)
        if cmd(text)==1: return True
    else: return True

def main(arg1, arg2, directory):
    directory=fixaddr(directory)
    fix=arg1+" "+arg2
    com=('powershell Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Bypass -Force; ')
    if not chr(92) in arg1: com+=(path[0]+'\\import\\powershell\\trycmd.ps1 "'+directory+'" "'+"'"+fix+"'"+'"')
    else: com+=(path[0]+'\\import\\powershell\\trycmd.ps1 \\"'+directory+'\\" \\"'+fix+'\\"')
    if cmd(com)==1: return startcmd(arg1,arg2,directory)
