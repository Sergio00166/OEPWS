#Code by Sergio1260

from actions import *
from actions1 import *
from saveas import save_as
from openfile import open_file


def keys_func(key,pointer,oldptr,line,offset,columns,banoff,arr,rows,
              filename,status,status_st,copy_buffer,black,bnc,slc,
              reset,saved_txt,ch_T_SP,banner,read_key,keys,select):

    if key==keys["supr"]:
        args=(pointer,offset,banoff,arr,line,select)
        arr, line, offset, select = supr(*args)
        status_st = False

    elif key==keys["arr_up"] or key==keys["ctrl+arr_up"]:
        selected = key==keys["ctrl+arr_up"]
        args=(line,offset,arr,banoff,oldptr,rows,pointer,select,selected)
        pointer, oldptr, offset, line, select = up(*args)
        
    elif key==keys["arr_down"] or key==keys["ctrl+arr_down"]:
        selected = key==keys["ctrl+arr_down"]
        args=(line,offset,arr,banoff,oldptr,rows,pointer,select,selected)
        pointer, oldptr, offset, line, select = down(*args)

    elif key==keys["arr_right"] or key==keys["ctrl+arr_right"]:
        args=(pointer,columns,offset,line,banoff,arr,rows,oldptr)
        pointer, oldptr, line, offset = right(*args); select=[]
        
    elif key==keys["arr_left"] or key==keys["ctrl+arr_left"]:
        args=(pointer,oldptr,line,offset,banoff,arr)
        pointer,oldptr,line,offset = left(*args); select=[]
        
    elif key==keys["start"]: pointer,oldptr,select = 1,1,[]
        
    elif key==keys["end"]:
        text=arr[line+offset-banoff]
        pointer = len(text)+1
        oldptr,select = pointer,[]
        
    elif key==keys["repag"] or key==keys["ctrl+repag"]:
        fix = key==keys["ctrl+repag"]
        args=(line,offset,banoff,rows,arr,sep,pointer,oldptr,select,fix)
        line,offset,pointer,oldptr,select = repag(*args)
        
    elif key==keys["avpag"] or key==keys["ctrl+avpag"]:
        fix = key==keys["ctrl+avpag"]
        args=(line,offset,banoff,rows,arr,sep,pointer,oldptr,select,fix)
        line,offset,pointer,oldptr,select = avpag(*args)
            

    elif key==keys["delete"]:
        args=(pointer,offset,line,arr,banoff,select)
        line,offset,arr,pointer,select = backspace(*args)
        status_st = False

    elif key==keys["return"]:
        args=(pointer,offset,banoff,line,arr,rows,status,select)
        line,offset,arr,pointer,staus,select = newline(*args)
        status_st = False

    elif key==keys["ctrl+s"]:
        out=open(filename,"w",encoding="UTF-8",newline='')
        out.write("\n".join(arr)); out.close()
        status=saved_txt; status_st=True
        out=open(filename,"r",encoding="UTF-8")
        
    elif key==keys["ctrl+x"]:
        args=(select,arr,line,offset,banoff,status_st,copy_buffer,pointer)
        copy_buffer,arr,line,offset,select = cut(*args)
        
    elif key==keys["ctrl+c"]:
        args=(select,arr,line,offset,banoff,pointer)
        copy_buffer = copy(*args)
        
    elif key==keys["ctrl+p"]:
        args=(copy_buffer,arr,line,offset,banoff,pointer,status_st,select)
        pointer,arr,status_st,copy_buffer,line,offset,select = paste(*args)                                              
            
    elif key==keys["ctrl+g"]:
        args=(columns,rows,banoff,line,arr,offset,bnc)
        line,offset = goto(*args)

    elif key==keys["ctrl+a"]:
        args = (filename,black,bnc,slc,reset,rows,banoff,arr,columns,status,\
                offset,line,banner,status_st,saved_txt,keys,read_key)
        status_st,filename,status = save_as(args)

    elif key==keys["ctrl+o"]:
        args = (filename,black,bnc,slc,reset,rows,banoff,arr,columns,status,offset\
                ,line,banner,status_st,keys,pointer,oldptr,select,read_key)
        arr,filename,status_st,pointer,oldptr,line,offset,select = open_file(args)
        
    elif key==keys["ctrl+t"]: ch_T_SP = not ch_T_SP

    else: #All the other keys
        args=(arr,key,select,pointer,line,offset,banoff,ch_T_SP,rows,keys)
        arr, pointer, line, offset = get_str(*args)
        status_st = False
                
    return pointer,oldptr,line,offset,columns,banoff,arr,rows,\
           filename,status,status_st,copy_buffer,ch_T_SP,select

