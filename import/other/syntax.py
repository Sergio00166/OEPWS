# Code by Sergio1260

from os.path import join, isabs
from re import findall

def parser(text, keywords):
    try:
        pattern = r"'([^']+)'|(\b\w+\b)"
        matches = findall(pattern, text)
        keyword_indices = []
        for keyword in keywords:
            for i, match in enumerate(matches):
                if match[1] == keyword:
                    keyword_indices.append(i)
                    break
        if keyword_indices != sorted(keyword_indices): raise SyntaxError
        parsed_groups = []; start_index = 0
        for index in keyword_indices:
            before_keyword = [match[0] for match in matches[start_index:index] if match[0]]
            parsed_groups.append(before_keyword)
            start_index = index + 1
        after_last_keyword = [match[0] for match in matches[start_index:] if match[0]]
        parsed_groups.append(after_last_keyword)

        return parsed_groups
    
    except: raise SyntaxError


def parse_syntax(code, directory, mode=["from", "to"]):
    # Example
    # If second mode is None
    # read "file" from "path"
    # If second mode is "to"
    # copy "file" from "path" to "destination"

    mode = [mode[0], mode[1]] if not mode[1]==None else [mode[0]]
    try:
        code = parser(code, mode)
        arg = code[0]; lenght=len(code); lenm=len(mode)
        if lenm>1:
            from_arg=code[1][0] if lenght>2 else directory
            if lenght>2: to = code[2]
            elif lenght==1: arg=code[0]
            else: to = code[1]
        else: from_arg=code[1][0] if lenght>1 else directory
        if not isabs(from_arg): from_arg = join(directory, from_arg)
        if len(arg)==0: arg=[""]
        out = [x if isabs(x) else join(from_arg, x) for x in arg]
        if lenm>1: return out, [x if isabs(x) else join(directory, x) for x in to]
        else: return out
    except: raise SyntaxError

def parse_basic_syntax(code, directory, mode="in"):
    sep="' "+mode+" '"
    try:
        if sep in code:
            code=code.split(sep);args=code[0][1:]
            file=code[1][:-1].split("' '")
        else: args=code[1:-1]; file=[directory]
        args=args.split("' '")
        return args, file
    except: raise SyntaxError

