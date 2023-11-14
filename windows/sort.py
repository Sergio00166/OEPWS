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
        if " in " in arg1:
            dirt=arg1[arg1.find(" in ")+4:]
            arg1=arg1[:arg1.find(" in ")]
            if not ":\\" in dirt:
                dirt=directory+dirt
        else: dirt=directory
        if arg1=="": arg1=".*"
        arg1=arg1.split("::")
        for i in arg1:
            pattern=re.compile(i); files=[]
            all_files=glob(dirt+"\\*",recursive=False, include_hidden=True)
            for x in all_files:
                if pattern.search(x):
                    files.append(x)
            
            if mode=="mtime":
                out=sorted(files, key=lambda x: getmtime(x))
                print("\n┌─"+green+" Directory "+reset+blue+dirt+reset+"\n│")
                for x in  reversed(out):
                    x=x.replace(directory,"")
                    print("├   "+yellow+x+reset)
                print("└─") 
                    
            elif mode=="ctime":
                out=sorted(files, key=lambda x: getctime(x))
                print("\n┌─"+green+" Directory "+reset+blue+dirt+reset+"\n│")
                for x in  reversed(out):
                    x=x.replace(directory,"")
                    print("├   "+yellow+x+reset)
                print("└─") 
                    
            elif mode=="alpha":
                fix=[]; dic={}
                for z in files:
                    xd=z.split(chr(92))
                    xd=xd[len(xd)-1].lower()
                    z=z.replace(directory,"")
                    fix.append(xd); dic[xd]=z
                print("\n┌─"+green+" Directory "+reset+blue+dirt+reset+"\n│")
                for x in sorted(fix): print("├   "+yellow+dic[x]+reset)
                print("└─")    
                        
            elif mode=="size":
                fix=[]; dic={}
                for z in files:
                    if isdir(z): size=dir_size(z)
                    else: size=getsize(z)
                    z=z.replace(directory,"")
                    if size in dic: dic[size]=dic[size]+"\n"+z
                    else: fix.append(size); dic[size]=z
                out=reversed(sorted(fix))
                print("\n┌─"+green+" Directory "+reset+blue+dirt+reset+"\n│")
                for x in out:
                    ext=dic[x].split("\n")
                    for p in ext:
                        print("├   "+yellow+p+reset)
                print("└─")
                
    except: print(color("\n   Error\n","R"))
    
