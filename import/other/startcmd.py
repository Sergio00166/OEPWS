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
        out = [out,arg2] if len(arg2)>0 else [out]
        try: Popen(out, cwd=directory).communicate()
        except: pass
    else: return True

def main(arg1, arg2, directory):
    out = " ".join([arg1,arg2] if len(arg2)>0 else [arg1])
    try: Popen(out, cwd=directorys).wait()
    except FileNotFoundError: return startcmd(arg1,arg2,directory)
    except: pass
