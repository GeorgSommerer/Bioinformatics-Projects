import numpy as np
import matplotlib
import matplotlib.pyplot as plt

n = 100
p0 = 0.2
r = 1
k = 4*int(r)+1 #Number of cells within an r-neighborhood
for x in range(1,int(r)+1):
    for y in range(1,int(r)+1):
        if np.sqrt(x**2+y**2)<=r:
            k+=4

"""
Initializes certain cells in the automaton.
:param pattern: Can be either an array of tuples containing the (x,y) positions of each cell relative to the origin (which is at (int(n/2),int(n/2)) that are initialized with 1,
    or a function according to which each cell is to be initialized.
:param bool hard_coded: If hard_coded is True, then the initial pattern is constructed according to hard-coded coordinates; otherwise, a function is used.
"""
def initialize(pattern,hard_coded=1):
    np.random.seed(0)
    global config, nextconfig
    config = np.zeros((n,n),dtype=int)
    nextconfig = np.zeros((n,n),dtype=int)
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
    nextconfig = np.zeros((n,n),dtype=int)
    for x in range(config.shape[0]):
        for y in range(config.shape[1]):
            nextconfig[x,y] = state_transition_func(config,x,y,k)
    not_finished = False if (config==nextconfig).all() else True
    config = nextconfig
    return not_finished

"""
Sum up the states of all cells in a von Neumann neighborhood of variable radius
"""
def count_vNeumann(config,x,y,r=r,n=n):
    count = 0
    for dx in range(-int(r),int(r)+1):
        count += config[(x+dx)%n,y]
        for dy in range(1,int(r)+1-np.abs(dx)):
            count += config[(x+dx)%n,(y+dy)%n]+config[(x+dx)%n,(y-dy)%n]
    return count

"""
Sum up the states of all cells in a Moore neighborhood of variable radius
"""
def count_Moore(config,x,y,r=r,n=n):
    count = 0
    for dx in range(-int(r),int(r)+1):
        for dy in range(-int(r),int(r)+1):
            count += config[(x+dx)%n,(y+dy)%n]
    return count

"""
Sum up the states of all cells within a certain radius of x
r=1 results in the von Neumann neighborhood, and r=sqrt(2) is equal to the Moore neighborhood
"""
def count_Radius(config,x,y,r=r,n=n):
    count = 0
    for dx in range(0,int(r)+1): #All cells along the x axis with |dx|<=int(r) lie within the neighborhood
        count += config[(x+dx)%n,y]
        if dx > 0:
            count += config[(x-dx)%n,y]
        dy = 1
        while (np.sqrt(dx**2+dy**2)<=r):
            count += config[(x+dx)%n,(y+dy)%n]+config[(x+dx)%n,(y-dy)%n]
            if dx > 0:
                count += config[(x-dx)%n,(y+dy)%n]+config[(x-dx)%n,(y-dy)%n]
            dy += 1
    return count


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

def radius(val = r):
    """
    Radius of the neighborhood.
    """
    global r, k
    r = float(val)
    k = 4*int(r)+1
    for x in range(1,int(r)+1):
        for y in range(1,int(r)+1):
            if np.sqrt(x**2+y**2)<=r:
                k+=4
    return val