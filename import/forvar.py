#Code by Sergio1260

from glob import glob
from other import fixaddr
from colors import color

error=("\n  "+color("ForVar:","M")+" "+color("Error","R")+"\n")

def main(arg,directory):
    try:
        if arg.startswith("<") or arg.startswith("{"):
            if not ">[" in arg: print(error); return ""
            separator="::"; ext=arg.find("] ")
            command=arg[ext+1:]; x=arg[:ext]
            
            if x[0]=="{":
                separator=x[1:x.find("}<")]
                name=x[x.find("}<")+2:]
                var=name[name.find("[")+1:]
                name=name[:name.find(">")] 
            else:
                name=x[x.find("}<")+2:]
                var=name[name.find("[")+1:]
                name=name[:name.find(">")]
                
            value=var[var.find("(")+1:len(var)-1]
            varname=var[:var.find("(")]
            
            if varname=="ls":
                if value=="": value=directory
                elif not ":\\" in value:
                    value=directory+value
                if not value.endswith("\\"): value+="\\"
                fix=glob(value+"*", recursive=False); out=[]
                if not len(fix)==0:
                    for z in fix:
                        z=z.split("\\"); file=z[len(z)-1]
                        dirt=z[:len(z)-1]; dirt="\\".join(dirt)
                        dirt=fixaddr(dirt); fix=dirt+file
                        out.append(fix.replace("\\","\\\\"))
                else: print(error); return ""
            
            elif varname=="list": out=value.split(",")
            
            elif varname=="range":
                try:
                    value=value.split(","); out=[]; lenght=len(value)
                    if lenght==1: fix=range(int(value[0])+1)
                    elif lenght==2: fix=range(int(value[0]),int(value[1])+1)
                    elif lenght==3: fix=range(int(value[0]),int(value[1])+1,int(value[2]))
                    else: print(error); return ""
                    for x in fix: out.append(str(x))
                except: print(error); return ""
                
            elif varname=="file":
                out=[]
                try:
                    fix=open(value, "r", encoding="UTF-8").readlines()
                    for x in fix: out.append(x.replace("\\","\\\\"))
                except: print(error); return ""

            while "{" in command and "}" in command and "<" in command and ">" in command:
                args=command[command.find("{")+1:command.find("}")]
                cmd=command[:command.find(" ")]
                arg1=args[:args.find(f"<{name}>")]; ext=[]
                arg2=args[args.find(f"<{name}>")+len(name)+2:]
                for x in out: ext.append(arg1+x+arg2)
                output=separator.join(ext)
                command=command.replace("{"+f"{arg1}<{name}>{arg2}"+"}",output)
            return command
        else: return arg
    
    except: print(error); return ""

