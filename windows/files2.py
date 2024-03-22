#Code by Sergio1260

from colors import color
from os import system as cmd
from other import fixcrdir
from os.path import isdir
from syntax import parse_syntax


def lsacl(arg1, directory):
    from glob import glob
    from subprocess import check_output
    
    print(""); reset=color(); lstext=[]
    green=color("","Gnr"); blue=color("","Bnr")
    yellow=color("","Ynr"); red=color("","Rnr")
    try:
        file=parse_syntax(arg1,directory,["in",None])
        for x in file:
            files = glob(x, recursive=False)
            for exp in files:
                ext=[[str(check_output('ICACLS "'+exp+'" 2>nul',
                shell=True),encoding="cp857").replace(exp,"")]]
                ext.append(exp); lstext.append(ext)
      
        if not len(lstext)==0:
            for x in lstext:
                file=x[1];ext=str(x[0]); buff=""
                if isdir(file):
                    if file+chr(92)==directory: file=fixcrdir(directory)+chr(92)
                    else: file=file.replace(directory,"")+chr(92)
                file=file[:len(file)].replace(directory,"")
                buff+=("┌─ "+green+"Object: "+reset+blue+file+reset+"\n│\n")
                ext=ext[ext.find(" "):]; fix=[]; ext=ext.split("\\n")
                for x in ext: fix.append(x.lstrip().rstrip())
                fix.pop(); fix.pop(); fix.pop()
                for x in fix:
                    buff+=(reset+"├  "); x=x.split(":"); y=x[0].split("\\\\")
                    try: buff+=(yellow+y[0]+blue+"\\"+green+y[1]+blue+": "+red+x[1]+"\n")
                    except: buff+=(green+y[0]+blue+": "+red+x[1]+"\n")
                buff+=reset+"└─\n\n"
                print(buff, end="")
        else: print(color("   Error\n","R"))
        
    except SyntaxError: print(color("   Syntax Error\n","R"))
    except: print(color("   Error\n","R"))


def write_to_file(arg1, directory):
    try:
        text=arg1[arg1.find('[')+1:arg1.find('] to ')]+" "
        fich=arg1[arg1.find('] to "')+5:]
        args=arg1[:arg1.find('[')-1]
        if args=="flush": mode="w"
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

        file=parse_syntax(fich,directory,["in",None])
        for x in file:
            file = open(x, mode, encoding="UTF-8")
            file.write(text); file.close()
    
    except SyntaxError: print(color("\n   Syntax Error\n","R"))
    except PermissionError: print(color("\n   Permission denied\n", "R"))
    except: print(color("\n   Error\n","R"))

