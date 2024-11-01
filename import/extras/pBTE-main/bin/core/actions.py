# Code by Sergio00166

from functions1 import *


def down(line,offset,arr,banoff,oldptr,rows,cursor,select,selected):
    if selected:
        selst = [line-banoff,offset]
        fix = line+offset
    if not line+offset==len(arr)+banoff-1:
        if not line==rows+banoff: line += 1
        elif not line+offset==len(arr)+1: offset += 1
        text = arr[line+offset-banoff]
        cursor = fixlenline(text,cursor,oldptr)
    if selected:
        seled = [line-banoff,offset]
        if sum(seled)<fix:
            seled[0] = seled[0]+1
        if len(select)==0:
            select = [selst,seled]
        else: select[1] = seled
    else: select = []
    return cursor, oldptr, offset, line, select

def up(line,offset,arr,banoff,oldptr,rows,cursor,select,selected):
    if selected: seled = [line-banoff,offset]
    if not line==banoff: line -= 1
    elif offset>0: offset -= 1
    text = arr[line+offset-banoff]
    cursor = fixlenline(text,cursor,oldptr)
    if selected:
        selst = [line-banoff,offset]
        if len(select)==0:
            select = [selst,seled]
        else: select[0] = selst
    else: select = []
    return cursor, oldptr, offset, line, select

def left(cursor,oldptr,line,offset,banoff,arr):
    if not cursor==1:
        cursor -= 1
        oldptr = cursor
    elif line+offset>banoff:
        if line>1: line -= 1
        elif offset>0: offset -= 1
        text = arr[line+offset-banoff]
        cursor = len(text)+1
    return cursor, oldptr, line, offset

def right(cursor,columns,offset,line,banoff,arr,rows,oldptr):
    text = arr[line+offset-banoff]
    if not cursor>len(text):
        cursor += 1
        oldptr = cursor
    elif not offset+line>len(arr)-1:
        if line>rows: offset += 1
        else: line += 1
        cursor = 1
    return cursor, oldptr, line, offset

def backspace(cursor,offset,line,arr,banoff,select):
    text=arr[line+offset-banoff]
    if len(select)==0:
        if not cursor==1: #Delete char
            p1 = list(text)+[""]
            # Fix weird bug
            try: p1.pop(cursor-2)
            except: p1.pop(cursor-1)
            text = "".join(p1)
            cursor -= 1
        else: #move all to previous line
            if not offset+line==1:
                seltext = arr[line+offset-banoff-1]
                arr[line+offset-banoff-1] = seltext+text
                arr.pop(line+offset-banoff)
                cursor = len(seltext)+1
                text = seltext+text
                if offset==0: line -= 1
                else: offset -= 1
        arr[line+offset-banoff] = text
    else: select,arr,line,offset,cursor = *del_sel(select,arr,banoff),1
    return line, offset, arr, cursor, select

def supr(cursor,offset,banoff,arr,line,select):
    text = arr[line+offset-banoff]
    if len(select)==0:
        p1 = list(text)
        if (cursor-1)<len(p1) and len(p1)>0:
            p1.pop(cursor-1)
            text = "".join(p1)
        elif not line+offset==len(arr): #move all to previous line
            seltext = arr[line+offset-banoff+1]
            arr[line+offset-banoff+1] = text+seltext
            arr.pop(line+offset-banoff+1)
            text = text+seltext
        arr[line+offset-banoff] = text
    else: select,arr,line,offset,cursor = *del_sel(select,arr,banoff),1
    return arr, line, offset, select

def comment_func(arr,line,offset,banoff,select,comment,cursor,indent):
    orig = arr[line+offset-banoff]
    if not len(select)>0:
        pos = line+offset-banoff
        p1,p2 = cmt_w_ind(arr[pos], indent)
        arr[pos] = p1+comment[0]+p2+comment[1]            
    else: arr = select_add_start_str(arr,line,offset,select,comment)
    if not orig==arr[line+offset-banoff]: cursor+=len(comment[0])
    return arr,cursor

def uncomment_func(arr,line,offset,banoff,select,comment,cursor,indent):
    orig = arr[line+offset-banoff]
    if not len(select)>0:
        pos,lenght = line+offset-banoff,len(comment[0])
        p1,p2 = cmt_w_ind(arr[pos], indent)
        if p2.startswith(comment[0]): p2=p2[lenght:]
        if p2.endswith(comment[0]): p2=p2[:lenght]
        arr[pos] = p1+p2 
    else: arr = select_add_start_str(arr,line,offset,select,comment,True)
    if not orig==arr[line+offset-banoff]: cursor-=len(comment[0])
    return arr,cursor
    
