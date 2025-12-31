import pycxsimulator
import numpy as np
import matplotlib
import matplotlib.pyplot as plt 
from ca_funs import count_Moore, count_Radius

matplotlib.use("TkAgg")

n = 100
p0 = 0.3

Ra = 2
Ri = 6
wa = 8
wi = 1

def initialize():
    #np.random.seed(0)
    global config, nextconfig
    config = (np.random.random((n,n))<=p0).astype(int)
    nextconfig = np.zeros((n,n),dtype=int)

def observe():
    global config
    plt.cla()
    plt.imshow(config,vmin=0,vmax=1,cmap="binary")

def update():
    global config, nextconfig
    nextconfig = np.zeros((n,n),dtype=int)
    for x in range(config.shape[0]):
        for y in range(config.shape[1]):
            nextconfig[x,y] = 1 if wa*count_Radius(config,x,y,Ra)-wi*count_Radius(config,x,y,Ri)>0 else 0
    not_finished = False if (config==nextconfig).all() else True
    config = nextconfig
    return not_finished

pycxsimulator.GUI(parameterSetters = []).start(func=[initialize,observe,update])
