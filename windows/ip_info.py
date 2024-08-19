#Code by Sergio00166

import psutil
import socket
from subprocess import check_output
from colors import color

def get_gtw4():
    try:
        raw=str(check_output("route print 0.0.0.0"))
        raw=raw[raw.find("IPv4"):].split("\\r\\n")[4:]
        raw=raw[:raw.index("="*75)]; out=[]
        for x in raw:
            x=x.lstrip()
            while "  " in x: x=x.replace("  "," ")
            x=x.split(" "); out.append([x[3],x[2]])
        return out
    except: pass

def get_gtw6():
    try:
        raw=str(check_output("route print ::/0"))
        raw=raw[raw.find("IPv6"):].split("\\r\\n")[4:]
        raw=raw[:raw.index("="*75)]; out={}
        for x in raw:
            x=x.lstrip().replace("  "," ").split(" ")
            out[x[0]]=x[14]
        return out
    except: pass

def get_if_name():
    raw=str(check_output("route print 0.0.0.0"))
    raw=raw.split("\\r\\n")[2:]; adapters=[]
    for x in raw:
        value=x[:x.find(".")].lstrip()
        if "..........................." in x:
            out=[x[30:],value]
        elif not "=====" in x:
            adapters.append([x[30:],value])
        else:
            adapters.append(out)
            return adapters

def get_cidr_notation(netmask):
    bits = sum(bin(int(x)).count('1') for x in netmask.split('.'))
    return f'/{bits}'

def main():
    ifaces=get_if_name(); gtw4=get_gtw4(); gtw6=get_gtw6(); index=-1
    print("")
    for interface, addresses in psutil.net_if_addrs().items():
        print(color(" "+interface+" ","bW")); index+=1
        print(color("  altname ","R")+color(ifaces[index][0],"B-"))
        for addr in addresses:
            if addr.family == psutil.AF_LINK:
                print(color("  link/ether ","G")+color(addr.address,"B"))
            if addr.family == socket.AF_INET:
                cidr_notation = get_cidr_notation(addr.netmask)
                print(color("  inet ","G-")+color(addr.address,"B")+color(cidr_notation,"M"), end="")
                try:
                    for x in gtw4:
                        if x[0]==addr.address:
                            print(color(" gtw ","G")+color(x[1],"B"), end="")
                            gtw4.pop(gtw4.index(x)); break
                except: pass
                print("")
                try: print(color("  gtw6 ","G")+color(gtw6[ifaces[index][1]],"B"))
                except: pass
            if addr.family == socket.AF_INET6: print(color("  inet6 ","G-")+color(addr.address,"B"))
        print("")
