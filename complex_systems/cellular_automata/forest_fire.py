import pycxsimulator
import numpy as np
import matplotlib
import matplotlib.pyplot as plt 

matplotlib.use("TkAgg")

n = 100
p0 = 0.618

r = 1
k = 4*int(r)+1
states = 3 #0: empty, 1: healthy, 2: burning, 3: charred

for x in range(1,int(r)+1):
    for y in range(1,int(r)+1):
        if np.sqrt(x**2+y**2)<=r:
            k+=4

def initialize():
    #np.random.seed(0)
    global config, nextconfig
    #config = np.zeros((n,n),dtype=int)
    config = ((np.random.random((n,n))<=p0).astype(int))
    config[int(n/2),int(n/2)]=2
    nextconfig = np.ones((n,n),dtype=int)

def observe():
    global config
    plt.cla()
    plt.imshow(config,vmin=0,vmax=2,cmap="binary")

def update():
    global config, nextconfig
    nextconfig = np.zeros((n,n),dtype=int)
    for x in range(config.shape[0]):
        for y in range(config.shape[1]):
            if config[x,y]==0:
                nextconfig[x,y] = 0
            elif config[x,y]==1:
                nextconfig[x,y] = 2 if count_vNeumann(config,x,y,2,r,n)>0 else 1
            else:
                nextconfig[x,y] = 3
            
    not_finished = False if (config==nextconfig).all() else True
    config = nextconfig
    return not_finished

def count_Moore(config,x,y,val,r=r,n=n):
    count = 0
    for dx in range(-int(r),int(r)+1):
        for dy in range(-int(r),int(r)+1):
            if config[(x+dx)%n,(y+dy)%n] == val:
                count += config[(x+dx)%n,(y+dy)%n]
    return count

def count_vNeumann(config,x,y,val,r=r,n=n):
    count = 0
    for dx in range(-int(r),int(r)+1):
        if config[(x+dx)%n,y] == val:
            count += config[(x+dx)%n,y]
        for dy in range(1,int(r)+1-np.abs(dx)):
            if config[(x+dx)%n,(y+dy)%n] == val:
                count += config[(x+dx)%n,(y+dy)%n]
            if config[(x+dx)%n,(y-dy)%n] == val:
                count += config[(x+dx)%n,(y-dy)%n]
    return count

pycxsimulator.GUI(parameterSetters = []).start(func=[initialize,observe,update])
