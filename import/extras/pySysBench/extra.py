from colorama import init, Back, Style, deinit
reset=Style.RESET_ALL; black=Back.WHITE+Style.DIM; deinit()
from time import sleep as delay
from copy import deepcopy
from multiprocessing import Pool, cpu_count
from functools import partial
from time import time

cube =\
[
    [[0, 192], [16, 192]],
    [[16, 192], [16, 202]],
    [[16, 202], [0, 202]],
    [[0, 192], [0, 202]]
]

margin =\
[
    [[0,0], [512,0]],
    [[0,0], [0,384]],
    [[512,0], [512,384]],
    [[0,384], [512,384]]    
]

vertex0 = [[[0, 197], [16, 197]]]
vertex1 = [[[0, 202], [16, 192]]]
vertex2 = [[[8, 192], [8, 202]]]
vertex3 = [[[0, 192], [16, 202]]]

def fill_polygon(vertex):
    points_between = []
    for i, (x1, y1) in enumerate(vertex):
        for x2, y2 in vertex[i + 1:]:
            dx, dy = x2 - x1, y2 - y1;
            fix=min(abs(dx), abs(dy))
            distance = max(abs(dx)-fix, abs(dy)-fix)
            if not distance == 0:
                points_between.extend([(round(x1 + k * dx / distance), round(y1 + k * dy / distance)) for k in range(distance + 1)])
    return points_between

def init_scr(x,y): return [[0]*(x+1) for _ in range(y+1)]
               
def refresh(vbuff,time=0,dump=False):
    screen=["".join([black+"  "+reset if x==1 else "  " for x in row]) for row in vbuff]
    screen="\r\033[%d;%dH"%(1, 1)+"\n".join(screen)
    if not dump: delay(time); print(screen,flush=True)
    else: return screen

def mid_points(vertex):
    x1, y1 = vertex[0]; x2, y2 = vertex[1]
    distance_x = x2-x1; distance_y = y2-y1
    num_points = max(abs(distance_x), abs(distance_y))
    step_x = distance_x / num_points
    step_y = distance_y / num_points
    return [(round(x1 + step_x * (i + 1)), round(y1 + step_y * (i + 1))) for i in range(num_points)]

def raster(vertex,vbuff,color=1, fill=False):
    buffer=deepcopy(vbuff)
    cords = list(set(tuple(coord) for sublist in vertex for coord in sublist))
    for x in vertex: cords+=mid_points(x)
    if fill: cords = fill_polygon(cords)
    for x in cords: buffer[x[1]][x[0]]=color
    return buffer

def wk(x,vbuff,ret):
    cube_moved = [ [[coord[0][0] + x, coord[0][1]], [coord[1][0] + x, coord[1][1]]] for coord in cube ]
    vbuff = raster(cube_moved, vbuff, fill=True)
    if not ret: return refresh(vbuff,dump=True)

def main(bench,proc):
    vbuff = init_scr(512, 384)
    vbuff=raster(margin,vbuff)
    blank=deepcopy(vbuff)
    x = 0; speed = 1
    cont=0; data = []
    while True:
        data.append(x)
        if x >= 512 - 16:
            speed = -1; cont+=1  
        elif x <= 0:
            speed = 1
            if cont>0: break
        x += speed
    pool=Pool(processes=proc)
    worker = partial(wk, vbuff=vbuff, ret=bench)
    if bench:
        passes=0; elapsed=0
        while True:
            proc=pool.map_async(worker,data)
            start=time(); proc.get(); passes+=1
            elapsed+=time()-start
            if elapsed>30:
                pool.close()
                return passes/elapsed*10000
    
    else: buffer=pool.map_async(worker,data).get()

    if not bench:
        pool.close()
        while True:
            for x in buffer: print(x)
                
if __name__=="__main__": main(False,cpu_count())
