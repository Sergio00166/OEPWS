#Code by Sergio1260

from multiprocessing import Process
from time import sleep as delay
from msvcrt import getch

def proc(arg):
    def work(arg):
        data=("000000000000000000000000000000000"
              "000000000000000000000000000000000"
              "000000000000000000000000000000000"
              "000000000000000000000000000000000"
              "000000000000000000000000000000000"
              "000000000000000000000000000000000"
              "000000000000000000000000000000000"
              "000000000000000000000000000000000"
              "000000000000000000000000000000000"
              "000000000000000000000000000000000"
              "000000000000000000000000000000000"
              "000000000000000000000000000000000"
              "000000000000000000000000000000000"
              "000000000000000000000000000000000"
              "000000000000000000000000000000000"
              "000000000000000000000000000000000")
        dic=[]
        data=(data+data+data+data+data+data+data+data+data+data+
              data+data+data+data+data+data+data+data+data+data+
              data+data+data+data+data+data+data+data+data+data+
              data+data+data+data+data+data+data+data+data+data+
              data+data+data+data+data+data+data+data+data+data+
              data+data+data+data+data+data+data+data+data+data+
              data+data+data+data+data+data+data+data+data+data+
              data+data+data+data+data+data+data+data+data+data+
              data+data+data+data+data+data+data+data+data+data+
              data+data+data+data+data+data+data+data+data+data+
              data+data+data+data+data+data+data+data+data+data+
              data+data+data+data+data+data+data+data+data+data+data)
        while True:
            try:
                for x in range(0,int(int(arg)/8)):
                    dic.append(data)
                dic=[] 
            except: continue           
    work(arg)

def worker_mp(arg,cores):
    process=[]
    for x in range(0,int(cores)):
        thr=Process(target=proc, args=(arg,))
        process.append(thr)
    delay(3)
    for x in process: x.start()
    print("\n  Press any key to stop . . .  ", end="")
    getch(); print("\n")
    for x in process: x.terminate()

def main():
    size=int(virtual_memory().free*0.5/cpu_count())
    worker_mp(size,cpu_count())
    
