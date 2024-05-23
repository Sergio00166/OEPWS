# pBTE
python-based Basic Text Editor

A a basic terminal text editor with python using the minimun external libraries as possible (only wcwidth and colorama) 

Nowadays it is in development stage, then it can be expected to be broken

Basic functionalities currently available such as copy, cut, paste lines, and the basic for a text editor

Due to limitations with msvcrt.getch() on windows to select (highlight) lines you must use Ctrl+arrows instead of Shift+arrows 

Requirements:<br>
Python 3 (tested under python 3.12)<br>
No dependencies<br>
Windows, with UTF-8 mode<br> (tested under win11)
Also now "works" under linux (tested under FEDORA and UBUNTU)

<br><h2>OPTIONS</h2>
<br>*NORMAL*<br>
^E EXIT | ^S SAVE | ^A Save as | ^O OPEN | ^C COPY | ^X CUT | ^P PASTE | ^G GOTO | ^T T/SP <br>
<br>*Open file menu*<br>
^C CANCEL | ^O OPEN  | ^N NEW FILE <br>
<br>*Save as menu*<br>
^C CANCEL | ^S SAVE | ^B BACKUP | ^A APPEND | ^P PREPEND
<br>
