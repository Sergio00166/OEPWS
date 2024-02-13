# Code by Sergio1260

from os import getcwd
from os.path import join, isabs


def parse_syntax(code, directory):
    try:
        
        if '" from "' in code:
            code=code.split('" from "')
            arg=code[0]
            code=code[1].split('" to "')
            from_arg=code[0]
            if not isabs(from_arg):
                from_arg=join(directory, from_arg)
            to=code[1]
            
        else:
            code=code.split('" to "')
            arg=code[0]
            from_arg=directory
            to=code[1]
            
        arg=arg.split('" "')
        to=to.split('" "')
        arg[0]=arg[0][1:]
        to[-1]=to[-1][:-1]
        out=[]; out1=[]
        
        for x in arg:
            if isabs(x): out.append(x)
            else: out.append(join(from_arg, x))

        for x in to:
            if isabs(x): out1.append(x)
            else: out1.append(join(directory, x))
        
        return out, out1
    
    except: raise SyntaxError
