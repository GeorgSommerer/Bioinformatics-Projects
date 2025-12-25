import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
from discrete_models import *
from itertools import product


class Vars:
    def __init__(self,model,h=0.01):
        if model == "PDE_2":
            self.params_vec = [(np.array([[0.5,1],[-0.5,1]]),np.array([0,0]))]
            self.inits_vec = list(product(np.arange(-2.0,2.0,1.),np.arange(-2.0,2.0,1.)))#[(1,1)]
            self.params_names = ["A","b"]
            self.inits_names = ["x0","y0"]
        if model == "Logistic":
            self.params_vec = [(0.5,500)]
            self.inits_vec = [(10,)] 
            self.params_names = ["r","K"]
            self.inits_names = ["x0"]
        if model == "LV_Euler":
            self.params_vec = [(1,1,1,1,h)]
            self.inits_vec = [(0.1,0.1)] 
            self.params_names = ["a","b","c","d","h"]
            self.inits_names = ["x0","y0"]
        if model == "LV_PPM":
            self.params_vec = [(1,1,1,2,h)]
            self.inits_vec = [(0.3,0.2)] 
            self.params_names = ["a","b","c","d","h"]
            self.inits_names = ["x0","y0"]
        if model == "LV_PPM_3":
            self.params_vec = [(1,1,1,1,1,0.05,h)]
            self.inits_vec = [(0.3,0.2,10)] 
            self.params_names = ["a","b","c","d","e","p","h"]
            self.inits_names = ["x0","y0","z0"]

def select_ode(model,params,inits):
    if model == "PDE_2":
        return PDE_2(*params,*inits)
    if model == "Logistic":
        return Logistic(*params,*inits)
    if model == "LV_Euler":
        return LV_Euler(*params,*inits)
    if model == "LV_PPM":
        return LV_PPM(*params,*inits)
    if model == "LV_PPM_3":
        return LV_PPM_3(*params,*inits)

def plot_np(res,timesteps,v):
    minval = np.min(res)
    maxval = np.max(res)
    fig1, axs1 = plt.subplots(len(v.inits_vec),len(v.params_vec),squeeze=False) # For all combinations of parameters and initial values used (one for each column, counted via i_total), plot in the 0th row all variables against the timesteps, and in all the other rows all 2-combinations of variables against each other (m_var vs. n_var)
    fig2, axs2 = plt.subplots(math.comb(len(v.inits_names),2),len(v.params_vec),squeeze=False)
    for i_param in range(len(v.params_vec)):
        for j_init in range(len(v.inits_vec)):
            for m_var in range(len(v.inits_names)):
                axs1[j_init,i_param].plot(timesteps,res[i_param,j_init,:,m_var],label=f"{v.inits_names[m_var]}={v.inits_vec[j_init][m_var]}")
                axs1[j_init,i_param].legend()
                axs1[j_init,i_param].set_ylim([minval,maxval])
            axs1[0,i_param].set_title(",".join([f"{v.params_names[l]}={v.params_vec[i_param][l]}" for l in range(len(v.params_names))]))        
    for i_param in range(len(v.params_vec)):
        for j_init in range(len(v.inits_vec)):
            for m_var in range(len(v.inits_names)):
                for n_var in range(m_var+1,len(v.inits_names)):
                    j_total = len(v.inits_names)*m_var+n_var
                    axs2[-1+j_total,i_param].plot(res[i_param,j_init,:,m_var],res[i_param,j_init,:,n_var])
                    axs2[-1+j_total,i_param].set_xlabel(v.inits_names[m_var])
                    axs2[-1+j_total,i_param].set_ylabel(v.inits_names[n_var])
                    axs2[-1+j_total,i_param].set_xlim([minval,maxval])
                    axs2[-1+j_total,i_param].set_ylim([minval,maxval])
            axs2[0,i_param].set_title(",".join([f"{v.params_names[l]}={v.params_vec[i_param][l]}" for l in range(len(v.params_names))]))        
    plt.show() 
        
def main():
    print(len(list(product(np.arange(-2.0,2.0,.5),np.arange(-2.0,2.0,.5)))))
    n = 5000
    h = 0.01
    model = "LV_PPM" # "PDE_2": n=30, h=1; LV_PPM: n=5000, h=0.01
    v = Vars(model,h)

    timesteps = np.linspace(0,n*h,n)

    res_matrix = np.empty([len(v.params_vec),len(v.inits_vec),len(timesteps),len(v.inits_names)])
    for i in range(len(v.params_vec)):
        for j in range(len(v.inits_vec)):
            myode = select_ode(model,v.params_vec[i],v.inits_vec[j])
            for t in range(len(timesteps[1:])):
                myode.update()
                myode.observe()
            res_matrix[i,j,:,:] = myode.result
    plot_np(res_matrix,timesteps,v)

if __name__ == "__main__":
    main()