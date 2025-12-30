import pycxsimulator
from ca_funs import *


def main():
    matplotlib.use("TkAgg")

    ca = (
        (lambda config,x,y: count_vNeumann(config,x,y)%2, """Parity Model using von Neumann neighborhood and mod 2"""),
        (lambda config,x,y: 1 if count_Moore(config,x,y)>=4 else 0, """Droplet Model using Moore neighborhood"""),
        (lambda config,x,y: 1 if count_Moore(config,x,y)==3 or (count_Moore(config,x,y)==4 and config[x,y]==1) else 0, """Game of Life""") #count=3 -> 3 active neighbors if quiescent, 2 active neighbors if active; count=4 -> 3 active neighbors if active
    )

    inits = (
        ([size_matrix],([(0,0),(0,1),(1,0),(-1,0),(0,-1)],1)), # Plus
        ([size_matrix],([(-1,0),(0,0),(1,0)],1)), # Line
        ([size_matrix,prob],(lambda n,p0:np.random.random((n,n))<=p0,0)), # Random entries in matrix
        ([size_matrix],([(0,-2),(0,-1),(0,0),(1,0),(2,-1)],1)) # Game of Life glider
    )

    c = 2 # Changes the model used
    i = 3 # Changes the initial conditions used

    initialize.__doc__ = ca[c][1]

    pycxsimulator.GUI(parameterSetters = inits[i][0]).start(func=[initialize,observe,update],initparams=inits[i][1],stepparams=ca[c][0])


if __name__ == "__main__":
    main()