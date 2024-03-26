#Code by Sergio1260

from functions import *


def supr(pointer,max_len,text,offset,banoff,arr,line,status_st,select):
    if len(select)==0:
        try:
            if not pointer==max_len+1:
                p1=list(text); p1.pop(pointer-1)
                text="".join(p1)
            elif not line+offset==1: #move all to previous line
                seltext=arr[line+offset-banoff+1]
                arr[line+offset-banoff+1]=text+seltext
                arr.pop(line+offset-banoff+1)
                text=text+seltext
        except: pass
        status_st=False
    else: select,arr,text,line,offset = del_sel(select,arr,banoff)
    return text, arr, line, offset, status_st, select

def goto(rows, banoff, line, arr, offset, black, reset):
    print("\r\033[%d;%dH"%(rows+banoff+2,1),end="")
    print(" "+black+"Go to line:"+reset, end=" "); p1=input()
    print("\r\033[%d;%dH"%(line, 1),end="")
    line,offset,text = CalcRelLine(p1,arr,offset,line,banoff,rows)
    print("\033c", end="")
    return line, offset,text 

    
def paste(copy_buffer,arr,line,offset,banoff,pointer,text,status_st):
    if not len(copy_buffer)==0:
        if isinstance(copy_buffer, list):
            p1=arr[:line+offset-banoff]
            p2=arr[line+offset-banoff:]
            arr=p1+copy_buffer+p2
            text=copy_buffer[0]        
        else:
            p1=arr[:line+offset-banoff]; p2=arr[line+offset-banoff+1:]
            fix1=text[:pointer-1]; fix2=text[+pointer-1:]
            out=fix1+copy_buffer+fix2; arr=p1+[out]+p2; text=out
            pointer=len(fix1+copy_buffer)+1; status_st=False
    return pointer,arr,text,status_st,copy_buffer
    
def cut(select,arr,line,offset,banoff,text,status_st,copy_buffer,pointer):
    if not len(select)==0:
        p1=arr[:sum(select[0])]; p2=arr[sum(select[1]):]
        start=sum(select[0])-1
        if start<0: start=0
        copy_buffer=arr[start:sum(select[1])]
        if not start==0: copy_buffer=copy_buffer[1:]
        line=select[0][0]+banoff; offset=select[0][1]
        select = []; arr = p1 + p2
    elif line+offset-banoff==len(arr)-1:
        copy_buffer=text[pointer-1:]
        text=text[:pointer-1]
    else:
        copy_buffer=arr[line+offset-banoff]
        arr.pop(line+offset-banoff)
        text=arr[line+offset-banoff]
    status_st=False

    return copy_buffer,arr,text,line,offset,select

def repag(line,offset,banoff,rows,arr,sep,pointer,oldptr):
    p1=line+offset-banoff-rows
    if p1<0: p1=0
    line, offset, text =\
    CalcRelLine(p1,arr,offset,line,banoff,rows)
    if not sep==chr(92): getch()
    pointer,oldptr = fixlenline(text,pointer,oldptr)
    return line, offset, text, pointer, oldptr

def avpag(line,offset,banoff,rows,arr,sep,pointer,oldptr):
    p1=line+offset-banoff+rows
    if p1>=len(arr): p1="-"
    line, offset, text =\
    CalcRelLine(p1,arr,offset,line,banoff,rows)
    if not sep==chr(92): getch()
    pointer,oldptr = fixlenline(text,pointer,oldptr)
    return line, offset, text, pointer, oldptr

def copy(select,arr,line,offset,banoff,pointer):
    if not len(select)==0:
        start=sum(select[0])-1
        if start<0: start=0
        copy_buffer=arr[start:sum(select[1])]
        if not start==0: copy_buffer=copy_buffer[1:]
    else: copy_buffer=arr[line+offset-banoff][pointer-1:]
    select=[]
    return copy_buffer, select


    
