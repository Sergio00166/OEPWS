#Code by Sergio1260


def updscr_thr():
    global black,reset,status,banoff,offset,line,pointer
    global banner,filename,rows,columns,run_thread,text
    global kill,p_offset,arr,select
    
    if not sep==chr(92): #If OS is LINUX
        #Get default values for TTY
        import sys; import termios; import tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
    while not kill:
        delay(0.01)
        if run_thread:
            # Save old vars and get new values
            old_rows=rows; old_columns=columns
            rows,columns=get_size()
            # Check if terminal is too small
            if rows<4 or columns<34: print("\r\033cTerminal too small")
            # Compare the old values with the new ones
            elif not (old_rows==rows and old_columns==columns):
                # Increment the offset if line is geeter than rows
                if line>rows: offset=offset+(line-rows); line=rows	
                # Call screen updater function
                print("\r\033c",end="") #Clear screen
                # If OS is LINUX restore TTY to it default values
                if not sep==chr(92): termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                update_scr(black,reset,status,banoff,offset,line,pointer,arr,banner,filename,rows,columns,status_st,False,select)
                # If OS is LINUX set TTY to raw mode
                if not sep==chr(92): tty.setraw(fd)



if __name__=="__main__":
    
    from sys import path
    from os import sep
    # Add the folder to import from here
    path.append(path[0]+sep+"bin")
    from init import *
    
    # Run the update Thread
    update_thr=Thread(target=updscr_thr)
    run_thread=True; kill=False
    update_thr.start()
    
    while True:
        try:
            # Fix for the pointer variable
            if pointer==0: pointer=1
            # If detected key to quickly (Ctrl + V)
            key_fast=end-start<0.01
            if not key_fast:
                # If status flag is 0 set save text to blank
                if status_st==0: status=saved_df 
                # Get the terminal size
                rows,columns=get_size()
                # Call screen updater function
                update_scr(black,reset,status,banoff,offset,line,pointer,arr,\
                           banner,filename,rows,columns,status_st,False,select)
            if not key_fast: run_thread=True #Start update Thread
            # Set time after reading key from keyboard and stopping the update Thread
            start=time(); key=getch(); end=time(); run_thread=False
            # If key is Ctrl + Q (quit) exit the program and clear the screen
            if key==keys["ctrl+q"]:
                if len(files)>0:
                    filename=files[0]; files=files[1:]; arr=read_UTF8(filename)
                    pointer=1; line=1; offset=0; status_st=False; print("\033c",end="")
                else: kill=True; update_thr.join(); print("\033c",end=""); break    
            else: #Call keys functions (Yeah, its a lot of args and returned values)
                args = (key,pointer,oldptr,line,offset,columns,banoff,arr,rows,\
                        filename,status,status_st,copy_buffer,fixstr,fix,\
                        black,reset,saved_txt,ch_T_SP,banner,getch,keys,select)
                
                pointer,oldptr,line,offset,columns,banoff,arr,rows,\
                filename,status,status_st,copy_buffer,fixstr,fix,\
                ch_T_SP,select = keys_func(*args)
                
        except: pass

