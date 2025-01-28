# Code by Sergio00166

from os import get_terminal_size,sep
from os.path import split as psplit
from multiprocessing import cpu_count, Pool
from re import split as resplit
from data import ascii_no_lfcr
        
bom_map = {
    b'\xef\xbb\xbf': 'utf-8-sig',
    b'\xff\xfe': 'utf-16-le',
    b'\xfe\xff': 'utf-16-be',
}
rev_bom_map = {
    'utf-8-sig': b'\xef\xbb\xbf',
    'utf-16-le': b'\xff\xfe',
    'utf-16-be': b'\xfe\xff',
}
codecs_no_bom = ("utf-8", "utf-16", "latin_1")



def calc_displacement(data,line,banoff,offset,rows,rect=0):
    line += len(data)-rect
    if line-banoff>rows:
        offset+=line-rows-banoff
        line=rows+banoff
    return line,offset

def get_size():
    size=get_terminal_size()
    return size[1]-2,size[0]-2

def cmt_w_ind(string, sepstr):
    pos,lenght = 0,len(sepstr)
    while string.startswith(sepstr,pos): pos+=lenght
    return string[:pos], string[pos:]

def decode(key):
    out = key.decode("UTF-8")
    for x in ascii_no_lfcr:
        if chr(x) in out:
            return ""
    return out

def fixlenline(text,cursor,oldptr):
    lenght=len(text)+1
    if cursor>lenght or oldptr>lenght:
        return lenght
    elif oldptr>cursor: return oldptr
    else: return cursor

def CalcRelLine(p1,arr,offset,line,banoff,rows):
    try: p1 = len(arr)-1 if p1=="-" else int(p1)
    except: return line, offset
    if p1<len(arr):
        part = (rows//2)
        line,offset = part,p1-part
        if offset<0: offset,line = 0,p1
        line += banoff
    return line, offset

def del_sel(select, arr, banoff, blank=False):
    p1=arr[:sum(select[0])]
    p2=arr[sum(select[1]):]
    line=select[0][0]+banoff
    offset=select[0][1]
    if blank: arr=p1+[""]+p2
    else: arr=p1+p2
    # Fix when selection is on bottom
    if line>banoff and line+offset-banoff>len(arr)-1:
        if offset>0: offset-=1
        else: line-=1
    return [], arr, line, offset

def fixfilename(path, lenght):
    if len(path) <= lenght: return path
    dirname, basename = psplit(path)
    if len(path) <= lenght: return path
    available_lenght = lenght - len(basename) - 1
    if available_lenght <= 0: return basename[:lenght - 1]+'*'
    parts = dirname.split(sep)
    while len(parts) > 0 and len(sep.join(parts)) > available_lenght: parts.pop(0)
    if len(parts) == 0: compacted_path=basename
    else: compacted_path = sep.join(parts)+sep+basename
    return compacted_path

def select_add_start_str(arr,line,offset,select,text,remove=False):
    # Get the values from select
    start=sum(select[0]); end=sum(select[1])
    # Get the text that is upper and below the selected region
    p0=arr[:start]; p2=arr[end:]
    # Get the text that is selected
    p1=arr[start:end]
    if isinstance(text, list):
        if not remove: p1=[text[0]+x+text[1] for x in p1]
        else:
            p1 = [
                x[len(text[0]):] if len(text[1])==0 and x.startswith(text[0])
                else x[len(text[0]):-len(text[1])]
                if x.startswith(text[0]) and x.endswith(text[1])
                else x for x in p1
            ]
    elif not remove: p1=[text+x for x in p1]
    else: p1 = [x[len(text):] if x.startswith(text) else x for x in p1]   
    return p0+p1+p2 # Reconstruct the arr


def get_str(arr,key,select,cursor,line,offset,banoff,indent,rows,keys):
    out = decode(key)
    if select:
        if out=="\t":
            args = (arr,line,offset,select,indent)
            arr = select_add_start_str(*args)
            return arr, cursor, line, offset, select
        else:
            args = (select,arr,banoff,True)
            select,arr,line,offset = del_sel(*args)
            cursor = 1 # Reset cursor value

    pos = line+offset-banoff
    text = arr[pos] # Get current line
    p1,p2 = text[:cursor-1],text[cursor-1:]
    out = out.replace("\t",indent)
    out_lines = resplit(r'[\n\r]',out)

    if not select and len(out_lines)>1:
        arr[pos] = p1+out_lines[0]
    else: arr[pos] = p1+out_lines[0]+p2

    if len(out_lines) > 1:
        cursor = len(out_lines[-1])+1
        if not select: out_lines[-1] += p2
        arr[pos+1:pos+1] = out_lines[1:]
        args = (out_lines,line,banoff,offset,rows,1)
        line,offset = calc_displacement(*args)
    else: cursor += len(out_lines[0])

    return arr, cursor, line, offset, select


# Detect if indent is tab or space
def taborspace(contents):
    sp_cnt,tab_cnt = 0,0
    for x in contents:
        if x.startswith(" "*4): sp_cnt+=1
        if x.startswith("\t"): tab_cnt+=1
    return " "*4 if sp_cnt>tab_cnt else "\t"


def detect_line_ending_char(c):
    c = c[:1024]
    crlf = c.count('\r\n')
    c = c.replace('\r\n','')
    cr = c.count('\r')
    lf = c.count('\n')
    if crlf>cr and crlf>lf:
        return '\r\n'
    elif cr>lf: return '\r'
    else: return '\n'


def read_UTF8(path):
    data = open(path, "rb").read()
    codec = None

    for bom, encoding in bom_map.items():
        if data.startswith(bom):
            data,codec = data[len(bom):],encoding
            break

    if codec:
        data = data.decode(codec)
        lnsep = detect_line_ending_char(data)
        data = data.split(lnsep)
        return data,codec,lnsep

    for codec in codecs_no_bom:
        try:
            data = data.decode(codec)
            lnsep = detect_line_ending_char(data)
            data = data.split(lnsep)
            return data,codec,lnsep
        except: pass

    raise UnicodeError


def write_UTF8(path,codec,lnsep,data):
    file = open(path,"wb")
    data = lnsep.join(data).encode(codec)
    if codec in rev_bom_map:
        bom = rev_bom_map[codec]
        data = bom+data
    file.write(data); file.close()

