import pycxsimulator
import numpy as np
import matplotlib
import matplotlib.pyplot as plt 

matplotlib.use("TkAgg")

n = 100
p0 = 0.0001

r = 2
k = 4*int(r)+1
states = 4 #0: quiescent, 4: active, 3~1: refractory

for x in range(1,int(r)+1):
    for y in range(1,int(r)+1):
        if np.sqrt(x**2+y**2)<=r:
            k+=4

def initialize():
    #np.random.seed(0)
    global config, nextconfig
    #config = np.zeros((n,n),dtype=int)
    config = states*((np.random.random((n,n))<=p0).astype(int))
    nextconfig = np.zeros((n,n),dtype=int)

def observe():
    global config
    plt.cla()
    plt.imshow(config,vmin=0,vmax=states,cmap="bone")

def update():
    global config, nextconfig
    nextconfig = np.zeros((n,n),dtype=int)
    for x in range(config.shape[0]):
        for y in range(config.shape[1]):
            if config[x,y]==0:
                nextconfig[x,y] = states if np.random.rand()<=p0+np.tanh(count_Moore(config,x,y,r,n)/k) else 0
            else:
                nextconfig[x,y] = config[x,y]-1
    not_finished = False if (config==nextconfig).all() else True
    config = nextconfig
    return not_finished

def count_Moore(config,x,y,r=r,n=n):
    count = 0
    for dx in range(-int(r),int(r)+1):
        for dy in range(-int(r),int(r)+1):
            if config[(x+dx)%n,(y+dy)%n] == states:
                count += config[(x+dx)%n,(y+dy)%n]
    return count

pycxsimulator.GUI(parameterSetters = []).start(func=[initialize,observe,update])
