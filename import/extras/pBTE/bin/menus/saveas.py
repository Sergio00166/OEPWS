# Code by Sergio00166

from functions1 import decode,get_size,read_UTF8,write_UTF8
from upd_scr import menu_updsrc
from time import sleep as delay
from threading import Thread
from glob import glob
from os import sep


if not sep==chr(92): #If OS is LINUX
    #Get default values for TTY
    from termios import TCSADRAIN,tcsetattr,tcgetattr
    from sys import stdin; from tty import setraw
    fd = stdin.fileno(); old_settings = tcgetattr(fd)

def updscr_thr():
    global saveastxt,filewrite,rows,columns,black,reset,status,banoff
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
            mode=(filewrite,saveastxt,wrtptr,lenght)
            arg=(black,bnc,slc,reset,status,banoff,offset,line,\
            wrtptr,arr,banner,filename,rows,columns,status_st)
            rows,columns = menu_updsrc(arg,mode)
            # If OS is LINUX set TTY to raw mode
            if not sep==chr(92): setraw(fd,when=TCSADRAIN)


def exit():
    global fd, old_settings, run, kill, thr
    run=False; kill=True; thr.join()
    if not sep == chr(92): tcsetattr(fd,TCSADRAIN,old_settings)


def save_as(arg):
    global saveastxt,filewrite,rows,columns,black,reset,status,banoff
    global lenght,wrtptr,offset,line,arr,banner,filename,rows,columns
    global run, kill, fd, thr, old_settings, status_st, bnc, slc

    filename,black,bnc,slc,reset,rows,banoff,arr,columns,status,offset,\
    line,banner,status_st,keys,read_key,codec,lnsep = arg

    saveastxt=" Save as: "; lenght=len(saveastxt)+2
    filewrite=filename; wrtptr=lenght+len(filewrite)
    thr=Thread(target=updscr_thr)
    run,kill,complete = False,False,False
    thr.daemon=True; thr.start()
    cmp_counter = 0
    
    while True:
        # Fix when the cursor is out
        if len(filewrite)<wrtptr-lenght:
            wrtptr = len(filewrite)+lenght
        try:
            # Force use LINUX dir separator
            filewrite=filewrite.replace(chr(92),"/")
            # If OS is LINUX restore TTY to it default values
            if not sep==chr(92):
                old=(fd,TCSADRAIN,old_settings)
                tcsetattr(fd, TCSADRAIN, old_settings)
            # Call Screen updater
            mode=(filewrite,saveastxt,wrtptr,lenght)
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
                if not (len(filewrite)==0 or (sep==chr(92) and not ":/" in filewrite)):
                    if not complete: content=glob(filewrite+"*",recursive=False)
                    if len(content)>0: complete=True
                    if cmp_counter>=len(content): cmp_counter = 0
                    if complete:
                        filewrite=content[cmp_counter]
                        cmp_counter+=1
                    else: filewrite=content[0]

            elif complete and key==keys["return"]:
                wrtptr=len(filewrite)+len(saveastxt)+2
                complete=False
            
            #Ctrl + S (confirms) or Ctrl + B backup
            elif key==keys["ctrl+s"] or key==keys["ctrl+b"]:
                old_filewrite = filewrite
                try:
                    if key==keys["ctrl+b"] and filewrite==filename: filewrite+=".bak"
                    write_UTF8(filewrite,codec,lnsep,arr)
                    if key==keys["ctrl+b"]: status="BCKPd"
                    else: status,filename = "SAVED",filewrite
                    status_st=True; break # Exit the menu
                except:
                    filewrite = old_filewrite
                    raise OSError
                
                
            elif key==keys["ctrl+c"]: break
        
            elif key==keys["delete"]:
                if not wrtptr==lenght:
                    if complete:
                        filewrite=filewrite.split("/")[:-1]
                        filewrite="/".join(filewrite)+"/"
                        wrtptr-=len(filewrite[-1])-1
                        complete=False
                    else: 
                        p1=list(filewrite)
                        p1.pop(wrtptr-lenght-1)
                        filewrite="".join(p1)
                        wrtptr-=1

            elif key==keys["arr_left"]:
                if not wrtptr==lenght: wrtptr-=1
                
            elif key==keys["arr_right"]:
                if not wrtptr>len(filewrite)+lenght-1: wrtptr+=1
                
            elif key==keys["supr"]:
                if complete:
                    filewrite="/".join(filewrite.split("/")[:-1])+"/"
                    wrtptr-=len(filewrite[-1])-1
                    complete=False
                else: 
                    p1=list(filewrite)
                    p1.pop(wrtptr-lenght)
                    filewrite="".join(p1)                   

            elif key in keys["start"]: wrtptr=lenght
                
            elif key in keys["end"]: wrtptr=len(filewrite)+lenght
         
            elif key==keys["return"]: pass

            elif key==keys["ctrl+p"] or key==keys["ctrl+a"]:
                tmp,codec,lnsep = read_UTF8(filewrite)
                if key==keys["ctrl+a"]: output=list(arr+tmp)
                elif key==keys["ctrl+p"]: output=list(tmp+arr)
                write_UTF8(filewrite,codec,lnsep,output)
                status,status_st = bnc+"ADDED",True
                break
            
            else: #Rest of keys
                if wrtptr<((columns+2)*rows+1):
                    out=decode(key)
                    p1=filewrite[:wrtptr-lenght]
                    p2=filewrite[wrtptr-lenght:]
                    filewrite=p1+out+p2
                    wrtptr+=len(out)

        except OSError: status,status_st = "ERROR",True
        except: pass
        
    exit() # Reset
    # Fix when current dir is root
    if filename.startswith("//"): filename = filename[1:]
    return status_st, filename, status, codec, lnsep
