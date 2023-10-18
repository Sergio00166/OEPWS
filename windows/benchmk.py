#Code by Sergio1260

import random
from multiprocessing import cpu_count, Process, Pool
from time import time
from time import sleep as delay
from colors import color

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

def generate_additional_points(initial_point, num_points):
    for _ in range(num_points):
        random_vertex = random.choice([(0, 0), (1, 0), (0.5, 0.866)])
        new_point_x = (initial_point[0] + random_vertex[0]) / 2
        new_point_y = (initial_point[1] + random_vertex[1]) / 2
        initial_point = (new_point_x, new_point_y)

def generate_parallel_points(num_processes, num_additional_points):
    initial_points = [generate_random_point() for _ in range(num_processes)]
    processes = []
    for i in range(num_processes):
        initial_point = initial_points[i]
        process = Process(target=generate_additional_points, args=(initial_point, num_additional_points))
        process.start()
        processes.append(process)
    start=time()
    for process in processes: process.join()
    end=time(); return end-start
    
def run(cores, sizef):
    global size, start ; size=sizef
    points=int((size*size)/cores)
    return generate_parallel_points(cores, points)

#0.7 is the offset to match te score of CPU-Z benchmark
def one_core(): return int(1/(run(1, 5120)*13)*100000*0.7)
def all_cores(): return int(1/run(cpu_count(), 16384)*100000*0.7)

def main():
    delay(0.5); print(""); prog=""; percent=0
    print("     "+color("  Python SysBench v3.0 ","bW"),end="\n\n")
    print("\r  Running Single-Core benchmark... ",end="")
    onec=str(one_core())
    print(color("DONE","B"),end="")
    delay(1)
    print("\r"+" "*64,end="")
    print("\r  Running Multi-Core benchmark... ",end="")
    allc=str(all_cores())
    print(color("DONE","B"),end="")
    delay(1)
    print("\r"+" "*64,end="")
    print("\r      Printing results... ",end="")
    delay(1.5)
    print(color("\r   Single-Core performance: ","B")+color(onec,"G")
          +"                                          ")
    print(color("   Multi-Core  performance: ","B")+color(allc,"G"))
    print("")

