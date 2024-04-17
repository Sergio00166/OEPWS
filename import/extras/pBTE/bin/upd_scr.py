# Code by Sergio1260

from functions import get_size, fixfilename, scr_arr2str


def update_scr(black,reset,status,banoff,offset,line,pointer,arr,banner,filename,rows,columns,rrw=False,select=[]):
    # Create the string that represents on which line we are
    position=black+"  "+str(line+offset-banoff)+" "*(4-len(str(line+offset-banoff)))
    # Create a part of the banner (position and status strings)
    outb=position+black+" "+reset+status+banner+black+"    "+reset
    # Now set the filenamevar with the fixed filename string and
    # sets the cls var with the clear screen scape code
    filename = fixfilename(filename, columns); cls="\r\033[%d;%dH"%(1, 1)
    # Get the text that will be on screen and update the pointer value
    all_file,pointer = scr_arr2str(arr,line,offset,pointer,black,reset,columns,rows,banoff)
    # Initialize the menu with all the banner
    menu=cls+outb+black+" "*(columns-31-len(filename))

    # Highlight selector
    if len(select)>0:
        # Get values from the select list
        start=select[0][0]; end=select[1][0]
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
        lenght=len(black+"*"+reset)
        # For each line of p1
        for x in p1:
            # Checks if the line rendered continues to the right
            # (having the flag that marks that)
            if x.endswith(black+">"+reset):
                out.append(x[:-lenght]+reset+">"+black)
            # Checks if the line rendered continues to the left
            # (having the flag that marks that)
            elif x.startswith(black+"<"+reset):
                out.append(x[:-lenght]+reset+"<"+black)
            # If none of the above simply add is to out dic
            else: out.append(x)
        # Create a string from the list
        p1="\n".join(out)
        # Now create the all file string. Adding the
        # ascii chars to p1 (the selected string)
        all_file=p0+black+p1+reset+p2
    # Add to the screen string the rest of the screen
    menu+=filename+" "+reset+"\n"+all_file
    # If raw mode is specified return the screen string
    if rrw: return menu
    else:
        # if not add the ansii code to move the
        # cursor where it is stored in line and
        # pointer vars and prints it
        menu+=("\r\033[%d;%dH"%(line+1, pointer))
        print(menu, end="")


def menu_updsrc(arg,mode=None,updo=False):
    # Extract args
    black,reset,status,banoff,offset,line,\
    pointer,arr,banner,filename,rows,columns=arg
    # Save old vars and get new values
    old_rows=rows; old_columns=columns
    rows,columns=get_size()
    # Check if terminal is too small
    if rows<4: print("\r\033cTerminal too small")
    # Compare the old values with the new ones
    elif not (old_rows==rows and old_columns==columns) or updo:
        if not updo: print("\r\033c",end="")
        if not mode==None or updo:
            # Set vars
            filetext,opentxt,wrtptr,lenght = mode
            out=opentxt+filetext
            # Calculate in what line it is
            fix=len(out)//(columns+2)
            # Calculate blank spaces
            full=((columns+2)*(fix+1))-len(out)
            # Get raw screen updated
            menu = update_scr(black,reset,status,banoff,\
            offset,line,0,arr,banner,filename,rows,columns,True)
            # Cut menu to add the menu bar
            menu = "\n".join(menu.split("\n")[:rows+banoff+1-fix])
            # Add menu to it
            menu+="\n"+black+out+(" "*(full))
            # Calculate pointer y displacement
            fix_lip = rows+banoff+2-fix+((wrtptr-1)//(columns+2))
            # Calculate pointer x displacement
            fix_wrtptr = (columns+2)*fix
            # Some pointer x displacement fix
            while True:
                if wrtptr-1-fix_wrtptr<0:
                    fix-=1; fix_wrtptr=(columns+2)*fix
                else: break
            # Add scape secuence to move cursor
            menu+="\r\033[%d;%dH"%(fix_lip, wrtptr-1-fix_wrtptr)
            # Print the whole screen
            print(menu, end="")
            
    return rows,columns
