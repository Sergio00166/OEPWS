# Code by Sergio00166

from actions import *
from actions1 import *
from saveas import save_as
from openfile import open_file


def keys_func(key,pointer,oldptr,line,offset,columns,banoff,arr,rows,
              filename,status,status_st,copy_buffer,black,bnc,slc,reset,
              saved_txt,indent,banner,read_key,keys,select,codec,lnsep,comment):

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
        times = 4 if key==keys["ctrl+arr_right"] else 1
        for x in range(times):
            args=(pointer,columns,offset,line,banoff,arr,rows,oldptr)
            pointer, oldptr, line, offset = right(*args)
        select=[]
        
    elif key==keys["arr_left"] or key==keys["ctrl+arr_left"]:
        times = 4 if key==keys["ctrl+arr_left"] else 1
        for x in range(times):
            args=(pointer,oldptr,line,offset,banoff,arr)
            pointer,oldptr,line,offset = left(*args)
        select=[]
        
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
        out=open(filename,"w",encoding=codec,newline='')
        out.write(lnsep.join(arr)); out.close()
        status=saved_txt; status_st=True
        
    elif key==keys["ctrl+x"]:
        args=(select,arr,line,offset,banoff,copy_buffer,pointer)
        copy_buffer,arr,line,offset,select = cut(*args)
        status_st = False
        
    elif key==keys["ctrl+c"]:
        args=(select,arr,line,offset,banoff,pointer)
        copy_buffer = copy(*args)
        
    elif key==keys["ctrl+p"]:
        args=(copy_buffer,arr,line,offset,banoff,pointer,select,rows,status_st)
        pointer,arr,copy_buffer,line,offset,select,status_st = paste(*args)
            
    elif key==keys["ctrl+g"]:
        args=(columns,rows,banoff,line,arr,offset,bnc)
        line,offset = goto(*args)

    elif key==keys["ctrl+a"]:
        args = (filename,black,bnc,slc,reset,rows,banoff,arr,columns,status,\
                offset,line,banner,status_st,saved_txt,keys,read_key,codec,lnsep)
        status_st,filename,status,codec,lnsep = save_as(args)

    elif key==keys["ctrl+o"]:
        args = (filename,black,bnc,slc,reset,rows,banoff,arr,columns,status,offset,\
                line,banner,status_st,keys,pointer,oldptr,select,read_key,codec,lnsep)
        arr,filename,status_st,pointer,oldptr,line,offset,select,codec,lnsep = open_file(args)
        
    elif key==keys["f1"]: indent = chg_var_str(columns,rows,banoff,line,bnc,indent,"indent") 
    elif key==keys["f2"]: comment[0] = chg_var_str(columns,rows,banoff,line,bnc,comment[0],"comment")
    elif key==keys["f3"]: comment[1] = chg_var_str(columns,rows,banoff,line,bnc,comment[1],"end cmt") 

    elif key==keys["ctrl+d"]:
        if len(select)>0:
            arr = select_add_start_str(arr,line,offset,select,indent,True)
        else: arr,pointer = dedent(arr,line,offset,banoff,indent,pointer)
    
    elif key==keys["ctrl+k"]:
        if len(select)>0: slt = select
        else:
            slt = [[line-banoff,offset],[line,offset]]
            pointer += len(comment[0])
        arr = select_add_start_str(arr,line,offset,slt,comment)
    
    elif key==keys["ctrl+u"]:    
        if len(select)>0: slt = select
        else: 
            slt = [[line-banoff,offset],[line,offset]]
            x = arr[line+offset-banoff]
            if x.startswith(comment[0]) and x.endswith(comment[1]):
                pointer -= len(comment[0])
        arr = select_add_start_str(arr,line,offset,slt,comment,True)

    else: #All the other keys
        args=(arr,key,select,pointer,line,offset,banoff,indent,rows,keys)
        arr, pointer, line, offset, select = get_str(*args)
        status_st = False
                
    return pointer,oldptr,line,offset,columns,banoff,arr,rows,filename,\
           status,status_st,copy_buffer,indent,select,codec,lnsep,comment

