# Code by Sergio00166

from scr_funcs import *
from sys import stdout
from os import sep


# Some ANSII ctrl codes
movcr = "\r\033[%d;%dH"
cls = movcr % (1, 1)
scr = "\r\x1b[?25h"
hcr = "\r\x1b[?25l"

def print(text):
    stdout.write(text)
    stdout.flush()


def text_selection(
    all_file, select, rows, banoff, line, black, slc, reset, columns
):
    # Get values from the select list
    start, end, out = select[0][0], select[1][0], []
    # Fix position for the end
    if line < rows + banoff:
        end += select[1][1] - select[0][1]
    start -= select[1][1] - select[0][1]
    # Fix start value
    if start < 0:
        start = 0
    # Get the text that is upper the selected region
    p0 = all_file[:start]
    # Get the text that is below the selected region
    p2 = all_file[end:]
    # Get the text that is selected
    p1 = all_file[start:end]
    # Get the len of the higligh ascii code
    lenght = len(black + "*" + reset)

    for x in p1:
        lenght = str_len(rscp(x, [black, reset], True))
        # Rehighlight ASCII ctrl chars (visual)
        x = rscp(x, [black, reset, slc])
        # Checks if the line rendered continues to the right
        if x.endswith(black + ">" + reset):
            x = x[:-lenght] + reset + ">" + black
        # Checks if the line rendered continues to the left
        elif x.startswith(black + "<" + reset):
            x = x[:-lenght] + reset + "<" + black
        # Add it to list and fill with spaces
        out.append(black + x + reset + (" " * (columns - lenght + 2)))

    # Expand all lines to fill the screen with empty spaces
    p0 = [
        x + ("\u00A0" * (columns - str_len(rscp(x, [black, reset], True)) + 2))
        for x in p0
    ]
    p2 = [
        x + ("\u00A0" * (columns - str_len(rscp(x, [black, reset], True)) + 2))
        for x in p2
    ]
    return p0 + out + p2


def update_scr(
    black,bnc,slc,reset,status,
    banoff,offset,line,cursor,
    arr,banner,filename,rows,
    columns,status_st,rrw=False,
    select=[],hlg_str="",
):
    # Create the string that represents on which line we are
    position = " " + str(line + offset - banoff) + "  "
    # Create a part of the banner (position and status strings)
    status = " " + banner[1] if not status_st else "  " + status
    outb = position + " " + banner[0] + status + "    "
    # Check if the space for the filename is too small
    lenght = columns - len(outb)
    small = lenght < 24
    if small:
        outb, fix, lenght = "", 1, columns
    # Fix the filename string to fit in the space
    filename = fixfilename(filename, lenght)
    # Use the fucking UNIX path separator
    filename = filename.replace(sep, "/")
    # Calculate blank space of necessary
    if small:
        filename += " " * (columns - len(filename))
    # Get the separation between the Left and the filename
    if not small:
        fix = columns - len(outb) - len(filename) + 1
    # Get the text that will be on screen and update the cursor value
    arr, cursor = scr_arr2str(
        arr, line, offset, cursor, black, reset, columns, rows, banoff
    )
    # Initialize the menu with all the banner
    menu = cls + bnc + outb + " " * fix
    # Hightligh the selected text
    if len(select) > 0:
        arr = text_selection(
            arr, select, rows, banoff, line, black, slc, reset, columns
        )
    # Expand all lines to fill the screen with empty spaces
    else:
        arr = [
            x + ("\u00A0" * (columns - str_len(rscp(x, [black, reset], True)) + 2))
            for x in arr
        ]
    # Add empty lines to fill the height
    if not len(arr)-1 == rows - banoff:
        arr += ["\u00A0" * (columns + 2)] * (rows - len(arr) + 1)
    # Create an string out of the arr
    all_file = "\n".join(arr)
    # This is for the find str function page
    if hlg_str != "":
        all_file = all_file.replace(hlg_str, black + hlg_str + reset)
    # Now concatenate all to create the screen
    menu += filename + " " + reset + "\n" + all_file
    # If raw mode is specified return the screen string
    if rrw:
        return menu
    else:
        mv = movcr % (line + banoff, cursor)
        print(hcr + menu + scr + mv)
        # If we are using this in the find
        # function return the relative cursor
        if hlg_str != "":
            return cursor


def menu_updsrc(arg, mode=None, updo=False):
    (  # Extract args
        black,bnc,slc,reset,status,
        banoff,offset,line,cursor,
        arr,banner,filename,
        rows,columns,status_st,
    ) = arg
    # Save old vars and get new values
    old_rows = rows
    old_columns = columns
    rows, columns = get_size()
    # Check if terminal is too small
    if rows < 4 or columns < 24:
        print("\r\033cTerminal too small")
    # Compare the old values with the new ones
    elif not (old_rows == rows and old_columns == columns) or updo:
        if not updo:
            print("\r\033[3J")  # Clear previous content
        if not mode == None or updo:
            # Set some vars
            filetext, opentxt, wrtptr, lenght = mode
            out = opentxt + filetext
            try: # Get raw screen updated
                menu = update_scr(
                    black, bnc, slc, reset, status,
                    banoff, offset, line, 0, arr,
                    banner, filename, rows,
                    columns, status_st, True,
                )
            except: return rows,columns
            # Cut menu to add the menu bar
            menu = "\n".join(menu.split("\n")[: rows + banoff])
            # Calculate relative cursor pos
            wrtptr, out = fix_cursor_pos(
                out, wrtptr - 1, columns, slc, reset + bnc
            )
            # Add blank spaces to shade it
            ln = str_len(rscp(out, [slc, reset + bnc], True))
            out += " " * (columns - ln + 2)
            # Print the whole screen and move cursor
            menu = hcr + menu + bnc + out + scr
            print(menu + movcr % (rows + 2, wrtptr))
    return rows,columns

