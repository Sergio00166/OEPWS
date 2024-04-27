#Code by Sergio1260

from glob import glob
from colors import color
from pathlib import Path
from other import fixaddr, fixcrdir
from syntax import parse_syntax

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
            worker(file, level + 1)
        else:
            prefix = "└── " if is_last_item else "├── "
            print("   "+spacing+prefix+green+file_name+reset)

def tree(arg1, directory):
    global blue, green, reset
    blue=color("","Bnr")
    green=color("","Gnr")
    reset=color()
    path=parse_syntax(arg1,directory,["in",None])[0]
    if path.endswith(chr(92)): path=path[:-1]
    dirt=path.split(chr(92))[-1]
    if not path==None:
        print("\n   "+blue+dirt+reset)
        worker(path); print("")

def print_files(files, max_width):
    current_width = 0
    for file in files:
        if files.index(file)==0:
            print("├   ",end="")
        elif current_width+len(file)>=max_width:
            print("\n├   ",end="")
            current_width = 0
        else: print(" · ", end="")
        print(file, end="")
        current_width += len(file)
    print("")

def ls(arg1, directory):
    from os.path import islink, isdir
    from os import get_terminal_size
    green=color("","Gnr"); blue=color("","Bnr")
    magenta=color("","Mnr"); red=color("","Rnr")
    reset=color()

    dirt=parse_syntax(arg1,directory,["from",None])

    for y in dirt:
        buff=glob(y, recursive=False)
        if not len(buff)==0:
            for x in buff:
                try:
                    if ":"+chr(92) in arg1 or arg1=="": dirt=x
                    else: dirt=x.replace(directory,"")
                    if not dirt.endswith(chr(92)): dirt+=chr(92)
                    if dirt==directory: dirt=fixcrdir(directory)+chr(92)
                    else: dirt=dirt.replace(directory,"")
                    x=fixaddr(x, True); exp=""
                    if not x==None:
                        print("\n┌─"+green+" Contents of "+reset+blue+dirt+reset+"\n│")
                        ext = glob(x+'*', recursive=False, include_hidden=True)
                        if not len(ext)==0:
                            file_list = []
                            for z in ext:
                                if islink(z) or z.endswith((".lnk",".url")):
                                    content=magenta+z.replace(x,"")+reset
                                elif isdir(z): content=blue+z.replace(x,"")+reset
                                else: content=green+z.replace(x,"")+reset
                                file_list.append(content)
                            max_width = get_terminal_size().columns
                            print_files(file_list, max_width)
                        else:  print("├   "+red+"EMPTY DIRECTORY"+reset)
                        print("└─")
                except: pass
        else: print("\n   "+color("The dir doesn't exist","R"))
    print("")
