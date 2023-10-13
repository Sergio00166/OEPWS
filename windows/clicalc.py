#Code by Sergio1260

from sys import path
from math import *
from os import system as cmd

def init():
    from colors import color
    global letras, operaprt, error, resultprt, scadd
    letras={":a":0,":b":0,":c":0,":d":0}
    operaprt=(str(color("\n Operation: ","G-") + color()))
    error=str(color("\n   Error","R"))
    resultprt=str(color("\n  Result: ","B"))
    scadd=str(color("\n  Succesfully added: ","B"))
    
def work(arg,mode):
    global temp, letras, operaprt, error, resultprt, scadd, buffer
    for x in letras: arg=arg.replace(x,str(letras[x]))
    arg=arg.replace("Ans",str(buffer))
    arg=arg.replace('"',"'")
    if ("input(" in arg or "print(" in arg): print(error) 
    else:
        try: result=str(eval(arg))
        except: result=""
        if len(result)==0: print(error)
        elif mode==1:
            print(resultprt+str(result))
            buffer=result
        elif mode==2:
            print(scadd+str(result))
            try: float(result)
            except: result='"'+result+'"'
            return result
    
def main(arg1=False):
    global letras, buffer
    init()
    buffer=0; fix=False
    while True:
        if arg1==False:
            print(operaprt,end="")
            arg=input()
        else: arg=arg1
        if fix==True:
            work("",3)
            fix=False
        if arg=="exit": print(""); break
        elif arg=="clear": cmd("CLS")
        else:
            if "set" in arg:
                letra=arg[arg.find("set(")+4:arg.find(")")]
                for x in letras:
                    if x.replace(":","")==letra:
                        letras[x]=work(arg.replace("set("+letra+")",""),2)
                        fix=True        
            else: work(arg,1)

        if arg1!=False: print(""); break

if __name__=="__main__":
    path.append(path[0]+chr(92)+"..\\import")
    main()
