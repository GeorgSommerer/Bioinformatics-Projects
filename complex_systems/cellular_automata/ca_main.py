import pycxsimulator
from ca_funs import *


def main():
    matplotlib.use("TkAgg")

    """
    ca contains a list of variable parameters, the state-transition function, and a doc string pertaining to the model
    """
    ca = (
        ([],[lambda config,x,y,k: count_vNeumann(config,x,y)%2], """Parity Model using von Neumann neighborhood and mod 2"""),
        ([],[lambda config,x,y,k: 1 if count_Moore(config,x,y)>=4 else 0], """Droplet Model using Moore neighborhood"""),
        ([radius],[lambda config,x,y,k: count_Radius(config,x,y)>=np.floor(k/2)], """Droplet Model using a custom radius"""),
        ([],[lambda config,x,y,k: 1 if count_Moore(config,x,y)==3 or (count_Moore(config,x,y)==4 and config[x,y]==1) else 0], """Game of Life"""), #count=3 -> 3 active neighbors if quiescent, 2 active neighbors if active; count=4 -> 3 active neighbors if active
        ([],[lambda config,x,y,k: np.round(count_vNeumann(config,x,y)/5)], """Majority Rule using Moore neighborhood"""),
        ([radius],[lambda config,x,y,k: np.round(count_Radius(config,x,y)/k)], """Majority Model using a custom radius""")
    )

    """
    inits contains a list of variable parameters, a list of hard-coded coordinates to be turned =1 or a function that determines the initial values,
    and a bool specifying whether the initial values are hard-coded or not
    """
    inits = (
        ([size_matrix],([(0,0),(0,1),(1,0),(-1,0),(0,-1)],1)), # Plus
        ([size_matrix],([(-1,0),(0,0),(1,0)],1)), # Line
        ([size_matrix,prob],(lambda n,p0:(np.random.random((n,n))<=p0).astype(int),0)), # Random entries in matrix
        ([size_matrix],([(0,-2),(0,-1),(0,0),(1,0),(2,-1)],1)) # Game of Life glider
    )

    c = 5 # Changes the model used
    i = 2 # Changes the initial conditions used

    initialize.__doc__ = ca[c][2]

    pycxsimulator.GUI(parameterSetters = ca[c][0]+inits[i][0]).start(func=[initialize,observe,update],initparams=inits[i][1],stepparams=ca[c][1])


if __name__ == "__main__":
    main()