#Code by Sergio1260

from glob import glob
from colors import color
from pathlib import Path
from other import fixaddr, fixcrdir

class Tree:

    def worker(path, level=0):
        global blue, green, reset
        path = Path(path)
        files = sorted(path.glob("*"))
        total_files = len(files)
        for index, file in enumerate(files):
            spacing = "│   " * level if level > 0 else ""
            is_last_item = index == total_files - 1
            file_name = file.name
            if file.is_dir():
                prefix = "└── " if is_last_item else "├── "
                print("   "+spacing+prefix+blue+file_name+reset)
                Tree.worker(file, level + 1)
            else:
                prefix = "└── " if is_last_item else "├── "
                print("   "+spacing+prefix+green+file_name+reset)

    def main(arg1, directory):
        global blue, green, reset
        blue=color("","Bnr")
        green=color("","Gnr")
        reset=color()
        if arg1=="": path=directory
        elif ":"+chr(92) in arg1: path=str(arg1)
        else: path=directory+chr(92)+str(arg1)
        path=fixaddr(path)
        if ":"+chr(92) in arg1: dirt=path
        else: dirt=path[:len(path)-1].replace(directory,"")
        if not path==None:
            dirt=dirt.replace(directory,"")
            if dirt=="": dirt=fixcrdir(directory)
            print("\n   "+blue+dirt+reset)
            Tree.worker(path); print("")


def ls(arg1, directory):
    from os.path import isfile, isdir, getmtime
    from datetime import datetime as dt
    green=color("","Gnr"); blue=color("","Bnr")
    magenta=color("","Mnr"); red=color("","Rnr")
    reset=color()
    if arg1=="": dirt=directory
    elif arg1=="\\": dirt="\\"
    elif ":\\" in arg1: dirt=arg1
    elif not chr(92) in arg1: dirt=directory+arg1+chr(92)
    else: dirt=directory+arg1
    if not dirt[len(dirt)-1:]==chr(92): dirt+=chr(92)
    dirt=dirt.split("::")
    for y in dirt:
        buff=glob(y, recursive=False)
        if not len(buff)==0:
            for x in buff:
                x=fixaddr(x)
                ext = glob(x+'*', recursive=False, include_hidden=True); exp=""
                if ":"+chr(92) in arg1 or arg1=="": dirt=x
                else: dirt=x[:len(x)-1].replace(directory,"")
                if not dirt[len(dirt)-1]==chr(92): dirt+=chr(92)
                if dirt==directory: dirt=fixcrdir(directory)+chr(92)
                print("\n┌─"+green+" Contents of "+reset+blue+dirt+reset+"\n│")
                if not len(ext)==0:                        
                    for z in ext:
                        try: hour = dt.fromtimestamp(getmtime(z)).strftime("%d-%m-%Y %H:%M:%S")
                        except: hour="##-##-#### ##:##:##"
                        if isdir(z): content=blue+z.replace(x,"")+reset
                        elif isfile(z):
                            if z.endswith((".lnk",".url")):  
                                content=magenta+z.replace(x,"")+reset
                            else: content=green+z.replace(x,"")+reset
                        print("├"+" "+hour+"  "+content)
                else:  print("├   "+red+"EMPTY DIRECTORY"+reset)
                print("└─")
        else: print("\n   "+color("The dir doesn't exist","R"))
        print("")
             
