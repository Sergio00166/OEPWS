# Code by Sergio00166

from functions1 import decode, get_size, read_UTF8
from upd_scr import menu_updsrc
from threading import Thread
from os import sep
from time import sleep as delay
from glob import glob

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
    print(reset+"\r\033c", end="")


def save_as(arg):
    global saveastxt,filewrite,rows,columns,black,reset,status,banoff
    global lenght,wrtptr,offset,line,arr,banner,filename,rows,columns
    global run, kill, fd, thr, old_settings, status_st, bnc, slc

    filename,black,bnc,slc,reset,rows,banoff,arr,columns,status,offset,\
    line,banner,status_st,saved_txt,keys,read_key,codec,lnsep = arg

    saveastxt=" Save as: "; lenght=len(saveastxt)+2
    filewrite=filename; wrtptr=lenght+len(filewrite)
    thr=Thread(target=updscr_thr); run=False
    kill=False; thr.start(); complete=False; cmp_counter=0
    
    while True:
        # Fix when the pointer is out
        if len(filewrite)<wrtptr-lenght:
            wrtptr = len(filewrite)+lenght
        try:
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

            if key==keys["tab"]:
                if not (len(openfile)==0 or (sep==chr(92) and not ":" in openfile)):
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
            
            #Ctrl + A (confirms) or Ctrl + B backup
            elif key==keys["ctrl+s"] or key==keys["ctrl+b"]:
                if key==keys["ctrl+b"] and filewrite==filename: filewrite+=".bak"
                out=open(filewrite,"w",encoding=codec,newline='')
                out.write(lnsep.join(arr)); out.close(); status_st=True
                if key==keys["ctrl+b"]: status=bnc+"BCKPd"
                else: status,filename = saved_txt,filewrite
                exit(); break
                
            elif key==keys["ctrl+c"]: exit(); break
        
            elif key==keys["delete"]:
                if not wrtptr==lenght:
                    if complete:
                        filewrite=filewrite.split(sep)[:-1]
                        filewrite=sep.join(filewrite)+sep
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
                if not wrtptr>len(filewrite)+lenght-1:  wrtptr+=1
                
            elif key==keys["supr"]:
                if not sep==chr(92): getch()
                if complete:
                    filewrite=sep.join(filewrite.split(sep)[:-1])+sep
                    wrtptr-=len(filewrite[-1])-1
                    complete=False
                else: 
                    p1=list(filewrite)
                    p1.pop(wrtptr-lenght)
                    filewrite="".join(p1)                   

            elif key==keys["start"]: wrtptr=lenght
                
            elif key==keys["end"]: wrtptr=len(filewrite)+lenght
         
            elif key==keys["return"]: pass

            elif key==keys["ctrl+p"] or key==keys["ctrl+a"]:
                tmp,codec,lnsep = read_UTF8(filewrite)
                if key==keys["ctrl+a"]: output=list(arr+tmp)
                elif key==keys["ctrl+p"]: output=list(tmp+arr)
                out=open(filewrite,"w",encoding=codec,newline='')
                out.write(lnsep.join(output)); out.close()
                status,status_st = bnc+"ADDED",True
                exit(); break
            
            else: #Rest of keys
                if wrtptr<((columns+2)*rows+1):
                    out=decode(key)
                    p1=filewrite[:wrtptr-lenght]
                    p2=filewrite[wrtptr-lenght:]
                    filewrite=p1+out+p2
                    wrtptr+=len(out)
        except: pass

    return status_st, filename, status, codec, lnsep
