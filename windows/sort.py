#Code by Sergio1260

from glob import glob
from os.path import getmtime, getctime,getsize, isdir
from colors import color
from sizes import get_directory_size as dir_size
   
def sort(arg,arg1,directory):
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
    arg1=arg1.split("::")
    for i in arg1:
        
        if mode=="mtime":
            files=glob(dirt+"\\"+i,recursive=False, include_hidden=True)
            out=sorted(files, key=lambda x: getmtime(x))
            print("\n┌─"+green+" Directory "+reset+blue+dirt+reset+"\n│")
            for x in  reversed(out):
                x=x.replace(directory,"")
                print("├   "+yellow+x+reset)
            print("└─") 
                
        elif mode=="ctime":
            files=glob(dirt+"\\"+i,recursive=False, include_hidden=True)
            out=sorted(files, key=lambda x: getctime(x))
            print("\n┌─"+green+" Directory "+reset+blue+dirt+reset+"\n│")
            for x in  reversed(out):
                x=x.replace(directory,"")
                print("├   "+yellow+x+reset)
            print("└─") 
                
        elif mode=="alpha":
            files=glob(dirt+"\\"+i,recursive=False, include_hidden=True)
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
            files=glob(dirt+"\\"+i,recursive=False, include_hidden=True)
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
    
    
