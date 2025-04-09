# Code by Sergio00166

from functions import *
from actions import up,down


def paste(copy_buffer, arr, line, offset, banoff, cursor, select, rows, status_st):
    if not len(copy_buffer)==0:
        if len(select)==0:
            pos = line+offset-banoff
            text = arr[pos]
            p1,p2 = text[:cursor-1],text[cursor-1:]
            if isinstance(copy_buffer,list):
                arr[pos] = p1+copy_buffer[0]
                for i, new_line in enumerate(copy_buffer[1:], start=1):
                    arr.insert(pos+i,new_line)
                arr[pos+len(copy_buffer)-1] += p2
                line,offset = calc_displacement(copy_buffer[1:],line,banoff,offset,rows)
                cursor = len(copy_buffer[-1])+1
            else:
                arr[pos] = p1+copy_buffer+p2
                cursor += len(copy_buffer)
        else:
            start = sum(select[0])
            select,arr,line,offset = del_sel(select, arr, banoff)
            if isinstance(copy_buffer,list):
                for i, new_line in enumerate(copy_buffer):
                    arr.insert(start+i,new_line)
                line,offset = calc_displacement(copy_buffer,line,banoff,offset,rows,1)
                cursor = len(copy_buffer[-1])+1
            else:
                arr.insert(start,copy_buffer)
                cursor = len(copy_buffer)+1
        status_st = False
    return cursor, arr, copy_buffer, line, offset, select, status_st


def cut(select, arr, line, offset, banoff, copy_buffer, cursor):
    pos = line+offset-banoff
    text = arr[pos]
    if select:
        start = max(sum(select[0])-1, 0)
        copy_buffer = arr[start:sum(select[1])]
        if start>0: copy_buffer = copy_buffer[1:]
        select,arr,line,offset = del_sel(select,arr,banoff)
    else:
        if cursor==1:
            if pos==len(arr)-1:
                 if not text == "":
                     copy_buffer = text
                     arr[pos] = ""
            else:
                copy_buffer = text
                arr.pop(pos)

        elif cursor-1==len(text):
            if pos<len(arr)-1:
                copy_buffer = arr.pop(pos+1)
        else:
            arr[pos] = text[:cursor-1]
            copy_buffer = text[cursor-1:]

    if isinstance(copy_buffer,list) and len(copy_buffer)==1:
        copy_buffer = copy_buffer[0]
    return copy_buffer, arr, line, offset, select


def copy(select, arr, line, offset, banoff, cursor):
    if select:
        start = max(sum(select[0])-1, 0)
        copy_buffer = arr[start:sum(select[1])]
        if start> 0: copy_buffer = copy_buffer[1:]
    else:
        pos = line+offset-banoff
        text = arr[pos]
        if cursor-1==len(text):
            if pos<len(arr)-1:
                copy_buffer = arr[pos+1]
        else: copy_buffer = text[cursor-1:]

    if isinstance(copy_buffer,list) and len(copy_buffer)==1:
        copy_buffer = copy_buffer[0]
    return copy_buffer


def repag(line,offset,banoff,rows,arr,sep,cursor,oldptr,select,selected):
    for x in range(0,rows):
        cursor, oldptr, offset, line, select =\
        up(line,offset,arr,banoff,oldptr,rows,cursor,select,selected)
    return line, offset, cursor, oldptr, select

def avpag(line,offset,banoff,rows,arr,sep,cursor,oldptr,select,selected):
    for x in range(0,rows):
        cursor, oldptr, offset, line, select =\
        down(line,offset,arr,banoff,oldptr,rows,cursor,select,selected)
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

def newline(cursor,offset,banoff,line,arr,rows,select):
    if not len(select) == 0:
        select,arr,line,offset = del_sel(select,arr,banoff)
        if len(arr)==0: return line,offset,arr,1,select
    text = arr[line+offset-banoff]
    if not len(text) == 0:
        arr.insert(line+offset-banoff,text[:cursor-1])
        text = text[cursor-1:]; cursor = 1
    else: arr.insert(line+offset-banoff, "")
    if line>rows: offset += 1
    else: line += 1
    arr[line+offset-banoff] = text
    return line,offset,arr,cursor,select

