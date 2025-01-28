# Code by Sergio00166

version="v0.6.9.2"
     
if not __name__=="__main__":

    from os import getcwd, sep, read, environ
    from sys import argv, path

    # Add all file structure
    root = path[0]+sep+"bin"+sep
    path.append(path[0]+sep+"lib.zip")
    path.append(root+"core")
    path.append(root+"menus")
    
    from os.path import abspath, isdir
    from functions1 import get_size,read_UTF8,taborspace
    from upd_scr import update_scr
    from keys_func import keys_func
    from colorama import init, Fore, Back, Style, deinit
    from threading import Thread
    from time import sleep as delay
    from glob import glob
    from data import keys

    # Define colors
    init(autoreset=False,convert=True)
    reset=Style.RESET_ALL
    bnc=Back.LIGHTWHITE_EX+Fore.BLACK
    black=Back.LIGHTCYAN_EX+Fore.BLACK+Style.DIM
    slc=Back.LIGHTYELLOW_EX+Fore.BLUE+Style.BRIGHT
    deinit(); del init, Fore, Back, Style, deinit

    # Create the raw kb reader
    if sep==chr(92):
        from msvcrt import getch\
             as gch, kbhit
        
        def getch():
            out = gch()
            while kbhit(): out+=gch()
            return out
    else:
        #Get default values for TTY
        from termios import TCSADRAIN,tcsetattr,tcgetattr
        from sys import stdin; from tty import setraw
        from select import select as slsl
        fd = stdin.fileno(); old_settings = tcgetattr(fd)

        def getch():
            old=(fd,TCSADRAIN,old_settings)
            setraw(fd,when=TCSADRAIN)
            out,rlist = b'',True
            while rlist:
                out += read(fd,8)
                # Check if available data
                rlist = slsl([fd],[],[],0)[0]
            # Set TTY to default
            tcsetattr(*old)
            return out


    # Check if we have arguments via cli, if not create an empty one
    filename = getcwd()+sep+"NewFile"
    # Fix when current dir is root
    if filename.startswith("//"):
        filename = filename[1:]
    arr,codec,lnsep = [""],"UTF-8","\n"
    if not len(argv)==1:
        files = [glob(x,recursive=False) for x in argv[1:]]
        files = [abspath(i) for x in files for i in x if not isdir(i)]
        files = [x.replace(sep,"/") for x in files]
        if len(files)>0:
            # Skip unopenable files
            for _ in range(len(files)):
                try:
                    name,files = files[0],files[1:]
                    arr,codec,lnsep = read_UTF8(name)
                    filename = name
                    break
                except: pass
    else: files=[]

    #Define a lot of stuff
    indent = taborspace(arr)
    offset=oldptr=0
    cursor=line=banoff=1
    banner=["pBTE",version]
    copy_buffer,select = "",[]
    end,start = 1,0
    comment = ["#",""]
    rows,columns=get_size()
    filename = filename.replace(sep,"/")

    status=""; status_st=False
    print("\033c", end="") # Clear the screen
    print("\033[1 q", end="") # Change cursor


