#Code by Sergio1260

from os import get_terminal_size,sep
from sys import path
path.append(path[0]+sep+"lib.zip")
from wcwidth import wcwidth


def wrap(text, columns):
    text=text.expandtabs(8)
    out=[]; counter=-1; buffer=""
    for x in text:
        if counter>=columns-1:
            lenght=str_len(x)
            if lenght>1: ext=buffer; buffer=x
            else: ext=buffer+x; buffer=""    
            out.append(ext); counter=0
        else: buffer+=x; counter+=str_len(x)
    if not buffer=="": out.append(buffer)
    return out

def get_size():
    size=get_terminal_size()
    return size[1]-3,size[0]-2

def decode(key,getch):
    for x in range(3):
        try: out=key.decode("UTF-8"); break
        except: key+=getch()
    return out

def fix_arr_line_len(arr, columns, black, reset):
    out=[]; fix=0//(columns+2)
    for text in arr:
        wrapped_text = wrap(text,columns)
        if len(wrapped_text)==0: wrapped_text=""
        elif fix==len(wrapped_text):
            text=wrapped_text[fix-1]
        else: text=wrapped_text[fix]
        if (len(wrapped_text)-fix)>1:
            text+=black+">"+reset
        out.append(text)   
    return out

def str_len(text,pointer=None):
    lenght=0
    if not pointer==None:
        fix=text[:pointer-1]
    else: fix=text
    fix=fix.expandtabs(8)
    for x in fix: lenght+=wcwidth(x)
    return lenght

def fixlenline(text, pointer, oldptr):
    length=len(text)+1
    if pointer>length or oldptr>length:
        return length,oldptr
    elif oldptr>pointer: return oldptr,oldptr
    else: return pointer,oldptr

def CalcRelLine(p1,arr,offset,line,banoff,rows):
    if p1=="-": p1=len(arr)-1
    try:
        p1=int(p1)
        if p1<len(arr):
            if p1<rows: offset=0; line=p1+banoff
            else: offset=p1-rows; line=rows+banoff
    except: pass
    text=arr[line+offset-banoff]
    return line, offset, text

def fix_cursor_pos(text,pointer,columns,black,reset):
    len_arr=[]; ptr=pointer; pos=0
    pointer=str_len(text,pointer)   
    wrapped_text = wrap(text,columns)  
    for x in wrapped_text:
        if pointer-str_len(x)<1: break
        else: pos+=1
        pointer-=str_len(x)
    if pos>0: pointer+=1
    if not len(wrapped_text)==0:
        text=wrapped_text[pos]
        if pos>0:
            text=black+"<"+reset+text
            if not pos==len(wrapped_text)-1:
                text+=black+">"+reset
        elif len(wrapped_text)>1:
            text+=black+">"+reset      
    else: text=""
                
    return pointer+1, text

def fixfilename(filename, columns):
    if len(filename)+32>columns: #If filename overflows
        flfix=filename.split(sep)
        filename=flfix[len(flfix)-1]
        if len(filename)+31>columns: #If still not fiting
            middle = len(filename) // 2
            filename=filename[:middle-1]+'*'+filename[middle+2:]
            if len(filename)+31>columns:
                filename=filename[:columns-32]+"*"
    return filename

def scr_arr2str(arr,line,offset,pointer,black,reset,columns,rows,banoff):
    text=arr[line+offset-banoff]; uptr=pointer
    pointer, text = fix_cursor_pos(text,pointer,columns,black,reset)
    arr=arr[offset : rows+offset+1]
    arr = fix_arr_line_len(arr,columns,black,reset)
    arr[line-1]=text; out_arr=[]
    for x in arr:
        ln=str_len(x)
        if uptr>(columns+2) and arr.index(x)==line-1: ln-=12
        if ln<(columns+2): x=x+(" "*(columns-ln+2))
        out_arr.append(x)
    if not len(arr)==rows:
        out_arr+=[" "*(columns+2)]*(rows-len(arr)+1)
    
    return "\n".join(out_arr).expandtabs(8), pointer

    
    
