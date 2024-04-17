from extra import main as bench
from sys import argv
from time import sleep as delay
from multiprocessing import cpu_count
import random
from multiprocessing import cpu_count, Process, Pool
from time import time
from sys import argv


class stress:
    
    @staticmethod
    def generate_random_point():
        vertices = [(0, 0), (1, 0), (0.5, 0.866)]
        vertex = random.choice(vertices)
        r1 = random.random()
        r2 = random.random()
        if r1 + r2 >= 1:
            r1 = 1 - r1
            r2 = 1 - r2
        point_x = vertex[0] * (1 - r1 - r2) + vertices[(vertices.index(vertex) + 1) % 3][0] * r1 + vertices[(vertices.index(vertex) + 2) % 3][0] * r2
        point_y = vertex[1] * (1 - r1 - r2) + vertices[(vertices.index(vertex) + 1) % 3][1] * r1 + vertices[(vertices.index(vertex) + 2) % 3][1] * r2
        return point_x, point_y
    
    @staticmethod
    def generate_additional_points(initial_point, range):
        for _ in range:
            random_vertex = random.choice([(0, 0), (1, 0), (0.5, 0.866)])
            new_point_x = (initial_point[0] + random_vertex[0]) / 2
            new_point_y = (initial_point[1] + random_vertex[1]) / 2
            initial_point = (new_point_x, new_point_y)
            
    @staticmethod
    def generate_parallel_points(num_processes, num_additional_points):
        initial_points = [stress.generate_random_point() for _ in range(num_processes)]
        processes = []
        for i in range(num_processes):
            initial_point = initial_points[i]
            process = Process(target=stress.generate_additional_points, args=(initial_point, num_additional_points))
            process.start()
            processes.append(process)
        start=time()
        for process in processes: process.join()
        end=time(); return end-start

    @staticmethod
    def worker():
        initial_point=stress.generate_random_point()
        stress.generate_additional_points(initial_point, iter(int,1))
        
    @staticmethod
    def main():
        proc=[]
        print("\n   PYTHON BASED CPU STRESS-TEST\n")
        delay(0.33)
        print("STARTING...",end="\r")
        for _ in range(cpu_count()):
            proc.append(Process(target=stress.worker))
        for x in proc: x.start()
        delay(2)
        input("RUNNING. Press any key to stop . . .  ")
        for x in proc: x.terminate()
        print("")


def benchmark():
    delay(0.5); print(""); prog=""; percent=0
    print("      Python SysBench v4.1 ",end="\n\n")
    print("\r  Running Single-Core benchmark... ",end="")
    onec=int(bench(True,1))
    print("DONE",end="");  delay(1)
    print("\r"+" "*64,end="")
    print("\r  Running Multi-Core benchmark... ",end="")
    allc=int(bench(True,cpu_count()))
    print("DONE",end="")
    delay(0.5)
    print("\r"+" "*64+"\r      Printing results... ",end="")
    delay(1)
    print("\r   Single-Core performance: "+str(onec)+" "*42)
    print("\r   Multi-Core  performance: "+str(allc)+"\n")
    

if __name__=="__main__":
    if not len(argv)==1:
        arg=argv[1]
        if arg=="stress":
            stress.main()
        elif arg=="bench":
            benchmark()
        else: print("\n   BAD ARGUMENT\n")
    else: benchmark()
