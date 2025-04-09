#Code by Sergio00166

from glob import glob
from colors import color
from pathlib import Path
from other import fixaddr, fixcrdir
from syntax import parse_syntax

def worker(path, level=0, parent_is_last=[]):
    global blue, green, reset
    path = Path(path)
    files = sorted(path.glob("*"))
    total_files = len(files)
    for index, file in enumerate(files):
        spacing = ""
        for i in range(level):
            if i < len(parent_is_last) and parent_is_last[i]:
                spacing += "    "
            else:
                spacing += "│   "
        is_last_item = index == total_files - 1
        file_name = file.name
        if file.is_dir():
            prefix = "└── " if is_last_item else "├── "
            print("   " + spacing + prefix + blue + file_name + reset)
            worker(file, level + 1, parent_is_last + [is_last_item])
        else:
            prefix = "└── " if is_last_item else "├── "
            print("   " + spacing + prefix + green + file_name + reset)

def tree(arg1, directory):
    global blue, green, reset
    blue = color("", "Bnr")
    green = color("", "Gnr")
    reset = color()
    path = parse_syntax(arg1, directory, ["in", None])[0]
    if path.endswith(chr(92)): path = path[:-1]
    dirt = fixcrdir(path)
    if dirt != directory: dirt = dirt.replace(directory, "")
    if not path == None:
        print("\n   " + blue + dirt + reset)
        worker(path)
        print("")

# The rest of the code (print_files and ls) remains unchanged
