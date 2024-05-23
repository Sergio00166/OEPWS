#Code by Sergio1260

     
if not __name__=="__main__":

    from os import getcwd, sep, read
    from sys import argv, path
    from os.path import isabs, isdir
    from glob import glob
    from functions1 import get_size, read_UTF8, CalcRelLine, get_str
    from functions import str_len, fscp
    from upd_scr import update_scr
    from keys_func import keys_func
    from subprocess import check_output
    path.append(path[0]+sep+"lib.zip")
    from colorama import init, Fore, Back, Style, deinit
    from threading import Thread
    from time import sleep as delay
    from time import time

    # Define colors

    init(autoreset=False,convert=True)
    reset=Style.RESET_ALL
    bnc=Back.LIGHTWHITE_EX+Fore.BLACK+Style.DIM
    black=Back.LIGHTCYAN_EX+Fore.BLACK+Style.DIM
    slc=Back.LIGHTYELLOW_EX+Fore.BLUE+Style.BRIGHT
    deinit(); del init, Fore, Back, Style, deinit

    if not sep==chr(92): #If OS is LINUX
        #Get default values for TTY
        from termios import TCSADRAIN,\
        tcsetattr, tcgetattr, ICANON, ECHO
        from sys import stdin
        fd = stdin.fileno()
        old_settings = tcgetattr(fd)

    version="v0.5.7.3"

    if sep==chr(92):

        from msvcrt import getch as getchar, kbhit

        def getch():
            out,count = [getchar()],0
            while kbhit():
                out.append(getchar())
                count+=1
                if count==8: break
            return b''.join(out)

    else: # Linux

        def getch():
            old=(fd,TCSADRAIN,old_settings)
            terminal = tcgetattr(fd)
            terminal[3] = terminal[3] & ~(ICANON | ECHO)
            tcsetattr(fd, TCSADRAIN, terminal)
            try: out=read(fd,8)
            except KeyboardInterrupt:
                 out=b'\x03'
            finally: tcsetattr(*old)
            return out

    #Check if we have arguments via cli, if not create an empty one
    if not len(argv)==1:
        files=[glob(x,recursive=False) for x in argv[1:]]
        files=[i for x in files for i in x if not isdir(i)]
        if len(files)>0: 
            arr=read_UTF8(files[0])
            filename=files[0]; files=files[1:]
        else: filename=getcwd()+sep+"NewFile"; arr=[""]; files=[]    
    else: filename=getcwd()+sep+"NewFile"; arr=[""]; files=[] 

    # Creates a list of banned chars code

    values=["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
    fixstr=[]
    for x in range(0,2):
        for y in values:
            fixstr.append(str(x)+y)

    #Define a lot of stuff
    pointer=offset=oldptr=0
    line=banoff=1
    banner=["pBTE",version]
    copy_buffer,select = "",[]
    end,start,ch_T_SP = 1,0,False

    rows,columns=get_size()

    #Flag to show after saving the file
    saved_txt="SAVED"; status=saved_df=" "*5; status_st=False
    print("\033c", end="") # Clear the screen


    # Here we have all the mapped scape codes for the keys and for Windows and Linux

    if sep==chr(92):
        
        keys = {"special":b'\xe0',"delete":b'\x08',"return":b'\r',"ctrl+s":b'\x13',
                "ctrl+n":b'\x0e',"ctrl+x":b'\x18',"ctrl+c":b'\x03',"ctrl+p":b'\x10',
                "ctrl+g":b'\x07',"ctrl+a":b'\x01',"ctrl+o":b'\x0f',"ctrl+t":b'\x14',
                "ctrl+b":b'\x02',"ctrl+e":b'\x05',"arr_up":b'\xe0H',"arr_down":b'\xe0P',
                "arr_right":b'\xe0M',"arr_left":b'\xe0K',"supr":b'\xe0S',"start":b'\xe0G',
                "end":b'\xe0O',"repag":b'\xe0I',"avpag":b'\xe0Q',"tab":b'\t',"insert":b'\xe0R',
                "ctrl+arr_up":b'\xe0\x8d',"ctrl+arr_down":b'\xe0\x91',"ctrl+arr_left":b'\xe0s',
                "ctrl+arr_right":b'\xe0t',"ctrl+repag":b'\xe0\x86', "ctrl+avpag":b'\xe0v'}
    else:
        keys = {"special":b'\x1b',"delete":b'\x7f',"return":b'\n',"ctrl+s":b'\x13',
                "ctrl+n":b'\x0e',"ctrl+x":b'\x18',"ctrl+c":b'\x03',"ctrl+p":b'\x10',
                "ctrl+g":b'\x07',"ctrl+a":b'\x01',"ctrl+o":b'\x0f',"ctrl+t":b'\x14',
                "ctrl+b":b'\x02',"ctrl+e":b'\x05',"arr_up":b'\x1b[A',"arr_down":b'\x1b[B',
                "arr_right":b'\x1b[C',"arr_left":b'\x1b[D',"supr":b'\x1b[3~',"start":b'\x1b[H',
                "end":b'\x1b[F',"repag":b'\x1b[5~',"avpag":b'\x1b[6~',"tab":b'\t',"insert":b'2',
                "ctrl+arr_up":b'\x1b[1;5A',"ctrl+arr_down":b'\x1b[1;5B',"ctrl+arr_left":b'\x1b[1;5D',
                "ctrl+arr_right":b'\x1b[1;5C',"ctrl+repag":b'\x1b[5;5~',"ctrl+avpag":b'\x1b[6;5~'}


