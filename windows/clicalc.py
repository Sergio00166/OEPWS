#Code by Sergio1260

from os import system as cmd
from sys import path
import math
math = {x:getattr(math, x) for x in dir(math)}
from math import *

def fix(code):
    import ast
    banned_functions = {'print', 'exit', 'quit', 'exec', 'eval', 'input'}
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and (isinstance(node.func, ast.Name) and node.func.id in banned_functions): return False
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                for name in node.names:
                    module_name = name.name.split('.')[0]
                    if module_name in banned_modules: return False
        return True
    except SyntaxError: return False

def init():
    global letras, operaprt, error, resultprt
    from colors import color
    letras={":a":0,":b":0,":c":0,":d":0}
    operaprt=(str(color("\n Operation: ","G-") + color()))
    error=str(color("\n   Error","R"))
    resultprt=str(color("\n  Result: ","B"))
   
def work(arg,mode):
    global letras, operaprt, error, resultprt, buffer
    for x in letras: arg=arg.replace(x,str(letras[x]))
    arg=arg.replace("Ans",str(buffer))
    arg=arg.replace('"',"'")
    if fix(arg):
        try:
            result=eval(arg,{},math)
            if type(result)==type(print):
                result=None
        except: result=None
    else: result=None
    if mode==1: print(resultprt+str(result)); buffer=result
    elif mode==2: return result
    
def main(arg1=False):
    global letras, buffer
    init(); buffer=0
    while True:
        if arg1==False:
            print(operaprt,end="")
            arg=input()
        else: arg=arg1
        if arg=="exit": print(""); break
        elif arg=="clear": cmd("CLS")
        elif arg=="flush": letras={":a":0,":b":0,":c":0,":d":0}
        else:
            if "set" in arg:
                letra=arg[arg.find("set(")+4:arg.find(")")]
                for x in letras:
                    if x.replace(":","")==letra:
                        letras[x]=work(arg.replace("set("+letra+") ",""),2)
            else: work(arg,1)

        if arg1!=False: print(""); break

if __name__=="__main__":
    path.append(path[0]+chr(92)+"..\\import")
    main()
