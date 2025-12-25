import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
from discrete_models import *

def plot_np(res,timesteps,v):
    plot_timesteps(res,timesteps,v)
    if (len(v.inits_names)>1):
        plot_against(res,timesteps,v)   
    else:
        pass
        #plot_cobweb(res,timesteps,v)  
    plt.show() 

"""
For each combination of parameters and initial values, a plot of all variables over time is created.
"""
def plot_timesteps(res,timesteps,v):
    minval = np.min(res)
    maxval = np.max(res)
    fig, axs = plt.subplots(len(v.inits_vec),len(v.params_vec),squeeze=False)
    for i_param in range(len(v.params_vec)):
        for j_init in range(len(v.inits_vec)):
            for m_var in range(len(v.inits_names)):
                if i_param == len(v.params_vec)-1:
                    axs[j_init,i_param].plot(timesteps,res[i_param,j_init,:,m_var],label=f"{v.inits_names[m_var]}={v.inits_vec[j_init][m_var]}")
                    axs[j_init,i_param].legend(loc='center left', bbox_to_anchor=(1, 0.5))
                else:
                    axs[j_init,i_param].plot(timesteps,res[i_param,j_init,:,m_var])
                axs[j_init,i_param].set_ylim([minval,maxval])
            axs[0,i_param].set_title(",".join([f"{v.params_names[l]}={v.params_vec[i_param][l]}" for l in range(len(v.params_names))]))   

"""
For each set of parameters and each pair of variables, a phase diagram for each set of initial values is created.
"""
def plot_against(res,timesteps,v):
    minval = np.min(res)
    maxval = np.max(res)
    fig, axs = plt.subplots(math.comb(len(v.inits_names),2),len(v.params_vec),squeeze=False)
    for i_param in range(len(v.params_vec)):
        for j_init in range(len(v.inits_vec)):
            combos = 0
            for m_var in range(len(v.inits_names)):
                for n_var in range(m_var+1,len(v.inits_names)):
                    if i_param == len(v.params_vec)-1:
                        axs[combos,i_param].plot(res[i_param,j_init,:,m_var],res[i_param,j_init,:,n_var],label=f"{v.inits_names[m_var]}={v.inits_vec[j_init][m_var]}\n{v.inits_names[n_var]}={v.inits_vec[j_init][n_var]}")
                        axs[combos,i_param].legend(loc='center left', bbox_to_anchor=(1, 0.5))
                    else:
                        axs[combos,i_param].plot(res[i_param,j_init,:,m_var],res[i_param,j_init,:,n_var])
                    axs[combos,i_param].set_xlabel(v.inits_names[m_var])
                    axs[combos,i_param].set_ylabel(v.inits_names[n_var])
                    axs[combos,i_param].set_xlim([minval,maxval])
                    axs[combos,i_param].set_ylim([minval,maxval])
                    combos += 1
            axs[0,i_param].set_title(",".join([f"{v.params_names[l]}={v.params_vec[i_param][l]}" for l in range(len(v.params_names))])) 

"""
If only 1 variable exists, a cobweb plot is created for each pair of parameters and initial values.
"""
def plot_cobweb(res,timesteps,v):
    minval = np.min(res)
    maxval = np.max(res)
    fig, axs = plt.subplots(len(v.inits_vec),len(v.params_vec),squeeze=False)
    for i_param in range(len(v.params_vec)):
        for j_init in range(len(v.inits_vec)):
            for m_var in range(len(v.inits_names)):
                axs[j_init,i_param].plot
                if i_param == len(v.params_vec)-1:
                    axs[j_init,i_param].plot(timesteps,res[i_param,j_init,:,m_var],label=f"{v.inits_names[m_var]}={v.inits_vec[j_init][m_var]}")
                    axs[j_init,i_param].legend(loc='center left', bbox_to_anchor=(1, 0.5))
                else:
                    axs[j_init,i_param].plot(timesteps,res[i_param,j_init,:,m_var])
                axs[j_init,i_param].set_ylim([minval,maxval])
            axs[0,i_param].set_title(",".join([f"{v.params_names[l]}={v.params_vec[i_param][l]}" for l in range(len(v.params_names))]))   

        
def main():
    """
    models[i][0] is the name of the model, as has to be given as input to Set_Model
    models[i][1] is the number of timesteps n
    models[i][2] is the step size h; therefore, n*h is the total time passed
    """
    models = [("PDE_2",30,1),("Logistic",400,1),("LV_Euler",5000,0.01),("LV_PPM",5000,0.01),("LV_PPM_3",5000,0.01),("van_del_Pol",10000,0.01)]
    chosen_model = 5

    n = models[chosen_model][1]
    h = models[chosen_model][2]
    timesteps = np.linspace(0,n*h,n)

    v = Set_Model(models[chosen_model][0],h)
    #For every pair (i,j) of parameters and initial values the model is iterated over, res_matrix contains the output for all variables throughout all timesteps
    res_matrix = np.empty([len(v.params_vec),len(v.inits_vec),len(timesteps),len(v.inits_names)])
    for i in range(len(v.params_vec)):
        for j in range(len(v.inits_vec)):
            mymodel = Calc_Model(v.functions,v.params_vec[i],v.inits_vec[j])
            for t in range(len(timesteps[1:])):
                mymodel.update()
                mymodel.observe()
            res_matrix[i,j,:,:] = mymodel.result
    plot_np(res_matrix,timesteps,v)

if __name__ == "__main__":
    main()