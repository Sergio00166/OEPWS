#Code by Sergio1260

from pygame.mixer import music
from pygame.mixer import init
from os.path import isfile
from colors import color
from sys import path
from os import system as cmd
from os.path import exists
from glob import glob
from sys import path
from random import randint
from threading import Thread
from time import sleep as delay
from subprocess import check_output
import wave
import msvcrt

try: len(ext)
except:
    temp=str(check_output("echo %temp%", shell=True))
    temp=temp[2:len(temp)-5].replace("\\\\","\\")
    ext=temp+"\\mp3tmp"+str(randint(0000,9999))+".wav"
    pause=False; init()

def wav_leght(file):
    with wave.open(file, 'rb') as file:
        return file.getnframes()/file.getframerate()

def timeformat(sec):
    hour=sec//3600
    if hour > 0: out += str(hour)+":"
    return str((sec%3600)//60,)+":"+"{:02d}".format(sec%60)

def countwk(ext):
    global offset, loop, status, kill, music, length, pause
    status=False; kill=False
    length=int(wav_leght(ext))
    while not kill:
        delay(0.1); time=int(music.get_pos()/1000)
        if status: progress_bar(time-offset,length)
        if not pause and not music.get_busy():
            if loop:
                while not kill:
                    try: music.play(); offset=0; break
                    except: pass
            else:
                if status: progress_bar(0,length)
                try: 
                    music.play()
                    music.pause()
                    pause=True
                except: pass
                offset=0
            
def progress_bar(current_value, max_value, bar_length=50):
    global lenbar
    progress = current_value / max_value
    filled_length = int(bar_length * progress)
    bar = '#' * filled_length + '-' * (bar_length - filled_length)
    out=f'  [{bar}]   '+timeformat(current_value)+" - "+timeformat(max_value)
    lenbar=len(out); print(out+"     ", end="\r")
   
def mp3(arg,arg1,directory):
    global offset, loop, status, counter
    global kill, pause, lenbar, music, length
    try:
        if arg1=="-quit":
            try:
                music.unload(); music.stop()
                cmd("DEL /F /A "+temp+"\\mp3tmp*.wav >nul 2>nul")
                kill=True; counter.join()
            except: pass
            
        elif arg1=="-pause":
            if pause: pause=False; music.unpause()
            else: pause=True; music.pause()
            
        elif arg1=="" and music.get_busy():
            status=True
            while True:
                key=msvcrt.getch()
                time=int(music.get_pos()/1000)
                if key == b'a' and music.get_busy():
                    offset+=1
                    if (time-offset)<0: offset=time
                    try: music.set_pos(time-offset)
                    except: pass
                if key == b's' and not time-offset==length:
                    offset-=1
                    try: music.set_pos(time-offset)
                    except: pass
                if key == b'q':
                    status=False
                    print("\r"+" "*lenbar)
                    break
                if key == b'w':
                    if pause: pause=False; music.unpause()
                    else: pause=True; music.pause()
                    
        if "-vol" in arg1:
            find="-vol"
            vol=arg1[arg1.find(find)+len(find)+1:]
            if " -loop" in vol: vol=vol[:vol.find("-loop")]
            if " -file" in vol: vol=vol[:vol.find(" ")]
            music.set_volume(int(vol)/100)
            
        if "-file" in arg1:
            find="-file"; init()
            args=arg1[:arg1.find(find)]
            if "-loop" in args: loop=True
            else: loop=False
            drt=arg1[arg1.find(find)+len(find)+1:]
            drt=drt.lstrip().rstrip()
            if not ":" in drt: direct = str(directory + drt)
            else: direct = drt
            direct=direct.replace("[","?").replace("]","?")
            file=glob(direct, recursive=False)
            if not len(file)==0:
                file=file[0]
                if isfile(file):
                    music.unload(); music.stop()
                    if exists(ext): cmd("DEL /F /A "+ext)
                    if cmd("ffmpeg -h 2>nul >nul")==0:
                        if not cmd('ffmpeg -loglevel quiet -i "'+file+'" "'+ext+'"')==1:
                            kill=True
                            try: counter.join()
                            except: pass
                            music.load(ext); music.play(loops=0)
                            counter=Thread(target=countwk, args=(ext,))
                            offset=0; counter.start(); pause=False
                    else: print(color("\n   FFMPEG is needed\n","R"))
                else: print(color("\n   It isn't a valid file\n","R"))
            else: print(color("\n   File not found\n","R"))
    except: print(color("\n   Error\n","R"))
