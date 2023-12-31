#Code by Sergio1260

from glob import glob
from os.path import getmtime, getctime,getsize, isdir
from colors import color
from sizes import get_directory_size as dir_size
import re


def sort(arg,arg1,directory):
    try:
        green=color("","Gnr")
        blue=color("","Bnr")
        yellow=color("","Ynr")
        reset=color()
        mode=arg[5:len(arg)-1]
        arg1=arg1.replace("'in'","\f")
        if arg1=="": arg1=".*"; dirt=directory
        elif " in " in arg1:
            dirt=arg1[arg1.find(" in ")+4:]
            arg1=arg1[:arg1.find(" in ")]
            if not ":\\" in dirt: dirt=directory+dirt
            dirt+=chr(92)
        elif ":\\" in arg1: dirt=arg1; arg1=".*"
        else: dirt=directory
        dirt=dirt.replace("\\\\","\\")
        if arg1.endswith(chr(92)):
            arg1=arg1[:len(arg1)-1]
            onlydir=True
        else: onlydir=False
        pattern=re.compile(arg1); files=[]
        all_files=glob(dirt+"\\*",recursive=False, include_hidden=True)
        for x in all_files:
            if pattern.search(x):
                if onlydir:
                    if isdir(x): files.append(x)
                else: files.append(x)
                
        if not len(files)==0:
            
            if mode=="mtime":
                print("\n┌─"+green+" Directory "+reset+blue+dirt+reset+"\n│")
                out=sorted(files, key=lambda x: getmtime(x))
                for x in  reversed(out):
                    x=x.replace(dirt,"")
                    print("├   "+yellow+x+reset)
                print("└─") 
                    
            elif mode=="ctime":
                print("\n┌─"+green+" Directory "+reset+blue+dirt+reset+"\n│")
                out=sorted(files, key=lambda x: getctime(x))
                for x in  reversed(out):
                    x=x.replace(dirt,"")
                    print("├   "+yellow+x+reset)
                print("└─") 
                    
            elif mode=="alpha":
                print("\n┌─"+green+" Directory "+reset+blue+dirt+reset+"\n│")
                fix=[]; dic={}
                for z in files:
                    xd=z.split(chr(92))
                    xd=xd[len(xd)-1].lower()
                    z=z.replace(dirt,"")
                    fix.append(xd); dic[xd]=z
                for x in sorted(fix): print("├   "+yellow+dic[x]+reset)
                print("└─")    
                        
            elif mode=="size":
                print("\n┌─"+green+" Directory "+reset+blue+dirt+reset+"\n│")
                fix=[]; dic={}
                for z in files:
                    if isdir(z): size=dir_size(z)
                    else: size=getsize(z)
                    z=z.replace(dirt,"")
                    if size in dic: dic[size]=dic[size]+"\n"+z
                    else: fix.append(size); dic[size]=z
                out=reversed(sorted(fix))
                for x in out:
                    ext=dic[x].split("\n")
                    for p in ext:
                        print("├   "+yellow+p+reset)
                print("└─")
            
        else: print("\n  "+color(arg1,"M")+color(" does not exist in","R")+" "+color(dirt,"B")+"\n")
    except: print(color("\n   Error\n","R"))
    
