# Code by Sergio1260

from os.path import join, isabs


def parse_basic_syntax(code, directory, mode="in"):

    sep = '" ' + mode + ' "'
    if sep in code:
        code = code.split(sep)
        args = code[0][1:]
        file = code[1][:-1]
        file = file.split('" "')
    else:
        args = code[1:-1]
        file = [directory]
    args = args.split('" "')
    
    return args, file


def parse_syntax(code, directory, mode=["from", "to"]):

    from_str = '" ' + mode[0] + ' "'
    dest_str = mode[1]
    if not dest_str == None:
        dest_str = '" ' + dest_str + ' "'

    try:
        is_from = from_str in code
        if is_from:
            code = code.split(from_str)
            arg = code[0]
            if not dest_str == None:
                code = code[1].split(dest_str)
                from_arg = code[0]
                to = code[1]
            else: from_arg = code[1][:-1]
            if not isabs(from_arg):
                from_arg = join(directory, from_arg)

        else:
            from_arg = directory
            if not dest_str == None:
                code = code.split(dest_str)
                arg = code[0]
                to = code[1]
            else: arg = code

        arg = arg.split('" "')
        arg[0] = arg[0][1:]
        out = []

        if dest_str == None and not is_from:
            arg[-1] = arg[-1][:-1]

        for x in arg:
            if isabs(x): out.append(x)
            else: out.append(join(from_arg, x))

        if not dest_str == None:
            to = to.split('" "')
            to[-1] = to[-1][:-1]
            out1 = []
            for x in to:
                if isabs(x): out1.append(x)
                else: out1.append(join(directory, x))
            return out, out1

        else: return out

    except: raise SyntaxError
