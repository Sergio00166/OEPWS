# Code by Sergio00166

version="v0.6.0.0"
     
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

    # Define colors
    init(autoreset=False,convert=True)
    reset=Style.RESET_ALL
    bnc=Back.LIGHTWHITE_EX+Fore.BLACK+Style.DIM
    black=Back.LIGHTCYAN_EX+Fore.BLACK+Style.DIM
    slc=Back.LIGHTYELLOW_EX+Fore.BLUE+Style.BRIGHT
    deinit(); del init, Fore, Back, Style, deinit

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
        else:
            filename=getcwd()+sep+"NewFile"
            arr,files = [""],[]   
            codec,lnsep = "UTF-8","\n" 
    else:
        filename=getcwd()+sep+"NewFile"
        arr,files = [""],[]   
        codec,lnsep = "UTF-8","\n"

    #Define a lot of stuff
    offset=oldptr=0
    pointer=line=banoff=1
    banner=["pBTE",version]
    copy_buffer,select = "",[]
    end,start,indent = 1,0,"\t"
    comment = ["#",""]
    rows,columns=get_size()

    #Flag to show after saving the file
    saved_txt="SAVED"; status=saved_df=" "*5; status_st=False
    print("\033c", end="") # Clear the screen


    # Here we have all the mapped scape codes for the keys and for Windows and Linux

    if sep==chr(92):
        
        keys = {"delete":b'\x08',"return":b'\r',"ctrl+s":b'\x13',"ctrl+d":b'\x04',
                "ctrl+n":b'\x0e',"ctrl+x":b'\x18',"ctrl+c":b'\x03',"ctrl+p":b'\x10',
                "ctrl+g":b'\x07',"ctrl+a":b'\x01',"ctrl+o":b'\x0f',"f1":b'\x00;',
                "f2":b'\x00<',"f3":b'\x00=',"ctrl+b":b'\x02',"ctrl+q":b'\x11',
                "arr_up":b'\xe0H',"arr_down":b'\xe0P',"arr_right":b'\xe0M',"arr_left":b'\xe0K',
                "supr":b'\xe0S',"start":b'\xe0G',"end":b'\xe0O',"repag":b'\xe0I',
                "avpag":b'\xe0Q',"tab":b'\t',"insert":b'\xe0R',"ctrl+arr_up":b'\xe0\x8d',
                "ctrl+arr_down":b'\xe0\x91',"ctrl+arr_left":b'\xe0s',"ctrl+arr_right":b'\xe0t',
                "ctrl+repag":b'\xe0\x86', "ctrl+avpag":b'\xe0v',"ctrl+k":b'\x0b',"ctrl+u":b'\x15'}
    else:
        keys = {"delete":b'\x7f',"return":b'\r',"ctrl+s":b'\x13',"ctrl+d":b'\x04',
                "ctrl+n":b'\x0e',"ctrl+x":b'\x18',"ctrl+c":b'\x03',"ctrl+p":b'\x10',
                "ctrl+g":b'\x07',"ctrl+a":b'\x01',"ctrl+o":b'\x0f',"f1":b'\x1bOP',
                "f2":b'\x1bOQ',"f3":b'\x1bOR',"ctrl+b":b'\x02',"ctrl+q":b'\x11',
                "arr_up":b'\x1b[A',"arr_down":b'\x1b[B',"arr_right":b'\x1b[C',
                "arr_left":b'\x1b[D',"supr":b'\x1b[3~',"start":b'\x1b[H',
                "end":b'\x1b[F',"repag":b'\x1b[5~',"avpag":b'\x1b[6~',"tab":b'\t',
                "insert":b'2',"ctrl+arr_up":b'\x1b[1;5A',"ctrl+arr_down":b'\x1b[1;5B',
                "ctrl+arr_left":b'\x1b[1;5D',"ctrl+arr_right":b'\x1b[1;5C',
                "ctrl+repag":b'\x1b[5;5~',"ctrl+avpag":b'\x1b[6;5~',"ctrl+k":b'\x0b',
                "ctrl+u":b'\x15'}

