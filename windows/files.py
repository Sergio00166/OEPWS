#Code by Sergio1260

from colors import color
from os import system as cmd
from dirfil_main import extra
from os.path import isdir
from other import fixfiles, fixcrdir

def lsacl(arg1, directory):
    print(""); reset=color()
    green=color("","Gnr"); blue=color("","Bnr")
    yellow=color("","Ynr"); red=color("","Rnr")
    if arg1=="" or arg1==".\\": arg1=directory[:len(directory)-1]
    out=extra(6,arg1,directory)
    if not len(out)==0:
        for x in out:
            file=x[1];ext=str(x[0]); buff=""
            file=fixfiles(file)
            if isdir(file):
                if file+chr(92)==directory: file=fixcrdir(directory)+chr(92)
                else: file=file.replace(directory,"")+chr(92)
            file=file[:len(file)].replace(directory,"")
            buff+=("┌─ "+green+"Object: "+reset+blue+file+reset+"\n│\n")
            ext=ext[ext.find(" "):]; fix=[]; ext=ext.split("\\n")
            for x in ext: fix.append(x.lstrip().rstrip())
            fix.pop(); fix.pop(); fix.pop()
            for x in fix:
                buff+=(reset+"├  ")
                x=x.split(":"); y=x[0].split("\\\\")
                try:
                    buff+=(yellow+y[0]+blue+"\\"+green+y[1]+
                            blue+": "+red+x[1]+"\n")
                except: buff+=(green+y[0]+blue+": "+red+x[1]+"\n")
            buff+=reset+"└─\n\n"
            print(buff, end="")
    else: print(color("   Error\n","R"))

def delete(arg1, directory):
    if not arg1=="": extra(2,arg1,directory)
    else: print(color("\n   Error\n","R"))

def edit_file(arg1, directory):
    from sys import path
    nano=path[0]+"\\import\\extras"+chr(92)+"nano.exe "
    if not len(arg1)==0:
        if "from" in arg1:
            fro=arg1.find("from"); fich=arg1[:fro]; files=arg1.split("::")
            for arg1 in files:
                if not chr(92) in arg1[fro+5:] and len(arg1[fro+5:])==2 and ":" in arg1[fro+5:]:
                    direct=arg1[fro+5:] + chr(92)
                elif not chr(92) in arg1[fro+5:] and not ":" in arg1[fro+5:]:
                    direct=directory + arg1[fro+5:] + chr(92)
                else: direct=arg1[fro+5:]
                exp='"'+fixfiles(direct+chr(92)+fich)+'"'
                exp=str(exp).replace(chr(92)+chr(92),chr(92))
                cmd("START /B /WAIT "+nano+exp)
        else:
            files=arg1.split("::")
            for arg1 in files:
                if not ":"+chr(92) in arg1: exp='"'+directory+arg1+'"'
                else: exp='"'+fixfiles(arg1)+'"'
                cmd("START /B /WAIT "+nano+exp)
    else: print(color("\n   Error\n","R"))

def write_to_file(arg1, directory):
    text=arg1[arg1.find('[')+1:arg1.find('] to ')]+" "
    fich=arg1[arg1.find('] to ')+5:]
    args=arg1[:arg1.find('[')-1]
    if args=="-flush": mode="w"
    else: mode="a"
    text=text[:len(text)-1]
    text=text.replace("\\\\n","\fn").replace("\\\\f","\ff")
    text=text.replace("\\f","\n").replace("\\\\t","\ft")
    text=text.replace("\\\\b","\fb").replace("\\\\r","\fr")
    text=text.replace("\\n","\n").replace("\\t","\t")
    text=text.replace("\\b","\b").replace("\\r","\r")
    text=text.replace("\fn","\\n").replace("\ft","\\t")
    text=text.replace("\fb","\\b").replace("\ff","\\f")
    text=text.replace("\fr","\\r").replace("\\\\","\\")
    extra(4,fich,directory,text,mode)

def chmod(arg1, directory):
    #chmod [user1:r],[user2:f] for file
    file=arg1[arg1.find(" for ")+5:]
    args=arg1[:arg1.find("[")]
    perms=arg1[arg1.find("["):arg1.find(" for ")]
    perms=perms.split(",")
    for x in perms:
        x=x.replace("[","").replace("]","")
        fix=x.split(":"); user=fix[0]; perm=fix[1]
        if args=="set ": extra(7,file,directory,"/E /P "+user+":N")
        for i in perm:
            if not (i=="" or i=="n"):
                extra(7,file,directory,"/E /G "+user+":"+i)

def chown(arg1, directory):
    #chmown user1 for file
    from other import isadmin
    if isadmin():
        file=arg1[arg1.find(" for ")+5:]
        user=arg1[:arg1.find(" for ")]
        extra(5,file,directory,"/setowner "+user)
    else: print(color("\n   You must be admin to do that\n","R"))

def files(arg,arg1,directory):
    if arg=="new":
        if not arg1=="": extra(1,arg1,directory)
        else: print(color("\n   Error\n","R"))
    elif arg=="no": delete(arg1, directory) 
    elif arg=="edit": edit_file(arg1, directory)
    elif arg=="write": write_to_file(arg1, directory)
    elif arg=="flush": extra(3,arg1,directory)
    elif arg=="chmod": chmod(arg1, directory)           
    elif arg=="chown": chown(arg1, directory)     
    elif arg=="lsacl": lsacl(arg1, directory)
