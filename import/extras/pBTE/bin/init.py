# Code by Sergio00166

version="v0.6.5.0"
     
if not __name__=="__main__":

    from os import getcwd, sep, read
    from sys import argv, path
    from os.path import abspath, isdir
    from functions1 import get_size,read_UTF8
    from upd_scr import update_scr
    from keys_func import keys_func
    path.append(path[0]+sep+"lib.zip")
    from colorama import init, Fore, Back, Style, deinit
    from threading import Thread
    from time import sleep as delay
    from glob import glob
    from data import keys

    # Define colors
    init(autoreset=False,convert=True)
    reset=Style.RESET_ALL
    bnc=Back.LIGHTWHITE_EX+Fore.BLACK+Style.DIM
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


    #Check if we have arguments via cli, if not create an empty one
    if not len(argv)==1:
        files=[glob(x,recursive=False) for x in argv[1:]]
        files=[abspath(i) for x in files for i in x if not isdir(i)]
        if len(files)>0: 
            arr,codec,lnsep = read_UTF8(files[0])
            filename=files[0]; files=files[1:]
            files = [x.replace(sep,"/") for x in files]
        else:
            filename=getcwd()+sep+"NewFile"
            arr,files = [""],[]   
            codec,lnsep = "UTF-8","\n" 
    else:
        filename=getcwd()+sep+"NewFile"
        arr,files = [""],[]   
        codec,lnsep = "UTF-8","\n"

    filename = filename.replace(sep,"/")

    #Define a lot of stuff
    offset=oldptr=0
    cursor=line=banoff=1
    banner=["pBTE",version]
    copy_buffer,select = "",[]
    end,start,indent = 1,0,"\t"
    comment = ["#",""]
    rows,columns=get_size()

    #Flag to show after saving the file
    saved_txt="SAVED"; status=saved_df=" "*5; status_st=False
    print("\033c", end="") # Clear the screen
    print("\033[1 q", end="") # Change cursor


