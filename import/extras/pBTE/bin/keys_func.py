#Code by Sergio1260

from functions import *
from actions import *
from actions1 import *
from saveas import save_as
from openfile import open_file

def keys_func(key,pointer,oldptr,line,offset,columns,banoff,arr,rows,
              filename,status,status_st,copy_buffer,fixstr,fix,\
              black,reset,saved_txt,ch_T_SP,banner,getch,keys,select):
        
    if key==keys["special"]:
        if not sep==chr(92): getch()
        special_key=getch() #Read char
        fix=(sep==chr(92) or special_key==b'1')
        if not sep==chr(92) and special_key==b'1':
            getch(); getch(); special_key=getch()

        if special_key==keys["supr"]:
            args=(pointer,offset,banoff,arr,line,select)
            arr, line, offset, select = supr(*args)
            if not sep==chr(92): getch()
            status_st = False
            
        # Not implemented yet
        elif special_key==keys["insert"] and (not sep==chr(92)): getch()

        elif special_key==keys["arr_up"] or special_key==keys["ctrl+arr_up"]:
            args=(line,offset,arr,banoff,oldptr,rows,pointer,special_key,keys,select,fix)
            pointer,oldptr,offset,line,select = up(*args)
            
        elif special_key==keys["arr_down"] or special_key==keys["ctrl+arr_down"]:
            args=(line,offset,arr,banoff,oldptr,rows,pointer,special_key,keys,select,fix)
            pointer, oldptr, offset, line, select = down(*args)

        elif special_key==keys["arr_right"] or special_key==keys["ctrl+arr_right"]:
            args=(pointer,columns,offset,line,banoff,arr,rows,oldptr)
            pointer,oldptr,line,offset = right(*args)
            select=[]
            
        elif special_key==keys["arr_left"] or special_key==keys["ctrl+arr_left"]:
            args=(pointer,oldptr,line,offset,banoff,arr)
            pointer,oldptr,line,offset = left(*args)
            select=[]
            
        elif special_key==keys["start"]:
            pointer=1; p_offset=0; oldptr=pointer; select=[]
            
        elif special_key==keys["end"]:
            text=arr[line+offset-banoff]
            pointer = len(text)+1
            oldptr=pointer; select=[]
            
        elif special_key==keys["repag"]:
            args=(line,offset,banoff,rows,arr,sep,pointer,oldptr)
            line,offset,pointer,oldptr = repag(*args)
            if not sep==chr(92): getch()
            select=[]
            
        elif special_key==keys["avpag"]:
            args=(line,offset,banoff,rows,arr,sep,pointer,oldptr)
            line,offset,pointer,oldptr = avpag(*args)
            if not sep==chr(92): getch()
            select=[]

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
        args=(columns,rows,banoff,line,arr,offset,black)
        line,offset = goto(*args)

    elif key==keys["ctrl+a"]:
        args = (filename,black,reset,rows,banoff,arr,columns,status,offset,line,banner,status_st,saved_txt,getch,keys,fixstr)
        status_st,filename,status = save_as(args)

    elif key==keys["ctrl+o"]:
        args = (filename,black,reset,rows,banoff,arr,columns,status,offset,line,banner,status_st,getch,keys,pointer,fixstr)
        arr,filename,status_st,pointer,line,offset = open_file(args)
        
    elif key==keys["ctrl+t"]: ch_T_SP = not ch_T_SP

    else: #All the other keys
        if not str(key)[4:6] in fixstr:
            out=decode(key,getch); skip=False
            inc=(4 if out=="\t" and ch_T_SP else 1)
            if len(select)>0:
                if out=="\t":
                    args=arr,line,offset,select,ch_T_SP
                    arr,skip = mng_tab_select(*args), True
                else: select,arr,line,offset = del_sel(select,arr,banoff)
                
            if out=="\t" and ch_T_SP: out=" "*4
            if not skip:
                text=arr[line+offset-banoff]
                p1,p2=text[:pointer-1],text[pointer-1:]
                pointer+=inc # Increment the char pos
                arr[line+offset-banoff]=(p1+out+p2)
            status_st=False

    return pointer,oldptr,line,offset,columns,banoff,arr,rows,\
           filename,status,status_st,copy_buffer,fixstr,fix,ch_T_SP,select

