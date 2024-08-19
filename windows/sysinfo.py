#Code by Sergio00166

from sys import path
from subprocess import check_output
from threading import Thread

def async_worker():
    global line
    import psutil
    from other import readable
    from colors import color
    line=[]
    green=color("","Gnr"); blue=color("","Bnr"); reset=color()
    ram=psutil.virtual_memory().total
    vram=psutil.swap_memory().total
    ram=color(readable(ram),"B")
    vram=color(readable(vram),"B")
    disk=psutil.disk_usage("C:\\")
    size=color(readable(disk.total),"B")
    free=color(readable(disk.free),"B")
    ram_info="RAM:   "+reset+ram+"  "+green+"   Swap:  "+reset+vram
    storage=color("Total ","Y")+reset+size+" "+color("   Free ","Y")+reset+free+" "
    line.append(blue+"        ▄▄▄▄▄▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄▄▄▄▄▄         "+green+"OS:    "+reset)
    line.append(blue+"        ████████████ ████████████         "+green+"Ver:   "+reset);line.append(green+"     Uptime:  "+reset)
    line.append(blue+"        ████████████ ████████████         "+green+"Host:  "+reset)
    line.append(blue+"        ████████████ ████████████         "+green+"Mfr:   "+reset)
    line.append(blue+"        ████████████ ████████████         "+green+"Model: "+reset)
    line.append(blue+"        ▄▄▄▄▄▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄▄▄▄▄▄         "+green+"CPU:   "+reset)
    line.append(blue+"        ████████████ ████████████         "+green+ram_info)
    line.append(blue+"        ████████████ ████████████         "+green+"C:\\    "+reset+storage)
    line.append(blue+"        ████████████ ████████████         "+green+"BIOS:  "+reset)
    line.append(blue+"        ████████████ ████████████         "+green+"TZ:    "+reset); line.append(green+"   Lang: "+reset)
    line.append(blue+"           MICROSOFT WINDOWS™             "+green+"GPUs:  "+reset)

    
def sysinfo():
    global line
    thr=Thread(target=async_worker); thr.start()
    file=path[0]+"\\import\\powershell\\sysinfo.ps1"
    raw=str(check_output("powershell -noprofile -executionpolicy bypass -file "+file), encoding="cp857")
    raw=raw[:len(raw)-1]
    raw=raw.split("\r\n")
    tz=raw[9]; tz=tz[:tz.find(")")+1]
    thr.join()
    out="\n"+line[0]+raw[1]+"\n"+line[1]+raw[2]+line[2]+raw[3]+"\n"+line[3]+raw[0]
    out+="\n"+line[4]+raw[4]+"\n"+line[5]+raw[5]+"\n"+line[6]+raw[6]+"\n"+line[7]
    out+="\n"+line[8]+"\n"+line[9]+raw[8]+"  /|"+raw[7]+"|\\\n"+line[10]+tz
    out+=line[11]+raw[10]+"\n"+line[12]+raw[11]
    if not len(raw)<12:
        for x in range(12,len(raw)): out+=" "*50+str(raw[x])
    print(out+"\n\n")
