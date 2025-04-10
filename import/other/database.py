#Code by Sergio00166

from colors import color
from multiprocessing import Process, Queue
try:
    from mp3 import mp3
    mp3loaded=True
except: mp3loaded=False
    
dic={"directory":["go","cd","eject","flmgr"],"files":["when","new","no","write","flush","chmod","chown","lsacl"],
     "users":["su","sudo","root","deluser","lsusr","addgroup","delgroup","lsgrp"],
     "extras":["speedtest","pwdgen","weather","drives","restart","shutdown","repair","time","flushdns","kill","print","mem"]}

def slc(arg,arg1):
    try: dic[arg].index(arg1); return True
    except: return False

def cmd(arg,arg1,directory,oldir, out):
    status=True
    if slc("directory",arg):
        from direct import direct
        directory=direct(arg,arg1,directory,oldir)
    elif slc("files",arg):
        from files import files
        files(arg,arg1,directory)
    elif slc("users",arg):
        from users import users
        users(arg,arg1,directory)
    elif slc("extras",arg):
        from extras import extras
        extras(arg,arg1,directory)
    else:
        from things import things
        status=things(arg,arg1,directory)
    out.put([directory,status])
      
def database(arg,arg1,directory,oldir):
    global mp3loaded, mp3
    try:
        if arg=="adduser":
            from users import add_user
            add_user(arg1)
        elif arg=="mp3":
            if mp3loaded: mp3(arg,arg1,directory)
            else:
                try:
                    from mp3 import mp3
                    mp3loaded=True
                    mp3(arg,arg1,directory)
                except:
                    print(color("\n    Cannot load mp3\n","R"))
                    mp3loaded=False
        else:
            out=Queue()
            proc=Process(target=cmd, args=(arg,arg1,directory,oldir,out,))
            proc.start(); ext=out.get(); proc.join(); directory=ext[0]
            if not (ext[1]==None or ext[1]):
                from startcmd import main as runcmd
                if runcmd(arg, arg1, directory):
                    print(color("\n  Command not found","R"))
                print("")
            out.close()
        return directory
    except KeyboardInterrupt:
        out.close()
        proc.terminate()
        return directory
