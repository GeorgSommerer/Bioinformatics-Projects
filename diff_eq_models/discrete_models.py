import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from itertools import product


"""
    Chooses the type of model as well as the parameters and initial values on which it is to be run
    :param str model: A string containing the model name, which can be obtained from the models array in the main method
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
    def __init__(self,model,h=0.01):
        if model == "PDE_2":
            self.params_vec = [(np.array([[0.5,1],[-0.5,1]]),np.array([0,0]))]
            self.inits_vec = list(product(np.arange(-2.0,2.0,1.),np.arange(-2.0,2.0,1.)))
            self.params_names = ["A","b"]
            self.inits_names = ["x0","y0"]
            self.functions = [lambda A,b,x,y: np.matmul(A,np.array([x,y]))+b]
        if model == "Logistic":
            self.params_vec = [(0.5,500)]
            self.inits_vec = [(1,),(10,),(50,),(100,),(200,),(500,)] 
            self.params_names = ["r","K"]
            self.inits_names = ["x0"]
            self.functions = [lambda r,K,x: x+r*x*(1-x/K)]
        if model == "LV_Euler":
            self.params_vec = [(1,1,1,1,h)]
            self.inits_vec = [(0.1,0.1)] 
            self.params_names = ["a","b","c","d","h"]
            self.inits_names = ["x0","y0"]
            self.functions = [lambda a,b,c,d,h,x,y: x+h*(a*x-b*x*y), lambda a,b,c,d,h,x,y: y+h*(c*x*y-d*y)]
        if model == "LV_PPM":
            self.params_vec = [(1,1,1,2,h)]
            self.inits_vec = [(0.3,0.2)] 
            self.params_names = ["a","b","c","d","h"]
            self.inits_names = ["x0","y0"]
            self.functions = [lambda a,b,c,d,h,x,y: x*(1+a*h)/(1+b*h*y),lambda a,b,c,d,h,x,y: y*(1+c*h*(x*(1+a*h)/(1+b*h*y)))/(1+d*h)]
        if model == "LV_PPM_3":
            self.params_vec = [(1,1,1,1,1,h),(1,1,1,1,0.05,h),(0.1,0.1,0.1,0.1,0.05,h)]
            self.inits_vec = [(10,0.3,0.2)] 
            self.params_names = ["a","b","c","d","e","h"]
            self.inits_names = ["z0","x0","y0"]
            self.functions = [lambda a,b,c,d,e,h,z,x,y: z/(1+e*h*x),lambda a,b,c,d,e,h,z,x,y: x*(1+a*h*(z/(1+e*h*x)))/(1+b*h*y),lambda a,b,c,d,e,h,z,x,y: y*(1+c*h*(x*(1+a*h*z/(1+e*h*x))/(1+b*h*y)))/(1+d*h)]
        if model == "van_del_Pol":
            self.params_vec = [(-1,h),(-0.1,h),(0,h),(.1,h),(1,h)]
            self.inits_vec = [(0.1,0.1),(0.5,0.5),(1,1)] 
            self.params_names = ["r","h"]
            self.inits_names = ["x0","y0"]
            self.functions = [lambda r,h,x,y: x+y*h, lambda r,h,x,y: y+h*(-r*(x**2-1)*y-x)]
        if model == "Bifurcation":
            self.params_vec = [(0.1,),(0.5,),(1.0,),(1.1,),(1.5,),(1.6,)]
            self.inits_vec = [(0.1,)]
            self.params_names = ["r"]
            self.inits_names = ["x0"]
            self.functions = [lambda r,x: x+r-x**2]

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