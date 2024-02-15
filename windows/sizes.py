#Code by Sergio1260

from os import path, scandir
from colors import color
from glob import glob
from other import readable, fixcrdir
from syntax import parse_syntax

def get_directory_size(directory):
    total = 0
    try:
        for entry in scandir(directory):
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_directory_size(entry.path)
    except NotADirectoryError: return path.getsize(directory)
    except PermissionError: return 0
    return total

def sizwk(i,directory):
    if path.isdir(i): return dirsize(i,directory)
    else:
        file_size = path.getsize(i)
        i=i.replace(directory,"")
        ext=(color('   File ',"G")+color(i,"B")+"\n")
        ext+=(color('   Size: ',"Y")+color(readable(file_size),"B")+"\n")
        return ext

def dirsize(arg1,directory):
    if arg1=="": direct=directory
    else:
        if ":\\" in arg1: direct=arg1
        else: direct=directory + arg1
    for x in glob(direct, recursive=False):
        size=get_directory_size(x)
        size=readable(size)
        if not x.endswith(chr(92)): x+=chr(92)
        x=x.replace(directory,"")
        if x=="": x=fixcrdir(directory)
        ext=(color("   Directory: ","G")+color(x,"B")+"\n")
        ext+=(color("   Dir size: ","Y")+color(size,"B")+"\n")
    return ext

def size(arg1,directory):
    from multiprocessing import Pool, cpu_count
    from functools import partial
    try:
        print("")
        files = parse_syntax(arg1,directory,["in",None])
        files = [content for file in files for content in glob(file, recursive=False)]  
        worker=partial(sizwk, directory=directory)
        pool=Pool(processes=cpu_count())
        exp=pool.map_async(worker,files)
        out=exp.get()
        if not len(out)==0:
            for i in out:
                print(i.replace(directory,""))
        else: print(color("   It doesn't exist","R")+"\n")
    except SyntaxError: print(color("   Syntax Error","R"))
    except: print(color("   Error\n","R"))

def dskinfo(arg1, directory):
    from psutil import disk_usage
    try:
        print("")
        if arg1=="":
            dirt=directory[:directory.find(chr(92))+1]
        else:
            if len(arg1)==1: arg1+=":"
            if not arg1[len(arg1)-1:]==chr(92): arg1+=chr(92)
            dirt=arg1[:arg1.find(chr(92))+1]
        print("┌─ "+color("Disk ","G")+color(dirt,"B")+"\n│")
        total,used,free,percent=disk_usage(dirt)
        print("├  "+color("Total: ","Y-")+color(readable(total),"B"))
        print("├  "+color("Free: ","Y-")+color(readable(free),"B"))
        print("├  "+color("Used: ","Y-")+ color(readable(used),"B"))
        if percent>=75:
            percent=color(str(percent) + "%","M")
        elif percent>=50 and percent<75:
            percent=color(str(percent) + "%","R")
        elif percent>=25 and percent<50:
            percent=color(str(percent) + "%","G")
        else: percent=color(str(percent) + "%","B") 
        print("├  "+color("Used percent: ","Y-") + percent)
        print("└─")
    except: print(color("   Error","R"))
    print("")
