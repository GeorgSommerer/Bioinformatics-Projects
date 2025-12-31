import pycxsimulator
import matplotlib
import matplotlib.pyplot as plt
import random as rd

n = 1000
sd = 0.1
dim = 10

matplotlib.use("TkAgg")

def num_particles(val = n):
    """
    Number of particles.
    """
    global n
    n = int(val)
    return val

def sd_particles(val = sd):
    """
    Standard deviation of the random Gaussian movement each particle takes every step.
    """
    global sd
    sd = float(val)
    return sd


def dim_plot(val = dim):
    """
    Change the dimensions of the plot.
    """
    global dim
    dim = float(val)
    return dim


def initialize():
    """
    This is my first PyCX simulator code.
    It simulates random motion of n particles.
    """
    global xlist, ylist
    xlist = []
    ylist = []
    for i in range(n):
        xlist.append(rd.gauss(0,1))
        ylist.append(rd.gauss(0,1))

def observe():
    global xlist, ylist
    plt.cla()
    plt.plot(xlist,ylist,'.')
    plt.xlim(-dim,dim)
    plt.ylim(-dim,dim)

def update():
    global xlist, ylist
    for i in range(n):
        xlist[i] += rd.gauss(0,sd)
        ylist[i] += rd.gauss(0,sd)



pycxsimulator.GUI(parameterSetters = [num_particles,sd_particles, dim_plot]).start(func=[initialize,observe,update])