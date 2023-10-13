#Code by Sergio1260

from sys import path
from subprocess import check_output

qu=str(input("Install profile to Windows Terminal APP? Y/N "))
if qu.lower()=="y":
    qu=str(input("Add profile to default? Y/N "))
    if qu.lower()=="y":
        deft=True
    else: deft=False
    raw=str(check_output("echo %userprofile%",shell=True))
    userdir=raw[2:len(raw)-4].replace(chr(92)+chr(92),chr(92))
    fich=open(userdir+"AppData\\Local\\"+
              "Packages\\Microsoft.WindowsTerminal_"+
              "8wekyb3d8bbwe\\LocalState\\settings.json","r")
    fix=False; fic=""; path=path[0].replace(chr(92),chr(92)+chr(92))
    for x in fich:
        if '    "defaultProfile": "{' in x:
            if deft==True:
                fic+=('    "defaultProfile": "{c80fd1c4-95c3-47a2-960e-b5695956c081}",\n')
        else:
            fic+=x
            if x=="        [\n" and fix==False :
                fic+=('            {')+"\n"
                fic+=('                "antialiasingMode": "cleartype",')+"\n"
                fic+=('                "colorScheme": "Campbell",')+"\n"
                fic+=('                "commandline": "'+path+'\\\\fixcmd\\\\start.cmd",')+"\n"
                fic+=('                "cursorHeight": 16,')+"\n"
                fic+=('                "cursorShape": "vintage",')+"\n"
                fic+=('                "guid": "{c80fd1c4-95c3-47a2-960e-b5695956c081}",')+"\n"  
                fic+=('                "hidden": false,')+"\n"  
                fic+=('                "icon": "ms-appx:///ProfileIcons/{0caa0dad-35be-5f56-a8ff-afceeeaa6101}.png",')+"\n"  
                fic+=('                "name": "OEPWS shell",')+"\n"  
                fic+=('                "startingDirectory": "%USERPROFILE%",')+"\n"  
                fic+=('                "tabTitle": "OEPWS shell"')+"\n"
                fic+=('            },')+"\n"
                fix=True                 

    fich=open(userdir+"AppData\\Local\\"+
              "Packages\\Microsoft.WindowsTerminal_"+
              "8wekyb3d8bbwe\\LocalState\\settings.json","w")
    fich.write(fic)
    input("Press any key to exit . . .  ")
