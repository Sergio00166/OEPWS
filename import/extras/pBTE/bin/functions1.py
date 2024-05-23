#Code by Sergio1260

from os import get_terminal_size,sep
from multiprocessing import cpu_count, Pool


def get_size():
    size=get_terminal_size()
    return size[1]-2,size[0]-2

def decode(key): return key.decode("UTF-8")

def fixlenline(text,pointer,oldptr):
    length=len(text)+1
    if pointer>length or oldptr>length:
        return length
    elif oldptr>pointer: return oldptr
    else: return pointer

def CalcRelLine(p1,arr,offset,line,banoff,rows):
    if p1=="-": p1=len(arr)-1
    try:
        p1=int(p1)
        if p1<len(arr):
            if p1<rows: offset=0; line=p1+banoff
            else: offset=p1-rows; line=rows+banoff
    except: pass
    return line, offset

def fixfilename(filename, columns):
    if len(filename)+32>columns: #If filename overflows
        flfix=filename.split(sep)
        filename=flfix[len(flfix)-1]
        if len(filename)+31>columns: #If still not fiting
            middle = len(filename) // 2
            filename=filename[:middle-1]+'*'+filename[middle+2:]
            if len(filename)+31>columns:
                filename=filename[:columns-32]+"*"
    return filename

def del_sel(select, arr, banoff):
    p1=arr[:sum(select[0])]; p2=arr[sum(select[1]):]
    line=select[0][0]+banoff; offset=select[0][1]
    select=[]; arr=p1+p2 
    return select, arr, line, offset

def mng_tab_select(arr,line,offset,select,ch_T_SP):
    # Get the values from select
    start=sum(select[0]); end=sum(select[1])
    # Get the text that is upper and below the selected region
    p0=arr[:start]; p2=arr[end:]
    # Get the text that is selected
    p1=arr[start:end]
    # Add a tab at the start of each element
    tab=" "*4 if ch_T_SP else "\t"
    p1=[tab+x for x in p1]
    # Now reconstruct all arr
    return p0+p1+p2

def get_str(arr,key,select,pointer,line,offset,banoff,ch_T_SP,rows,keys):
    
    out,skip = decode(key),False
   
    if select:
        if not out=="\t": select,arr,line,offset = del_sel(select,arr,banoff)     
        else: arr,skip = mng_tab_select(arr,line,offset,select,ch_T_SP),True
       
    if not skip:
        pos=line+offset-banoff; text=arr[pos]
        p1,p2 = text[:pointer-1], text[pointer-1:]
        if ch_T_SP: out=out.replace("\t"," "*4)
        out_lines = out.split(keys["return"].decode("utf-8"))
        arr[pos] = p1+out_lines[0]+p2
        
        if len(out_lines) > 1:
            arr[pos+1:pos+1] = out_lines[1:]
            line,offset = CalcRelLine(pos+len(out_lines)-1,arr,offset,line,banoff,rows)
            pointer += len(out_lines[-1])
        else: pointer += len(out_lines[0])

    return arr, pointer, line, offset


# Each line is ejecuted on a separate CPU core
def read_UTF8(file):
    file=open(file,"rb").readlines()
    pool=Pool(processes=cpu_count())
    out=pool.map_async(decode_until_error,file)
    out=out.get(); pool.close()
    return out

# Decodes the UTF8 and if it cant decode a byte it decodes it as ASCII
def decode_until_error(data):
    decoded = ""; index = 0
    while index < len(data):
        try:
            char = data[index:].decode('utf-8')
            decoded += char
            index += len(char.encode('utf-8'))
        except UnicodeDecodeError as e:
            byte_sequence = bytearray()
            byte_sequence.append(data[index])
            index += 1
            while index < len(data):
                if data[index] & 0b11000000 == 0b10000000:
                    byte_sequence.append(data[index])
                    index += 1
                else: break
            try:
                char = byte_sequence.decode('utf-8')
                decoded += char
            except UnicodeDecodeError:
                for byte in byte_sequence:
                    decoded += chr(byte)

    if decoded.endswith("\n"): decoded=decoded[:-1]
    if decoded.endswith("\r"): decoded=decoded[:-1]
    return decoded
