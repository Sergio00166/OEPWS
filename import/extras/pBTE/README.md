# pBTE 
python-based Basic Text Editor     

A a basic text editor with python using the minimun external libraries as possible.    
Only supports UTF-8 and UTF-16 (with or wihout BOM [LE/BE]) and ASCII (for reading bin files).    

It will autodetect encoding and linesep, but you can change any time (affects only when saving)    
with ^T and the S or L to change the charset and the linesep.    
The default encoding for blank files is UTF-8 and defaults to use LF.    

Using colorama and wcwidth (they are inside lib.zip) and its LICENSES can be found inside that zip file.    
Basic functionalities currently available such as copy, cut, paste lines, find string, and replaced string.   
Currently ctrl+Z is not available a workaround is using ctrl+a and then ctrl+b to create a .bak file  

-----------------------------------

### KEYBINDS

#### Main Mode:
- `^Q` [Quit],      `^T` [Main Setting Menu]
- `^S` [Save],      `^A` [Save as]
- `^O` [Open],      `^C` [Copy]
- `^X` [Cut],       `^P` [Paste]
- `^G` [GOTO],      `^D` [Dedent]
- `^I` [Indent],    `^K` [Comment]
- `^U` [Uncomment], `^F` [Find]
- `^R` [Replace],   `^J` [non-move NL]

#### OpenFile Menu:
- `^C` [Exit], `^O` [Open file]
- `Tab`/`Ret` [For autocomplete filenames]
- `^N` [New empty file]

#### SaveAs Menu:
- `^C` [Exit], `^S` [Save file]
- `Tab`/`Ret` [For autocomplete filenames]
- `^B` [BackUp], `^A` [Append], `^P` [Prepend]

#### Find Menu:
- `^C` [Exit]
- `<-` [Previous one]
- `->` [Next one]

#### Replace Menu:
- `^C` [Exit]
- `^A` [Replace all]
- `<-` [Previous one]
- `->` [Next one]
