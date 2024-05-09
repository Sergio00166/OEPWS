#Code by Sergio1260

from os import get_terminal_size,sep
from multiprocessing import cpu_count, Pool


def get_size():
    size=get_terminal_size()
    return size[1]-2,size[0]-2

def decode(key,getch):
    for x in range(3):
        try: out=key.decode("UTF-8"); break
        except: key+=getch()
    return out

def fixlenline(text, pointer, oldptr):
    length=len(text)+1
    if pointer>length or oldptr>length:
        return length,oldptr
    elif oldptr>pointer: return oldptr,oldptr
    else: return pointer,oldptr

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
