#Code by Sergio1260

from sys import path
from subprocess import check_output
from colors import color
import psutil
from other import readable

def sysinfo():
    try:
        green=color("","Gnr"); blue=color("","Bnr"); reset=color()
        file=path[0]+"\\import\\powershell\\sysinfo.ps1"
        raw=str(check_output("powershell Set-ExecutionPolicy -Scope CurrentUser "+
                             "-ExecutionPolicy Bypass -Force; "+file), encoding="cp857")
        raw=raw[:len(raw)-1]
        raw=raw.split("\r\n")

        raw.pop(8);raw.pop(9); cpu=raw[8]
        tz=raw[11]; tz=tz[:tz.find(")")+1]

        disk=psutil.disk_usage("C:\\")
        size=color(readable(disk.total),"B")
        free=color(readable(disk.free),"B")

        ram=psutil.virtual_memory().total
        vram=psutil.swap_memory().total
        ram=color(readable(ram),"B")
        vram=color(readable(vram),"B")
        
        storage=color("Total ","Y")+reset+size+" "+color("   Free ","Y")+reset+free+" "
        
        print("")
        print(blue+"                                          "+green+"Host:   "+reset+raw[0])
        print(blue+"        ▄▄▄▄▄▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄▄▄▄▄▄         "+green+"OS:     "+reset+raw[1])
        print(blue+"        ████████████ ████████████         "+green+"Ver:    "+reset+raw[2]+green+"    Uptime:  "+reset+raw[3])
        print(blue+"        ████████████ ████████████         "+green+"Owner:  "+reset+raw[4])
        print(blue+"        ████████████ ████████████         "+green+"WkGrp:  "+reset+raw[5])
        print(blue+"        ████████████ ████████████         "+green+"Mfr:    "+reset+raw[6])
        print(blue+"        ▄▄▄▄▄▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄▄▄▄▄▄         "+green+"Model:  "+reset+raw[7])
        print(blue+"        ████████████ ████████████         "+green+"CPU:    "+reset+cpu)
        print(blue+"        ████████████ ████████████         "+green+"RAM:    "+reset+ram+"  "+green+"    Swap:  "+reset+vram)
        print(blue+"        ████████████ ████████████         "+green+"Disk C: "+reset+storage)
        print(blue+"        ████████████ ████████████         "+green+"BIOS:   "+reset+raw[9]+" ("+raw[10]+")")
        print(blue+"                                          "+green+"TZ:     "+reset+tz+green+"   Lang: "+reset+raw[12])
        print(blue+"                                          "+green+"GPUs:   "+reset+raw[13])
        
        if not len(raw)<14:
            for x in range(14,len(raw)): print(" "*50+str(raw[x]))
        print("")
        
    except: print(color("\n   Error\n","R"))
