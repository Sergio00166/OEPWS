#Code by Sergio1260

from glob import glob

def main(arg,directory):
    try:
        separator="::"; ext=arg.find("] ")
        command=arg[ext+1:]; other=arg[:ext]
        ext=other.split("]::")
        for x in ext:
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
                for z in fix: out.append(z.replace("\\","\\\\"))
                
            elif varname=="list": out=value.split(",")
            elif varname=="range":
                value=value.split(",");out=[]
                if len(value)==1: fix=range(int(value[0])+1)
                elif len(value)==2: fix=range(int(value[0]),int(value[1])+1)
                else: fix=range(int(value[0]),int(value[1]),int(value[0])+1)
                for x in fix: out.append(str(x))
            while f"<{name}>" in command:
                args=command[command.find("{")+1:command.find("}")]
                cmd=command[:command.find(" ")]
                arg1=args[:args.find(f"<{name}>")]; ext=[]
                arg2=args[args.find(f"<{name}>")+len(name)+2:]
                for x in out: ext.append(arg1+x+arg2)
                output=separator.join(ext)
                command=command.replace("{"+f"{arg1}<{name}>{arg2}"+"}",output)
    except: command=arg
    return command
        
