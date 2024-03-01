#Code by Sergio1260

from multiprocessing import Pool
from glob import glob
from itertools import chain
from functools import partial
from subprocess import Popen
from sys import path

from multiprocessing import cpu_count

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
        out=f'cd "{directory}" ; &"{out}"'
        if not arg2=="": out+=" "+arg2
        com=["powershell.exe", "-Command", out]
        process = Popen(com); process.wait()
    else: return True

def main(arg1, arg2, directory):
    com=["powershell.exe","-Command"]
    com+=[path[0]+'\\import\\powershell\\trycmd.ps1']
    com+=[directory, arg1+" "+arg2]; process = Popen(com); process.wait()
    if process.returncode==1: return startcmd(arg1,arg2,directory)
