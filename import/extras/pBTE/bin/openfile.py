#Code by Sergio1260

from functions import decode, get_size
from upd_scr import menu_updsrc
from threading import Thread
from glob import glob
from os import getcwd, sep
from time import sleep as delay

if not sep==chr(92): import tty; import termios


def updscr_thr():
    global opentxt,openfile,rows,columns,black,reset,status,banoff
    global lenght,wrtptr,offset,line,arr,banner,filename,rows,columns
    global run, kill, fd, old_settings
    
    while not kill:
        delay(0.01)
        if run:
            # If OS is LINUX restore TTY to it default values
            if not sep==chr(92): termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            # Call Screen updater
            mode=(openfile,opentxt,wrtptr,lenght)
            arg=(black,reset,status,banoff,offset,line,\
            wrtptr,arr,banner,filename,rows,columns)
            rows,columns = menu_updsrc(arg,mode)
            # If OS is LINUX set TTY to raw mode
            if not sep==chr(92): tty.setraw(fd)

def exit():
    global fd, old_settings, run, kill, thr
    run=False; kill=True; thr.join()
    if not sep==chr(92):
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    print("\033c", end="")

def open_file(args):
    global opentxt,openfile,rows,columns,black,reset,status,banoff
    global lenght,wrtptr,offset,line,arr,banner,filename,rows,columns
    global run, kill, fd, old_settings, thr

    if not sep==chr(92): #If OS is LINUX
        #Get default values for TTY
        import sys; import termios; import tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

    filename,black,reset,rows,banoff,arr,columns,status,\
    offset,line,banner,status_st,getch,keys,pointer,fixstr = args
    openfile=sep.join(filename.split(sep)[:-1])+sep
    opentxt=" Open: "; lenght=len(opentxt)+2; wrtptr=lenght+len(openfile)
    thr=Thread(target=updscr_thr); run=False; kill=False; thr.start()

    complete=False; cmp_counter=0
    
    while True:
        # If OS is LINUX restore TTY to it default values
        if not sep==chr(92): termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        # Call Screen updater
        mode=(openfile,opentxt,wrtptr,lenght)
        arg=(black,reset,status,banoff,offset,line,\
        wrtptr,arr,banner,filename,rows,columns)
        rows,columns = menu_updsrc(arg,mode,True)
        # If OS is LINUX set TTY to raw mode
        if not sep==chr(92): tty.setraw(fd)

        run=True #Start update screen thread
        key=getch() #Map keys
        run=False #Stop update screen thread

        if key==keys["tab"]:
            try:
                if not (openfile==sep or len(openfile)==0):
                    if not complete: content=glob(openfile+"*",recursive=False)
                    if len(content)>1: complete=True
                    if cmp_counter>=len(content): cmp_counter = 0
                    if complete:
                        openfile=content[cmp_counter]
                        cmp_counter+=1
                    else: openfile=content[0]
            except: pass

        elif complete and key==keys['return']:
            wrtptr=len(openfile)+len(opentxt)+2
            complete=False
        
        elif key==keys["ctrl+o"]:
            try:
                openfile=glob(openfile, recursive=False)[0]
                for i in open(openfile, "r", encoding="UTF-8").readlines():
                    if '\x00' in i: raise ValueError
                tmp=open(openfile, "r", encoding="UTF-8").readlines(); arr=[]
                for x in tmp: arr.append(x.replace("\r","").replace("\n","").replace("\f",""))
                arr.append(""); filename=openfile
                exit(); status_st=False
                pointer=offset=0; line=1
                break
            except: pass
            
        elif key==keys["ctrl+q"]: exit(); break
    
        elif key==keys["delete"]:
            if not wrtptr==lenght:
                if complete:
                    openfile=openfile.split(sep)[:-1]
                    openfile=sep.join(openfile)+sep
                    wrtptr-=len(openfile[-1])-1
                    complete=False
                else: 
                    p1=list(openfile)
                    p1.pop(wrtptr-lenght-1)
                    openfile="".join(p1)
                    wrtptr-=1

        elif key==keys["special"]:
            if not sep==chr(92): special_key=getch()
            arrow=getch()
            if arrow==keys["arr_left"]:
                if not wrtptr==lenght:
                    wrtptr-=1
            elif arrow==keys["arr_right"]:
                if not wrtptr>len(openfile)+lenght-1:
                    wrtptr+=1
            elif arrow==keys["supr"]:
                if not wrtptr==lenght:
                    if complete:
                        openfile=openfile.split(sep)[:-1]
                        openfile=sep.join(openfile)+sep
                        wrtptr-=len(openfile[-1])-1
                        complete=False
                    else: 
                        p1=list(openfile)
                        p1.pop(wrtptr-lenght)
                        openfile="".join(p1)
        
            elif arrow==keys["start"]:
                wrtptr=lenght
                
            elif arrow==keys["end"]:
                wrtptr=len(openfile)+lenght
             
        elif key==keys["return"]: pass
        
        elif key==keys["ctrl+n"]:
            arr=[""]; text=""
            pointer=1; offset=0; line=1
            filename=getcwd()+sep+"NewFile"
            exit(); break
        
        else: #Rest of keys
            cond1=wrtptr<((columns+2)*rows+1)
            cond2=str(key)[4:6] in fixstr
            if cond1 and not cond2:
                out=decode(key,getch)
                p1=openfile[:wrtptr-lenght]
                p2=openfile[wrtptr-lenght:]
                openfile=p1+out+p2
                wrtptr+=1
                complete=False
    
    return arr,filename,status_st,pointer,line,offset
