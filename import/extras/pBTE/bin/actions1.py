# Code by Sergio00166

from functions1 import *


def paste(copy_buffer,arr,line,offset,banoff,cursor,select,rows,status_st):
    if not len(copy_buffer)==0:
        if len(select)==0:
            pos=line+offset-banoff; text=arr[pos]
            p1,p2 = text[:cursor-1],text[cursor-1:]
            if isinstance(copy_buffer,list):
                arr[pos]=p1+copy_buffer[0]
                p1,p3 = arr[:pos+1],arr[pos+1:]
                line,offset = calc_displacement(copy_buffer[1:],line,banoff,offset,rows)
                cursor = len(copy_buffer[-1])+1
                arr=p1+copy_buffer[1:-1]+[copy_buffer[-1]+p2]+p3        
            else:
                arr[pos] = p1+copy_buffer+p2
                cursor += len(copy_buffer)
        else:
            start = sum(select[0])
            select,arr,line,offset = del_sel(select,arr,banoff)
            p1,p2 = arr[:start],arr[start:]
            if isinstance(copy_buffer,list):
                arr=p1+copy_buffer+p2
                line,offset = calc_displacement(copy_buffer,line,banoff,offset,rows,1)
                cursor = len(copy_buffer[-1])+1
            else:
                arr=p1+[copy_buffer]+p2
                cursor = len(copy_buffer)+1
        status_st = False
    return cursor,arr,copy_buffer,line,offset,select,status_st
    
def cut(select,arr,line,offset,banoff,copy_buffer,cursor):
    pos = line+offset-banoff
    text=arr[pos]
    if not len(select)==0:
        start=sum(select[0])-1
        if start<0: start=0
        copy_buffer=arr[start:sum(select[1])]
        if not start==0: copy_buffer=copy_buffer[1:]
        select,arr,line,offset = del_sel(select,arr,banoff)
    else:
        copy_buffer=text[cursor-1:]
        if cursor==1 or cursor==len(text):
            arr.pop(pos)
            pos = line+offset-banoff
            if pos==len(arr) and pos!=0:
                if offset>0: offset-=1
                else: line-=1
        else:
            text=text[:cursor-1]
            arr[pos]=text           
    if isinstance(copy_buffer,list) and len(copy_buffer)==1:
        copy_buffer = copy_buffer[0]
    return copy_buffer,arr,line,offset,select

def copy(select,arr,line,offset,banoff,cursor):
    if not len(select)==0:
        start=sum(select[0])-1
        if start<0: start=0
        copy_buffer=arr[start:sum(select[1])]
        if not start==0: copy_buffer=copy_buffer[1:]
    else: copy_buffer=arr[line+offset-banoff][cursor-1:]
    if isinstance(copy_buffer,list) and len(copy_buffer)==1:
        copy_buffer = copy_buffer[0] 
    return copy_buffer

def repag(line,offset,banoff,rows,arr,sep,cursor,oldptr,select,selected):
    if selected: seled=[line-banoff,offset]
    p1=line+offset-banoff-rows
    if p1<0: p1=0
    line,offset = CalcRelLine(p1,arr,offset,line,banoff,rows)
    text=arr[line+offset-banoff]
    cursor=fixlenline(text,cursor,oldptr)
    arr[line+offset-banoff]=text  
    if selected:
        selst=[line-banoff,offset]
        if len(select)==0:
            select=[selst,seled]
        else: select[0]=selst
    else: select=[]    
    return line, offset, cursor, oldptr, select

def avpag(line,offset,banoff,rows,arr,sep,cursor,oldptr,select,selected):
    if selected:
        selst=[line-banoff,offset]
        fix=line+offset
    p1=line+offset-banoff+rows
    if p1>=len(arr): p1="-"
    line,offset = CalcRelLine(p1,arr,offset,line,banoff,rows)
    text=arr[line+offset-banoff]
    cursor=fixlenline(text,cursor,oldptr)
    arr[line+offset-banoff]=text
    if selected:
        seled=[line-banoff,offset]
        if sum(seled)<fix:
            seled[0]=seled[0]+1
        if len(select)==0:
            select=[selst,seled]
        else: select[1]=seled
    else: select=[]  
    return line, offset, cursor, oldptr, select

def dedent(arr,line,offset,banoff,indent,cursor):
    text = arr[line+offset-banoff]
    p1 = text[:cursor-1]
    p2 = text[cursor-1:]
    if len(indent)>0 and p1.endswith(indent):
        p1 = p1[:-len(indent)]
        cursor-=len(indent)
        arr[line+offset-banoff] = p1+p2
    return arr,cursor

