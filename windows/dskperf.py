#Code by Sergio1260

from subprocess import check_output
from colors import color
        
class read:
    def rand(drive):
        raw = str(check_output('WinSAT.exe disk -ran -read -drive '+drive+":", shell=False))
        raw=raw[516:]; output=raw[raw.find("Read")+4:]
        output=output[:output.find("/s")+2].replace(" ","")
        print(color("    Random Read Speed: ","B"),end="")
        print(color(output,"G"))
    def seq(drive):
        raw = str(check_output('WinSAT.exe disk -seq -read -drive '+drive+":", shell=False))
        raw=raw[522:]; output=raw[raw.find("Read")+4:]
        output=output[:output.find("/s")+2].replace(" ","")
        print(color("    Sequencial Read Speed: ","B"),end="")
        print(color(output,"G"))

class write:
    def rand(drive):
        raw = str(check_output('WinSAT.exe disk -ran -write -drive '+drive+":", shell=False))
        raw=raw[518:]; output=raw[raw.find("Write")+5:]
        output=output[:output.find("/s")+2].replace(" ","")
        print(color("    Random Write Speed: ","B"),end="")
        print(color(output,"G"))
    def seq(drive):
        raw = str(check_output('WinSAT.exe disk -seq -write -drive '+drive+":", shell=False))
        raw=raw[522:]; output=raw[raw.find("Write")+5:]
        output=output[:output.find("/s")+2].replace(" ","")
        print(color("    Sequencial Write Speed: ","B"),end="")
        print(color(output,"G"))

def main(arg,directory):
    print("")
    try:
        arg=" "+arg
        if " -drive " in arg:
            fix=arg[arg.find(" -drive ")+8:]+":"
            drive=str(fix[:fix.find(" -")])
            arg=arg.replace(" -drive "+drive,"")
            drive=drive.replace(":","").replace(chr(92),"")
        else: drive=directory[:directory.find(":")]
        print("  "+color("         Benchmarking Drive: "+drive+"           ","bW"))
        print("")
        if " -read " in arg and " -write " in arg and " -rand " in arg: read.rand(drive); write.rand(drive)
        elif " -read " in arg and " -write " in arg and " -seq " in arg: read.seq(drive); write.seq(drive)
        elif " -read " in arg and not " -write " in arg and " -rand " in arg: read.rand(drive)
        elif " -read " in arg and not " -write " in arg and " -seq " in arg: read.seq(drive)
        elif not " -read " in arg and " -write " in arg and " -rand " in arg: write.rand(drive)
        elif not " -read " in arg and " -write " in arg and " -seq " in arg: write.seq(drive)
        else:
            if " -rand" in arg:
                read.rand(drive); write.rand(drive)
            else: read.seq(drive); write.seq(drive)
    except OSError: print(color("   This feature requires admin mode","R"))
    except: pass
    print("")
