#Code by Sergio1260

from glob import glob
from colors import color
from multiprocessing import cpu_count, Pool
from functools import partial
from other import fixfiles
from os.path import isfile
import re
from fnmatch import translate
from sys import setrecursionlimit

setrecursionlimit(10**6) # increase the recursion limit

def finwk(x, filedir, lines):
    found=""; ext=""; text=lines[x[0]]
    for i in x[1]:
        found+=color(i,"B")
        if not x[1].index(i)==len(x[1])-1:
            found+=color(",","G")
        text=text.replace(i,color(i,"bW"))
        filedir=filedir.split("\\"); filedir=filedir[len(filedir)-1]
    ext+=("  "+found+color(" found in file:","G")+" "+color(filedir,"B-")
          +" "+color("in line:","G")+" "+color(str(x[0]+1),"R")+"\n")
    ext+=(color("  > ","R")+text.lstrip())
    return ext

def main(arg1,directory):
    try:
        print("")
        dic=[]; arg1=arg1.replace("'in'","\f")
        if " in " in arg1:
            fich=arg1[:arg1.find(" in ")]
            ind=arg1[arg1.find(" in ")+4:arg1.find(" find ")]
            filedir=ind+chr(92)+fich
        else:
            fich=arg1[:arg1.find(" find ")]
            if ":\\" in fich: filedir=fich
            else: filedir=directory+fich
        filedir=filedir.replace("\\\\","\\")
        if " find " in arg1:
            fin=arg1[arg1.find(" find ")+6:]
            if fin=="": fin="*"
            fin=fin.replace("'::'","\n")
            fin=fin.split("::"); buff=[]
            for x in fin: buff.append(x.replace("\n","::"))
            fin=buff; del buff
        filedir=fixfiles(filedir.replace("\f","in"))
        for file in glob(filedir, recursive=False):
            if isfile(file):
                lines=open(file, "r").readlines()
                fix=[]; exp={}
                for x in fin:
                    pattern = re.compile(x)
                    for i, line in enumerate(lines):
                        match = pattern.search(line)
                        if match: fix.append([i,[x]])
                for index, txt in fix:
                    if index in exp:
                        exp[index].extend(txt)
                    else: exp[index] = txt
                exp = [[k, v] for k, v in exp.items()]
                exp=sorted(exp, key=lambda item: item[0])
                pool=Pool(processes=cpu_count())
                grep=partial(finwk, filedir=file, lines=lines)
                ext=pool.map_async(grep,exp)
                out=ext.get()
                if not len(out)==0:
                    for x in out:
                        print(x)
                        if not x[len(x)-1]=="\n": print("")
                    
    except:  print(color("   Error\n","R"))
