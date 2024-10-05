# Code by Sergio00166

from os import sep
from sys import path
path.append(path[0]+sep+"lib.zip")
from wcwidth import wcwidth
from data import ascii_map,ascii_replaced


# Expands tabulators and splits the text in parts and as
# optional calculates the position and relative cursor
def wrap(text, columns, tabsize=8, cursor=None):
    buffer,counter,col = "", -1, 0
    result,pos,ptr = [], 0, 0
    extra = cursor!=None

    def handle_char(char, char_width):
        nonlocal buffer,counter,col,result,ptr,pos
        if counter + char_width > columns:
            result.append(buffer)
            if ptr-counter>0:
                ptr -= counter
                pos += 1
            buffer, counter = char, char_width
        else:
            buffer += char
            counter += char_width
        col += char_width

    for p,char in enumerate(text):
        if char == '\t':
            space_count = tabsize - (col % tabsize)
            expanded = ' ' * space_count
            if extra and cursor>p: ptr += space_count
            for x in expanded: handle_char(x, 1)
        else:
            char_width = wcwidth(char)
            if char_width<1: char_width=1
            if extra and cursor>p: ptr += char_width
            handle_char(char, char_width)

    if buffer: result.append(buffer)
    return (result,ptr,pos) if extra else (result)


def fix_arr_line_len(arr, columns, black, reset):
    out=[]; fix=0//(columns+2)
    for text in arr:
        text = text[:columns+2]
        wrapped_text = wrap(text,columns)
        if len(wrapped_text)==0: wrapped_text=""
        elif fix==len(wrapped_text):
            text=wrapped_text[fix-1]
        else: text=wrapped_text[fix]
        text=sscp(text,[black,reset])
        if (len(wrapped_text)-fix)>1:
            text+=black+">"+reset
        out.append(text)   
    return out

# Expands tabs and gets real string length
def str_len(self, tabsize=8):
    result,col,length = [],0,0
    for char in self:
        if char == '\t':
            space_count = tabsize - (col % tabsize)
            result.append(' ' * space_count)
            length += space_count
            col += space_count
        else:
            result.append(char)
            char_width = wcwidth(char)
            length += char_width
    return length


def fix_cursor_pos(text,cursor,columns,black,reset):
    text = text[:cursor+columns+2]
    wrapped_text, cursor, pos =\
    wrap(text,columns,cursor=cursor-1)

    if not len(wrapped_text)==0:
        if pos>len(wrapped_text)-1: pos=-1
        text=wrapped_text[pos]
        text=sscp(text,[black,reset])
        if pos>0:
            text=black+"<"+reset+text
            if not pos==len(wrapped_text)-1:
                text+=black+">"+reset
        elif len(wrapped_text)>1:
            text+=black+">"+reset      
    else: text=""
                
    return cursor+1, text


def scr_arr2str(arr,line,offset,cursor,black,reset,columns,rows,banoff):
    uptr=cursor; out_arr=[]; sp=black+"<"+reset
    text = arr[line+offset-banoff]
    cursor, text = fix_cursor_pos(text,cursor,columns,black,reset)
    arr = arr[offset:rows+offset+banoff]
    arr = fix_arr_line_len(arr,columns,black,reset)
    arr[line-banoff] = text

    for x in arr:
        ln=str_len(rscp(x,[black,reset],True))
        out_arr.append(x+(" "*(columns-ln+2)))
    if not len(arr)==rows:
        out_arr+=[" "*(columns+2)]*(rows-len(arr)+1)
    
    return "\n".join(out_arr), cursor


# Replaces ascii control chars to the highlighted visual version
def sscp(arg,color):
    global ascii_map
    b, r = color; ext = []
    for x in arg:
        if ord(x) in ascii_map:
            ext.append(b+ascii_map[ord(x)]+r)
        elif str_len(x)>0: ext.append(x)
        else: ext.append(b+"�"+r)
    return "".join(ext)

# Inverts the highlight (for the highlight selector)
def rscp(arg,color,mode=False):
    global ascii_replaced
    if len(color)==3:
        b,r,c = color
        b1 = r+b
        r1 = r+c
    else:
        b,r = color
        b1,r1 = b,r
    for x in ascii_replaced:
        arg=arg.replace(b+x+r, " " if mode else r1+x+b1)
    return arg
