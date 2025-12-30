import numpy as np
import matplotlib
import matplotlib.pyplot as plt

n = 100
p0 = 0.2

"""
Initializes certain cells in the automaton.
:param pattern: Can be either an array of tuples containing the (x,y) positions of each cell relative to the origin (which is at (int(n/2),int(n/2)) that are initialized with 1,
    or a function according to which each cell is to be initialized.
:param bool hard_coded: If hard_coded is True, then the initial pattern is constructed according to hard-coded coordinates; otherwise, a function is used.
"""
def initialize(pattern,hard_coded=1):
    global config, nextconfig
    config = np.zeros((n,n))
    nextconfig = np.zeros((n,n))
    if hard_coded:
        for state in pattern:
            config[int(n/2)-state[0],int(n/2)+state[1]] = 1
    else:
        config = pattern(n,p0)

def observe():
    global config
    plt.cla()
    plt.imshow(config,vmin=0,vmax=1,cmap="binary")

"""
Executes the state-transition function of the specific automaton for every cell
:return bool not_finished: if the automaton has entered its final state (meaning that the configuration doesn't change), this bool becomes false and the PyCX simulator stops.
"""
def update(state_transition_func):
    global config, nextconfig
    nextconfig = np.zeros((n,n))
    for x in range(config.shape[0]):
        for y in range(config.shape[1]):
            nextconfig[x,y] = state_transition_func(config,x,y)
    not_finished = False if (config==nextconfig).all() else True
    config = nextconfig
    return not_finished

"""
Sum up the states of all cells in a von Neumann neighborhood of radius 1
"""
def count_vNeumann(config,x,y):
    tempval = 0
    for dx in [-1,0,1]:
        tempval += config[(x+dx)%n,(y)%n]
    for dy in [-1,1]:
        tempval += config[(x)%n,(y+dy)%n]
    return tempval

"""
Sum up the states of all cells in a Moore neighborhood of radius 1
"""
def count_Moore(config,x,y):
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

def prob(val = p0):
    """
    Probability of any cell starting with 1.
    """
    global p0
    p0 = float(val)
    return val

