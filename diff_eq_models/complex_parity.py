import pycxsimulator
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random as rd

matplotlib.use("TkAgg")

n = 100

def count_Neumann(config,x,y):
    global n
    tempval = 0
    for dx in [-1,0,1]:
        tempval += config[(x+dx)%n,(y)%n]
    for dy in [-1,1]:
        tempval += config[(x)%n,(y+dy)%n]
    return tempval

def count_Moore(config,x,y):
    global n
    tempval = 0
    for dx in [-1,0,1]:
        for dy in [-1,0,1]:
            tempval += config[(x+dx)%n,(y+dy)%n]
    return tempval


def size_matrix(val = n):
    """
    Size of the matrix.
    """
    global n
    n = int(val)
    return val

def initialize():
    """
    CA using parity code and von Neumann neighborhood with r=1.
    """
    global n, config
    config = np.zeros((n,n))
    config[int(n/2),int(n/2)] = 1
    config[int(n/2)-1,int(n/2)] = 1
    config[int(n/2)+1,int(n/2)] = 1
    config[int(n/2),int(n/2)-1] = 1
    config[int(n/2),int(n/2)+1] = 1

def observe():
    global config
    plt.cla()
    plt.imshow(config,cmap="binary")

def update():
    global n, config
    temp_config = np.zeros((n,n))
    for x in range(config.shape[0]):
        for y in range(config.shape[1]):
            temp_config[x,y] = count_Neumann(config,x,y)%2
    config = temp_config



pycxsimulator.GUI(parameterSetters = [size_matrix]).start(func=[initialize,observe,update])