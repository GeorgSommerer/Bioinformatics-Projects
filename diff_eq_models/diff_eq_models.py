import numpy as np
from itertools import product


"""
    Chooses the type of model as well as the parameters and initial values on which it is to be run
    :param str model: A string containing the model name, which can be obtained from the models array in the main method
    :param int which: Given multiple sets of parameters/initial values (for different tasks, e.g. cobweb plot vs. bifurcation plot), choose which one to use
    :param float h: The step size which is used in the model.
    :param array(tuple) params_vec: Every tuple contains a set of parameters to try (tuple size has to match the length of self.params_names)
    :param array(tuple) inits_vec: Every tuple contains a set of initial values to try (tuple size has to match the length of self.inits_names)
    :param array(str) params_names: Names of the parameters
    :param array(str) inits_names: Names of the variables/initial values
    :param array(lambda) functions: Contains all the discretized equations defining the model
        The order of functions has to match the order of variables in self.inits_names
        The inputs of each function have to be the same and their order has to match the order in self.params_names then self.inits_names
"""
class Set_Model:
    def __init__(self,model,which=0,h=0.01):
        #PDE with 2 variables
        self.which = which
        if model == "PDE_2":
            self.params_vec = [(np.array([[0.5,1],[-0.5,1]]),np.array([0,0]))]
            self.inits_vec = list(product(np.arange(-2.0,2.0,1.),np.arange(-2.0,2.0,1.)))
            self.params_names = ["A","b"]
            self.inits_names = ["x","y"]
            self.functions = [lambda A,b,x,y: np.matmul(A,np.array([x,y]))+b]
        #Logistic model
        if model == "Logistic":
            self.params_vec = [(0.5,500)]
            self.inits_vec = [(1,),(10,),(50,),(100,),(200,),(500,)] 
            self.params_names = ["r","K"]
            self.inits_names = ["x"]
            self.functions = [lambda r,K,x: x+r*x*(1-x/K)]
        #Euler-discretized Lotka-Volterra model
        if model == "LV_Euler":
            self.params_vec = [(1,1,1,1,h)]
            self.inits_vec = [(0.1,0.1)] 
            self.params_names = ["a","b","c","d","h"]
            self.inits_names = ["x","y"]
            self.functions = [lambda a,b,c,d,h,x,y: x+h*(a*x-b*x*y), lambda a,b,c,d,h,x,y: y+h*(c*x*y-d*y)]
        #Lotka-Volterra model discretized with a positivity preserving map (PPM)
        if model == "LV_PPM":
            self.params_vec = [(1,1,1,2,h)]
            self.inits_vec = [[(0.3,0.2)],list(product(np.arange(0.3,0.30003,0.00001),np.arange(0.2,0.20003,0.00001)))][self.which] #0: standard analysis, 1: test for chaotic behavior
            self.params_names = ["a","b","c","d","h"]
            self.inits_names = ["x","y"]
            self.functions = [lambda a,b,c,d,h,x,y: x*(1+a*h)/(1+b*h*y),lambda a,b,c,d,h,x,y: y*(1+c*h*(x*(1+a*h)/(1+b*h*y)))/(1+d*h)]
        #PPM-discretized Lotka-Volterra model with additional ressource Z that is consumed by X but does not grow 
        if model == "LV_PPM_3":
            self.params_vec = [(1,1,1,1,1,h),(1,1,1,1,0.05,h),(0.1,0.1,0.1,0.1,0.05,h)]
            self.inits_vec = [(10,0.3,0.2)] 
            self.params_names = ["a","b","c","d","e","h"]
            self.inits_names = ["z","x","y"]
            self.functions = [lambda a,b,c,d,e,h,z,x,y: z/(1+e*h*x),lambda a,b,c,d,e,h,z,x,y: x*(1+a*h*(z/(1+e*h*x)))/(1+b*h*y),lambda a,b,c,d,e,h,z,x,y: y*(1+c*h*(x*(1+a*h*z/(1+e*h*x))/(1+b*h*y)))/(1+d*h)]
        #Van-del-Pol oscillator
        if model == "van_del_Pol":
            self.params_vec = [(-1,h),(-0.1,h),(0,h),(.1,h),(1,h)]
            self.inits_vec = [(0.1,0.1),(0.5,0.5),(1,1)] 
            self.params_names = ["r","h"]
            self.inits_names = ["x","y"]
            self.functions = [lambda r,h,x,y: x+y*h, lambda r,h,x,y: y+h*(-r*(x**2-1)*y-x)]
        #A simple model that shows period-doubling bifurcations
        if model == "Bifurcation":
            self.params_vec = [[(r,) for r in np.arange(0.,2.,0.01)],[(0.1,),(0.5,),(1.0,),(1.1,),(1.5,),(1.6,)]][self.which] #0: bifurcation, 1: Cobweb
            self.inits_vec = [(0.1,)]
            self.params_names = ["r"]
            self.inits_names = ["x"]
            self.functions = [lambda r,x: x+r-x**2]
        #A simplified version of the Logistic function used for bifurcation analysis
        if model == "Logistic_Map":
            self.params_vec = [[(r,) for r in np.arange(0,4,0.05)],[(r,) for r in range(5)]][self.which] #0: bifurcation, 1: Cobweb
            self.inits_vec = [(0.1,),(0.3,),(0.51,)]
            self.params_names = ["r"]
            self.inits_names = ["x"]
            self.functions = [lambda r,x: r*x*(1-x)]
        #Lorenz equations
        if model == "Lorenz":
            self.params_vec = [[(s*1.,30.,3.,h) for s in np.arange(4,24,4)],[(10.,r*1.,3.,h) for r in np.arange(10,60,10)],[(10.,30.,b*1.,h) for b in np.arange(1,6,1)]][self.which] #0: vary s, 1: vary r, 2: vary b
            self.inits_vec = [(1.,1.,1.)]
            self.params_names = ["s","r","b","h"]
            self.inits_names = ["x","y","z"]
            self.functions = [lambda s,r,b,h,x,y,z: x+h*(s*(y-x)),lambda s,r,b,h,x,y,z: y+h*(r*x-y-x*z),lambda s,r,b,h,x,y,z:z+h*(x*y-b*z)]


"""
    For any set of parameters and initial values, calculates the outcome of the discretized equations of the model at the next step
    :param np.ndarray(float) result: Size (timesteps, len(inits_names)); contains the calculated values for all variables at each step
"""
class Calc_Model:
    def __init__(self,functions,params,inits):
        self.functions = functions
        self.params = params
        self.vars = np.array(inits)
        self.result = np.array(self.vars)
    def observe(self):
        self.result = np.vstack((self.result,self.vars))
    def update(self):
        temp = []
        for f in self.functions:
            temp.append(f(*self.params,*self.vars))
        if type(temp[0]) == np.ndarray: #If the model is a PDE, only 1 function exists and the resulting variables are already returned in an np.ndarray
            self.vars = temp[0]
        else:
            self.vars = np.array(temp)