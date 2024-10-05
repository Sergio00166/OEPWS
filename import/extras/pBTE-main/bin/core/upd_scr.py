# Code by Sergio00166

from functions import scr_arr2str,rscp,sscp,str_len,fix_cursor_pos
from functions1 import get_size, fixfilename
from sys import stdout
from os import sep


# Some ANSII ctrl codes
movcr = "\r\033[%d;%dH"
cls = "\r\033[3J"
cls += movcr%(1,1)
scr = "\r\x1b[?25h"
hcr = "\r\x1b[?25l"

def print(text):
    stdout.write(text)
    stdout.flush()

def update_scr(black,bnc,slc,reset,status,banoff,offset,line,cursor,arr,banner,\
               filename,rows,columns,status_st,rrw=False,select=[],hlg_str=""):
    # Create the string that represents on which line we are
    position=" "+str(line+offset-banoff)+"  "
    # Create a part of the banner (position and status strings)
    status= (" "+banner[1] if not status_st else "  "+status)
    outb=position+" "+banner[0]+status+"    "
    # Check if the space for the filename is too small
    length = columns-len(outb); small = length<24
    if small: outb,fix,length = "",1,columns
    # Fix the filename string to fit in the space
    filename = fixfilename(filename,length)
    # Use the fucking UNIX path separator
    filename = filename.replace(sep,"/")
    # Calculate blank space of necessary
    if small: filename+=" "*(columns-len(filename))
    # Get the separation between the Left and the filename
    if not small: fix=columns-len(outb)-len(filename)+1
    # Get the text that will be on screen and update the cursor value
    all_file,cursor = scr_arr2str(arr,line,offset,cursor,black,reset,columns,rows,banoff)
    # This is for the find str function page
    if hlg_str!="": all_file = all_file.replace(hlg_str,black+hlg_str+reset) 
    # Initialize the menu with all the banner
    menu=cls+bnc+outb+" "*fix
    # Highlight selector
    if len(select)>0:
        # Get values from the select list
        start=select[0][0]; end=select[1][0]
        if line < rows+banoff:
            end+=select[1][1]-select[0][1]
        start-=select[1][1]-select[0][1]
        # Fix start value
        if start<0: start=0
        # Split lines
        all_file=all_file.split("\n")
        # Get the text that is upper the selected region
        p0="\n".join(all_file[:start])
        # Get the text that is below the selected region
        p2="\n".join(all_file[end:])
        # Get the text that is selected
        p1=all_file[start:end]; out=[]
        # Get the len of the higligh ascii code
        length=len(black+"*"+reset)
        # For each line of p1
        for x in p1:
            x=rscp(x,[black,reset,slc])
            # Checks if the line rendered continues to the right
            # (having the flag that marks that)
            if x.endswith(black+">"+reset):
                out.append(x[:-length]+reset+">"+black)
            # Checks if the line rendered continues to the left
            # (having the flag that marks that)
            elif x.startswith(black+"<"+reset):
                out.append(x[:-length]+reset+"<"+black)
            # If none of the above simply add is to out dic
            else: out.append(x)
        # Create a string from the list
        p1="\n".join(out)
        # Now create the all file string. Adding the
        # ascii chars to p1 (the selected string)
        all_file=p0+black+p1+reset+p2
    # Now concatenate all to create the screen
    menu+=filename+" "+reset+"\n"+all_file
    # If raw mode is specified return the screen string
    if rrw: return menu
    else:
        # if not add the ansii code firstly to unshow
        # the tty cursor, then move the cursor to the
        # desired line, the show the cursor and move
        # it horizontally and then print to stdout
        line += banoff
        menu += movcr%(line,1)+scr
        menu += movcr%(line,cursor)
        print(hcr+menu)
        # If we are using this in the find
        # function return the relative cursor
        if hlg_str!="": return cursor


def menu_updsrc(arg,mode=None,updo=False):
    # Extract args
    black,bnc,slc,reset,status,banoff,offset,line,cursor,\
    arr,banner,filename,rows,columns,status_st = arg
    # Save old vars and get new values
    old_rows=rows; old_columns=columns
    rows,columns=get_size()
    # Check if terminal is too small
    if rows<4 or columns<24: print("\r\033cTerminal too small")
    # Compare the old values with the new ones
    elif not (old_rows==rows and old_columns==columns) or updo:
        if not updo: print("\r\033[3J") # Clear previous content
        if not mode==None or updo:
            # Set some vars
            filetext,opentxt,wrtptr,length = mode
            out=opentxt+filetext
            # Get raw screen updated
            menu = update_scr(black,bnc,slc,reset,status,banoff,offset,\
            line,0,arr,banner,filename,rows,columns,status_st,True)
            # Cut menu to add the menu bar
            menu = "\n".join(menu.split("\n")[:rows+banoff])
            # Calculate relative cursor pos
            wrtptr,out = fix_cursor_pos(out,wrtptr-1,columns,slc,reset+bnc)
            # Add blank spaces to shade it
            ln=str_len(rscp(out,[slc,reset+bnc],True))
            out += " "*(columns-ln+2)
            # Print the whole screen and move cursor
            menu = hcr+menu+bnc+out+scr
            print(menu+movcr%(rows+2,wrtptr))
    return rows,columns
