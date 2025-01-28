# Code by Sergio00166

from functions1 import decode, get_size, read_UTF8, taborspace
from upd_scr import menu_updsrc
from time import sleep as delay
from threading import Thread
from os import getcwd,sep
from glob import glob


if not sep==chr(92): #If OS is LINUX
    #Get default values for TTY
    from termios import TCSADRAIN,tcsetattr,tcgetattr
    from sys import stdin; from tty import setraw
    fd = stdin.fileno(); old_settings = tcgetattr(fd)

def updscr_thr():
    global opentxt,openfile,rows,columns,black,reset,status,banoff
    global lenght,wrtptr,offset,line,arr,banner,filename,rows,columns
    global run, kill, fd, old_settings, status_st, bnc, slc
    
    while not kill:
        delay(0.01)
        if run:
            # If OS is LINUX restore TTY to it default values
            if not sep==chr(92):
                old=(fd,TCSADRAIN,old_settings)
                tcsetattr(fd, TCSADRAIN, old_settings)
            # Call Screen updater
            mode=(openfile,opentxt,wrtptr,lenght)
            arg=(black,bnc,slc,reset,status,banoff,offset,line,\
            wrtptr,arr,banner,filename,rows,columns,status_st)
            rows,columns = menu_updsrc(arg,mode)
            # If OS is LINUX set TTY to raw mode
            if not sep==chr(92): setraw(fd,when=TCSADRAIN)

def exit():
    global fd, old_settings, run, kill, thr
    run=False; kill=True; thr.join()
    if not sep == chr(92): tcsetattr(fd,TCSADRAIN,old_settings)


def open_file(arg):
    global opentxt,openfile,rows,columns,black,reset,status,banoff
    global lenght,wrtptr,offset,line,arr,banner,filename,rows,columns
    global run, kill, fd, old_settings, thr, status_st, bnc, slc

    filename,black,bnc,slc,reset,rows,banoff,arr,columns,status,offset,line,\
    banner,status_st,keys,cursor,oldptr,select,read_key,codec,lnsep,indent = arg

    openfile = "/".join(filename.split("/")[:-1])+"/"
    opentxt=" Open: "; lenght=len(opentxt)+2
    wrtptr=lenght+len(openfile)
    thr=Thread(target=updscr_thr)
    run,kill = False,False
    thr.daemon = True; thr.start()
    complete=False; cmp_counter=0
    
    while True:
        # Fix when the cursor is out
        if len(openfile)<wrtptr-lenght:
            wrtptr = len(openfile)+lenght
        try:
            # Force use LINUX dir separator
            openfile=openfile.replace(chr(92),"/")
            # If OS is LINUX restore TTY to it default values
            if not sep==chr(92):
                old=(fd,TCSADRAIN,old_settings)
                tcsetattr(fd, TCSADRAIN, old_settings)
            # Call Screen updater
            mode=(openfile,opentxt,wrtptr,lenght)
            arg=(black,bnc,slc,reset,status,banoff,offset,line,\
            wrtptr,arr,banner,filename,rows,columns,status_st)
            rows,columns = menu_updsrc(arg,mode,True)
            # If OS is LINUX set TTY to raw mode
            if not sep==chr(92): setraw(fd,when=TCSADRAIN)
            
            run=True #Start update screen thread
            key=read_key() #Map keys
            run=False #Stop update screen thread

            # Reset error message
            if status=="ERROR": status_st = False
            
            if key==keys["tab"]:
                if not (len(openfile)==0 or (sep==chr(92) and not ":/" in openfile)):
                    if not complete: content=glob(openfile+"*",recursive=False)
                    if len(content)>0: complete=True
                    if cmp_counter>=len(content): cmp_counter = 0
                    if complete:
                        openfile=content[cmp_counter]
                        cmp_counter+=1
                    else: openfile=content[0]

            elif complete and key==keys['return']:
                wrtptr=len(openfile)+len(opentxt)+2
                complete=False

            elif key==keys["return"]: pass
            
            elif key==keys["ctrl+o"]:
                openfile=glob(openfile, recursive=False)[0]
                arr,codec,lnsep = read_UTF8(openfile)
                filename,status_st = openfile,False
                cursor,offset,oldptr,line,select = 1,0,1,1,[]
                indent = taborspace(arr)
                break
                
            elif key==keys["ctrl+c"]: break
        
            elif key==keys["delete"]:
                if not wrtptr==lenght:
                    if complete:
                        openfile=openfile.split("/")[:-1]
                        openfile="/".join(openfile)+"/"
                        wrtptr-=len(openfile[-1])-1
                        complete=False
                    else: 
                        p1=list(openfile)
                        p1.pop(wrtptr-lenght-1)
                        openfile="".join(p1)
                        wrtptr-=1

            elif key==keys["arr_left"]:
                if not wrtptr==lenght: wrtptr-=1
                
            elif key==keys["arr_right"]:
                if not wrtptr>len(openfile)+lenght-1: wrtptr+=1
                    
            elif key==keys["supr"]:
                if complete:
                    openfile=openfile.split("/")[:-1]
                    openfile="/".join(openfile)+"/"
                    wrtptr-=len(openfile[-1])-1
                    complete=False
                else:
                    p1=list(openfile)
                    p1.pop(wrtptr-lenght)
                    openfile="".join(p1)

            elif key in keys["start"]: wrtptr=lenght
                
            elif key in keys["end"]: wrtptr=len(openfile)+lenght
            
            elif key==keys["ctrl+n"]:
                cursor,oldptr,offset,line = 1,1,0,1
                arr,select,status_st = [""],[],False
                filename=getcwd()+"/NewFile"
                break
  
            else: #Rest of keys
                if wrtptr<((columns+2)*rows+1):
                    out=decode(key)
                    p1=openfile[:wrtptr-lenght]
                    p2=openfile[wrtptr-lenght:]
                    openfile=p1+out+p2
                    wrtptr+=len(out)
                    complete=False

        except OSError: status,status_st = "ERROR",True
        except: pass

    exit() # Reset
    # Fix when current dir is root
    if filename.startswith("//"): filename = filename[1:]
    return arr,filename,status_st,cursor,oldptr,line,offset,select,codec,lnsep,indent
