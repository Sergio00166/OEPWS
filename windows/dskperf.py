#Code by Sergio00166

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
        if " -drive " in arg:
            fix=arg[arg.find(" -drive ")+8:]+":"
            drive=str(fix[:fix.find(" -")])
            arg=arg.replace(" -drive "+drive,"")
            drive=drive.replace(":","").replace(chr(92),"")
        else: drive=directory[:directory.find(":")]
        print("  "+color("         Benchmarking Drive: "+drive+"           ","bW"))
        print("")

        rmod  = "-read"  in arg
        wmod =  "-write" in arg
        rand  = "-rand"  in arg

        if not rmod and not wmod:
            rmod,wmod = True,True

        if rmod:
            if rand: read.rand(drive)
            else:    read.seq(drive)
        if wmod:
            if rand: write.rand(drive)
            else:    write.seq(drive)

    except: print(color("   This feature requires admin mode","R"))
    print("")
