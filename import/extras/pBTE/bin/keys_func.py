#Code by Sergio1260

from functions import *
from actions import *
from actions1 import *
from saveas import save_as
from openfile import open_file

def keys_func(key,text,pointer,oldptr,line,offset,columns,banoff,arr,rows,\
              max_len,filename,status,status_st,copy_buffer,fixstr,fix,\
              black,reset,saved_txt,ch_T_SP,banner,getch,keys,select):
        
    if key==keys["special"]:
        if not sep==chr(92): special_key=getch()
        special_key=getch() #Read char
        
        if special_key==keys["arr_up"] or special_key==keys["ctrl+arr_up"]:
            pointer, oldptr, text, offset, line, select =\
            up(line,offset,arr,text,banoff,oldptr,rows,pointer,special_key,keys,select)
            
        elif special_key==keys["arr_down"] or special_key==keys["ctrl+arr_down"]:
            pointer, oldptr, text, offset, line, select =\
            down(line,offset,arr,text,banoff,oldptr,rows,pointer,special_key,keys,select)

        elif special_key==keys["arr_right"]:          
            text, pointer, oldptr, line, offset =\
            right(pointer,text,columns,offset,line,banoff,arr,rows,oldptr)
            
        elif special_key==keys["arr_left"]:
            pointer, oldptr, text, line, offset =\
            left(pointer,oldptr,line,offset,banoff,text,arr)
            
        elif special_key==keys["supr"]:
            text, arr, select, status_st =\
            supr(pointer,max_len,text,offset,banoff,arr,line,select,status_st)
            
        elif special_key==keys["start"]:
            pointer=1; p_offset=0; oldptr=pointer
            
        elif special_key==keys["end"]:
            pointer=len(text)+1; oldptr=pointer
            
        elif special_key==keys["repag"]:
            line, offset, text, pointer, oldptr =\
            repag(line,offset,banoff,rows,arr,sep,pointer,oldptr)
            
        elif special_key==keys["avpag"]:
            line, offset, text, pointer, oldptr =\
            avpag(line,offset,banoff,rows,arr,sep,pointer,oldptr)


    elif key==keys["delete"]:
        line,offset, text, arr, pointer, select =\
        backspace(pointer,text,offset,line,arr,banoff,select)

    elif key==keys["return"]:
        line, offset, arr, pointer, text, staus =\
        newline(text,pointer,offset,banoff,line,arr,rows,status)
        
    elif key==keys["ctrl+s"]:
        out=open(filename,"w",encoding="UTF-8")
        out.write("\n".join(arr)); out.close()
        status=saved_txt; status_st=True
        out=open(filename,"r",encoding="UTF-8")
        
    elif key==keys["ctrl+x"]:
        copy_buffer, arr, text, line, offset, select =\
        cut(select,arr,line,offset,banoff,text,status_st,copy_buffer,pointer)
        
    elif key==keys["ctrl+c"]:
        copy_buffer, select =\
        copy(select,arr,line,offset,banoff,pointer)
        
    elif key==keys["ctrl+p"]:
        pointer, arr, text, status_st, copy_buffer =\
        paste(copy_buffer,arr,line,offset,banoff,pointer,text,status_st)                                              
            
    elif key==keys["ctrl+g"]:
        line, offset ,text =\
        goto(rows,banoff,line,arr,offset,black,reset)

    elif key==keys["ctrl+a"]:
        args = (filename,black,reset,rows,banoff,arr,columns,\
        status,offset,line,banner,status_st,saved_txt,getch,keys,fixstr)
        status_st, filename, status = save_as(args)

    elif key==keys["ctrl+o"]:
        args = (filename,black,reset,rows,banoff,arr,columns,\
        status,offset,line,banner,status_st,getch,keys,pointer,fixstr)
        arr,filename,status_st,pointer,line,offset = open_file(args)
        text=arr[line+offset-1]
        
    elif key==keys["ctrl+t"]: ch_T_SP = not ch_T_SP

    else: #All the other keys
        if not str(key)[4:6] in fixstr:
            out=decode(key,getch);p1=text[:pointer-1]; p2=text[pointer-1:]
            if out=="\t" and ch_T_SP: out=" "*4; pointer+=3
            text=(p1+out+p2); pointer+=1; status_st=False
            select=[]

    return text,pointer,oldptr,line,offset,columns,banoff,arr,rows,max_len,\
           filename,status,status_st,copy_buffer,fixstr,fix,ch_T_SP,select

