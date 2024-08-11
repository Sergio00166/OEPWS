#OEPWS

<h2>NOT LONGER WORKING ON THIS</h2>

Open simplE Python-based Windows Shell

A Windows 'shell' with its own simple syntax

Includes my pBTE custom text editor and my pySysBench CPU stability and benchmark tool

And if you write native windows commands "works".<br>
Write # before the command and it will executed on the windows native cmd

Extra: if you type the name of an executable without the .exe, this shell will look for it and execute it with the commands provided via CLI

----------------------------------

      alpha v0.1.70.2

      Updated secondary modules (pBTE and pySysBench)
      
---------------------------------------------------------------------------

Includes third-party software:  <a href="https://github.com/aristocratos/btop4win">btop4windows (aristocratos)</a>, and speedtest

---------------------------------------------------------------------------

Requieres Python 3.12<br>
UTF-8 support (requires the 'Beta: Use Unicode UTF-8 for worldwide language support' option in Windows Region Settings.)<br>

Recomended to use with Windows Terminal, in the "import" directory there are a file named 
"WinTermADD.py" allowing you to install a profile in the Windows Terminal easily

---------------------------------------------------------------------------

*Syntax:*

Separators are "::", allowing to use all types of system accepted characters without limitation<br>
Example *copy test::Users\\test2 from C:\ to D:\\::E:\\folder* <br>
and also you can use "from"/"in" to indicate where are the files/dir and "to" to indicate the destination
<br><br>
Using ";" like linux cli and when using ""+commands using "&"
<br><br>
*loop variables*<br>
{separator}\<varname\>[operation(args)] command {text1\<varname\>text2}text3<br>
it concatenates the output from the operation() with the separator <br>
(if not specified, the default is "::") and combines each occurency with the text1 and text2<br>
text3 is not affected because it isnt inside {}.<br>
Current supported operations: ls, list, range, file<br>
Example of use:<br>
{\n}\<var\>[ls()] print {\<var\>}<br>
Print every file inside the current path
<br><br>
*Enviorment variables*

$dir > refers to the actual directory <br>
$ver > refers to the current version<br>
$ + name > refers to the native enviorment variable from windows cmd

---------------------------------------------------------------------------

To run an file on the current dir you need to put .\ before the file name (you can use * and ? in the filename)<br><br>

*root* <br>
(+ su) starts command prompt as root <br>
(+ command) runs command as root (NT authority System) <br>
<br><br>
*sudo* <br>
(+ su) starts command prompt as admin <br>
(+ command) runs command as admin <br>
<br><br>
*sort(mode)* file (in path)<br>
Sorts by the mode the contents of the dir <br>
Modes: mtime, ctime, size, alpha (alphabetical)<br><br>
*where* file (in path)<br>
prints when the file/dir was modified and created <br><br>
*flmgr*<br>
Terminal based file manager (FL)
<br><br>
*perfmon*<br>
Terminal based performance monitor and task manager (btop4windows)
<br><br>
*go* dir (GO to dir) <br>
Options back prev down <br>
same as cd but only with absolute paths <br>
go back <br>
same as cd .. but you can use go back 4 that is the same as cd ..\\..\\..\\..\\ <br>
go prev <br>
changes the path to the previous path <br>
go down <br>
It goes along the route backwards until you find the part with the same name as the argument <br>
Example your are in C:\Users\test\Documents\folder\folder1\ and if you want to go directly to "test" you can use
go down test and the result path will be C:\Users\test\ <br>
extra: with "go .\\" the actual path changes to the location of the terminal files 
<br><br>
*cd* dir <br>
go to upper directory
<br><br>
*downdir* dir <br>
you can go to any directory in the current path by putting only its name
<br><br>
write -flush to file [some text \n and other line]
<br><br>
flush file
<br><br>
*new* name <br>
creates a new empty file or directorory <br>
to create a file: new filename <br>
to create a dir: new dirname\\ <br>
<br><br>
*no* name <br>
deletes a file or directory <br>
to delete a file: no filename <br>
to delete a dir: no dirname\\ <br>
<br><br>
*read* file <br>
prints the content of the especified file<br>
Options:<br>
readn (No counter) disables the line counter<br>
readc (Concatenate) like linux cat command<br>
Important: -f can be used with -n or -c no -n -c at the same time<br> 
<br><br>
*ls* dir
<br><br>
*dirtree* dir <br>
makes a tree of the subdirs in a especific dir
<br><br>
*cal* this year month x <br>
year x this month <br>
year x month x <br>
today <br>
prints a calendar with the arguments 
<br><br>
*time* <br>
prints the hour
<br><br>
*copy* and *move* <br>
copy fich from path to path path2
<br><br>
*rmov* name from path to newname <br>
moves ONE file to ONE destination EACH
like rmov 1 2 to 1 2
moves 1 to 1 and 2 to 2
<br><br>
*edit* file from path <br>
edits the specified file with the nano editor
<br><br>
*locate* file/dir in path from  <br>
finds the specified file/dir in the path
locatenr (not recursive version)
<br><br>
*from* file in path find hello <br>
finds the word hello in the specified file
<br><br>
*link/links* lnkname in path to file in path <br>
creates a shorcut (link) or a symbolic link (links) <br>
<br><br>
*size* file <br>
prints the size of the file
<br><br>
*clear* <br>
clears the screen
<br><br>
app <br>
starts the app (located on the C: program files folders)
<br><br>
*ip*<br>
prints the ip config
<br><br>
*repair* <br>
repairs the system <br>
(sfc, dism.exe)
<br><br>
*perfmon*<br>
cli based task manager
<br><br>
*flushdns* <br>
clears the dns cache
<br><br>
*kill* proc <br>
kills a process
<br><br>
*calc* <br>
opens a cli calculator interface or returns the result of the args
<br><br>
*dskperf -read -write -mode -drive C*
mode can be rand or seq
<br><br>
*mp3 -file file.mp3* <br>
-pause -quit <br>
whith no args:<br>
      "q" quit<br>
      "a" decrese<br>
      "s" increase<br>
      "w" pause/unpause<br>
-vol 0-100 <br>
mp3 player
<br><br>
*exit* <br>
exits the program
<br><br>
*benchmk* <br>
cpu benchmark
<br><br>
*stress* <br>
cpu stress test
<br><br>
*weather City* <br>
shows the weather for the city
<br><br>
*su* user <br>
starts command prompt as a user especified <br>
<br><br>
*adduser* -sudo username <br>
add a user, whith -sudo the created user will have admin permisions
<br><br>
*deluser* username <br>
deletes a user
<br><br>
*chmod* <br>
changes file/dir permisions (ACL)
chmod [user1:r] for file -> <br>
chmod set(optional) [username:permisions] for filename/folder
<br><br>
*chown username for file* <br>
changes the owner of a file
<br><br>
*lsacl file* <br>
list the acl for a file
<br><br>
*eject* disk <br>
Unmounts the disc for safe extraction
<br><br>
*print/printf text* <br>
prints in the terminal "text"<br>
if printf, it will not use scaped chars like \r
<br><br>
*mem* <br>
prints the total/used/free physical memory
<br<br>
