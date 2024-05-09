#Code by Sergio1260

from functions1 import *


def supr(pointer,offset,banoff,arr,line,select):
    text=arr[line+offset-banoff]
    if len(select)==0:
        p1=list(text)
        if (pointer-1)<len(p1) and len(p1)>0: 
            p1.pop(pointer-1)
            text="".join(p1)
        elif not line+offset==len(arr): #move all to previous line
            seltext=arr[line+offset-banoff+1]
            arr[line+offset-banoff+1]=text+seltext
            arr.pop(line+offset-banoff+1)
            text=text+seltext
        arr[line+offset-banoff]=text
    else:
        select,arr,line,offset =\
        del_sel(select,arr,banoff)

    return arr, line, offset, select


def goto(columns, rows, banoff, line, arr, offset, black):
    try:
        print("\r\033[%d;%dH"%(rows+banoff+2,1),end="")
        print(black+(" "*(columns+2))+"\r", end="")
        print(" Go to line: ", end=""); p1=input()
        print("\r\033[%d;%dH"%(line, 1),end="")
        line,offset = CalcRelLine(p1,arr,offset,line,banoff,rows)
    except: pass
    print("\033c", end="")
    return line, offset

def paste(copy_buffer,arr,line,offset,banoff,pointer,status_st,select):
    if not len(copy_buffer)==0:
        if len(select)==0:
            pos=line+offset-banoff; text=arr[pos]
            p1,p2 = text[:pointer-1],text[pointer-1:]
            if isinstance(copy_buffer,list):
                arr[pos]=p1+copy_buffer[0]+p2
                p1,p2 = arr[:pos+1],arr[pos+1:]
                arr=p1+copy_buffer[1:]+p2
            else: arr[pos]=p1+copy_buffer+p2
        else:
            start,end = sum(select[0]),sum(select[1])
            p1,p2 = arr[:start],arr[end:]
            if not isinstance(copy_buffer,list):
                arr=p1+[copy_buffer]+p2
            else: arr=p1+copy_buffer+p2
            select = []

    return pointer,arr,status_st,copy_buffer,line,offset,select

    
def cut(select,arr,line,offset,banoff,status_st,copy_buffer,pointer):
    text=arr[line+offset-banoff]
    if not len(select)==0:
        p1=arr[:sum(select[0])]
        p2=arr[sum(select[1]):]
        start=sum(select[0])-1
        if start<0: start=0
        copy_buffer=arr[start:sum(select[1])]
        if not start==0: copy_buffer=copy_buffer[1:]
        line=select[0][0]+banoff; offset=select[0][1]
        select = []; arr = p1 + p2
    else:
        copy_buffer=text[pointer-1:] 
        if (line+offset)<len(arr):
            arr.pop(line+offset-banoff)
            text=arr[line+offset-banoff]
        else: text=text[:pointer-1]
        arr[line+offset-banoff]=text
    return copy_buffer,arr,line,offset,select

def copy(select,arr,line,offset,banoff,pointer):
    if not len(select)==0:
        start=sum(select[0])-1
        if start<0: start=0
        copy_buffer=arr[start:sum(select[1])]
        if not start==0: copy_buffer=copy_buffer[1:]
    else: copy_buffer=arr[line+offset-banoff][pointer-1:]
    return copy_buffer

def repag(line,offset,banoff,rows,arr,sep,pointer,oldptr):
    p1=line+offset-banoff-rows
    if p1<0: p1=0
    line,offset = CalcRelLine(p1,arr,offset,line,banoff,rows)
    text=arr[line+offset-banoff]
    pointer,oldptr = fixlenline(text,pointer,oldptr)
    arr[line+offset-banoff]=text
    return line, offset, pointer, oldptr

def avpag(line,offset,banoff,rows,arr,sep,pointer,oldptr):
    p1=line+offset-banoff+rows
    if p1>=len(arr): p1="-"
    line,offset = CalcRelLine(p1,arr,offset,line,banoff,rows)
    text=arr[line+offset-banoff]
    pointer,oldptr = fixlenline(text,pointer,oldptr)
    arr[line+offset-banoff]=text
    return line, offset, pointer, oldptr


    
