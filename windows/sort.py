#Code by Sergio1260

from glob import glob
from os.path import getmtime, getctime,getsize
from colors import color

def work(mode,i,directory,dirt):
    out=[]  
    if mode=="mtime":
        files=glob(dirt+"\\"+i,recursive=False)
        out=sorted(files, key=lambda x: getmtime(x))
        for x in reversed(out):
            x=x.replace(directory,"")
            out.append(i)
            
    elif mode=="ctime":
        files=glob(dirt+"\\"+i,recursive=False)
        out=sorted(files, key=lambda x: getctime(x))
        for x in reversed(out):
            x=x.replace(directory,"")
            out.append(x)
            
    elif mode=="alpha":
        files=glob(dirt+"\\"+i,recursive=False)
        fix=[]; dic={}
        for z in files:
            xd=z.split(chr(92))
            xd=xd[len(xd)-1].lower()
            z=z.replace(directory,"")
            fix.append(xd); dic[xd]=z
        for x in sorted(fix): out.append(dic[x])
                
    elif mode=="size":
        files=glob(dirt+"\\"+i,recursive=False)
        fix=[]; dic={}
        for z in files:
            size=getsize(z)
            z=z.replace(directory,"")
            fix.append(size)
            dic[size]=z
        out=reversed(sorted(fix))
        for x in out: out.append(dic[x])
        
    return out

        
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
    for x in arg1:
        out=work(mode,x,directory,dirt)
        print("\n┌─"+green+" Directory "+reset+blue+dirt+reset+"\n│")
        for x in out: print("├   "+yellow+x+reset)
        print("└─")    
    
    
