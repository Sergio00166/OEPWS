#Code by Sergio1260

from functions import *


def down(line,offset,arr,text,banoff,oldptr,rows,pointer,key,keys,select,fix):
    selected=key==keys["ctrl+arr_down"] and fix
    if selected:
        selst=[line-banoff,offset]
        fix=line+offset
    if not line+offset==len(arr)+banoff-1:
        if not line==rows+banoff: line+=1
        elif not line+offset==len(arr)+1: offset+=1
        text=arr[line+offset-banoff]
        pointer,oldptrt=fixlenline(text,pointer,oldptr)
    if selected:
        seled=[line-banoff,offset]
        if not len(select)==0:
            select[1]=seled
        else: select=[selst,seled]
    else: select=[]
 
    return pointer, oldptr, text, offset, line, select

def up(line,offset,arr,text,banoff,oldptr,rows,pointer,key,keys,select,fix): 
    selected=key==keys["ctrl+arr_up"] and fix
    if selected: seled=[line-banoff,offset]
    if not line==banoff: line-=1
    elif offset>0: offset-=1
    text=arr[line+offset-banoff]
    pointer,oldptr=fixlenline(text,pointer,oldptr)
    if selected:
        selst=[line-banoff,offset]
        if not len(select)==0:
            select[0]=selst
        else: select=[selst,seled]
    else: select=[]
    return pointer, oldptr, text, offset, line, select

def backspace(pointer,text,offset,line,arr,banoff,select):
    if len(select)==0:
        if not pointer==1: #Delete char   
            p1=list(text)+[""]
            p1.pop(pointer-2)
            text="".join(p1)
            pointer-=1
            
        else: #move all to previous line
            if not offset+line==1:
                seltext=arr[line+offset-banoff-1]
                arr[line+offset-banoff-1]=seltext+text
                arr.pop(line+offset-banoff)
                pointer=len(seltext)+1
                text=seltext+text
                if not offset==0: offset-=1
                else: line-=1
                status_st=False
    else: select,arr,text,line,offset = del_sel(select,arr,banoff)
    return line, offset, text, arr, pointer, select

def newline(text,pointer,offset,banoff,line,arr,rows,status,select):  
    p1=arr[:line+offset-banoff]
    p2=arr[line+offset-banoff:]
    if not len(text)==0:
        fix=1
        seltext=[text[:pointer-fix]]
        arr=p1+seltext+p2
        text=text[pointer-fix:]
        pointer=0
    else: arr=p1+[""]+p2
    if not line>rows: line+=1
    else: offset+=1
    status_st=False
    if not len(select)==0: select=[]
    return line, offset, arr, pointer, text, status, select

def left(pointer,oldptr,line,offset,banoff,text,arr):
    if not pointer==1: pointer-=1; oldptr=pointer
    elif not line+offset==1:
        if offset==0: line-=1
        else: offset-=1
        text=arr[line+offset-banoff]
        pointer=len(text)+1
    return pointer, oldptr, text, line, offset

def right(pointer,text,columns,offset,line,banoff,arr,rows,oldptr):
    if not pointer>len(text):
        pointer+=1
        oldptr=pointer
    else:
        if not offset+line>len(arr)-1:
            if not line>rows-2: line+=1
            else: offset+=1
            pointer=1
            text=arr[line+offset-banoff]
    return text, pointer, oldptr, line, offset


