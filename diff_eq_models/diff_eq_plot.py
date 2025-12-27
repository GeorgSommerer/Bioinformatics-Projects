import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

"""
Main plotting function; calls the individual plots depending of the bitmap that is input.
"""
def plot_main(res,timesteps,v,plot_which):
    minval = np.min([0,np.min(res)])-0.1*np.abs(np.min([0,np.min(res)]))
    maxval = np.max([1,np.max(res)])+0.1*np.abs(np.max([1,np.max(res)]))  

    if (plot_which & 1 << 0):
        plot_timesteps(res,timesteps,v,minval,maxval)
    if (plot_which & 1 << 1):
        plot_trajectory_2D(res,timesteps,v,minval,maxval)   
    if (plot_which & 1 << 2):
        plot_trajectory_3D(res,timesteps,v,minval,maxval)   
    if (plot_which & 1 << 3):
        plot_cobweb(res,timesteps,v,minval,maxval)  
    if (plot_which & 1 << 4):
        plot_asymptotic(res,timesteps,v,minval,maxval)  
        
    plt.show() 

"""
For each combination of parameters and initial values, a plot of all variables over time is created.
"""
def plot_timesteps(res,timesteps,v,minval,maxval):
    fig, axs = plt.subplots(len(v.inits_vec),len(v.params_vec),squeeze=False)
    for i_param in range(len(v.params_vec)):
        for j_init in range(len(v.inits_vec)):
            for m_var in range(len(v.inits_names)):
                axs[j_init,i_param].plot(timesteps,res[i_param,j_init,:,m_var],label=f"{v.inits_names[m_var]}0={v.inits_vec[j_init][m_var]}")
                    
                axs[j_init,len(v.params_vec)-1].legend(loc='center left', bbox_to_anchor=(1, 0.5))
                axs[j_init,i_param].set_ylim([minval,maxval])
        axs[0,i_param].set_title(",".join([f"{v.params_names[l]}={v.params_vec[i_param][l]}" for l in range(len(v.params_names))]))   

"""
For each set of parameters and each pair of variables, a phase diagram of the trajectories for all initial values is created.
Maybe add phase space: mvals, nvals = meshgrid(np.linspace) -> mdot, ndot = f(mvals, nvals), g(mvals, nvals) -> streamplot(mvals, nvals, mdot, ndot)
"""
def plot_trajectory_2D(res,timesteps,v,minval,maxval):
    fig, axs = plt.subplots(math.comb(len(v.inits_names),2),len(v.params_vec),squeeze=False)
    for i_param in range(len(v.params_vec)):
        for j_init in range(len(v.inits_vec)):
            combos = 0
            for m_var in range(len(v.inits_names)):
                for n_var in range(m_var+1,len(v.inits_names)):
                    axs[combos,i_param].plot(res[i_param,j_init,:,m_var],res[i_param,j_init,:,n_var],label=f"{v.inits_names[m_var]}0={v.inits_vec[j_init][m_var]}\n{v.inits_names[n_var]}0={v.inits_vec[j_init][n_var]}")
        
                    axs[combos,len(v.params_vec)-1].legend(loc='center left', bbox_to_anchor=(1, 0.5))                
                    axs[combos,i_param].set_xlabel(v.inits_names[m_var])
                    axs[combos,i_param].set_ylabel(v.inits_names[n_var])
                    axs[combos,i_param].set_xlim([minval,maxval])
                    axs[combos,i_param].set_ylim([minval,maxval])
                    combos += 1

        axs[0,i_param].set_title(",".join([f"{v.params_names[l]}={v.params_vec[i_param][l]}" for l in range(len(v.params_names))])) 

"""
If 3 variables exist, plot the trajectory in 3D space once for every initial value, and once for all at the same time.
"""
def plot_trajectory_3D(res,timesteps,v,minval,maxval):
    fig, axs = plt.subplots(len(v.inits_vec)+1,len(v.params_vec),squeeze=False,subplot_kw=dict(projection='3d'))
    for i_param in range(len(v.params_vec)):
        for j_init in range(len(v.inits_vec)):
            axs[j_init,i_param].plot(res[i_param,j_init,:,0],res[i_param,j_init,:,1],res[i_param,j_init,:,2],label=f"{v.inits_names[0]}0={v.inits_vec[j_init][0]}\n{v.inits_names[1]}0={v.inits_vec[j_init][1]}\n{v.inits_names[2]}0={v.inits_vec[j_init][2]}")
            axs[j_init,len(v.params_vec)-1].legend(loc='center left', bbox_to_anchor=(1, 0.5))  
            axs[len(v.inits_vec),i_param].plot(res[i_param,j_init,:,0],res[i_param,j_init,:,1],res[i_param,j_init,:,2]) 

        for j_init in range(len(v.inits_vec)+1):
            axs[j_init,i_param].set_xlabel(v.inits_names[0])
            axs[j_init,i_param].set_ylabel(v.inits_names[1])
            axs[j_init,i_param].set_zlabel(v.inits_names[2])
            axs[j_init,i_param].set_xlim([np.min(res[:,:,:,0]),np.max(res[:,:,:,0])])
            axs[j_init,i_param].set_ylim([np.min(res[:,:,:,1]),np.max(res[:,:,:,1])])
            axs[j_init,i_param].set_zlim([np.min(res[:,:,:,2]),np.max(res[:,:,:,2])])
        axs[0,i_param].set_title(",".join([f"{v.params_names[l]}={v.params_vec[i_param][l]}" for l in range(len(v.params_names))])) 

"""
If only 1 variable exists, a cobweb plot is created for each pair of parameters and initial values.
"""
def plot_cobweb(res,timesteps,v,minval,maxval):
    fig, axs = plt.subplots(len(v.inits_vec),len(v.params_vec),squeeze=False)
    for i_param in range(len(v.params_vec)):
        for j_init in range(len(v.inits_vec)):
            axs[j_init,i_param].plot([minval,maxval],[minval,maxval],'k')
            rng = np.linspace(minval,maxval,100)
            axs[j_init,i_param].plot(rng,[v.functions[0](*v.params_vec[i_param],var) for var in rng],'k')

            horizontal = [res[i_param,j_init,0,0]]
            vertical = [res[i_param,j_init,0,0]]
            for t in range(1,len(timesteps)):
                horizontal.append(vertical[-1])
                vertical.append(res[i_param,j_init,t,0])
                horizontal.append(res[i_param,j_init,t,0])
                vertical.append(res[i_param,j_init,t,0])
            axs[j_init,i_param].plot(horizontal,vertical,label=f"{v.inits_names[0]}0={v.inits_vec[j_init][0]}")

            axs[j_init,len(v.params_vec)-1].legend(loc='center left', bbox_to_anchor=(1, 0.5))
            axs[j_init,i_param].set_xlabel(f"{v.inits_names[0]}(n)")
            axs[j_init,0].set_ylabel(f"{v.inits_names[0]}(n+1)")
            axs[j_init,i_param].set_xlim([np.min,maxval])
            axs[j_init,i_param].set_ylim([minval,maxval])
        axs[0,i_param].set_title(",".join([f"{v.params_names[l]}={v.params_vec[i_param][l]}" for l in range(len(v.params_names))])) 

"""
Plots the asymptotic behavior of the model for every parameter across all variations of that parameter for all initial values
"""
def plot_asymptotic(res,timesteps,v,minval,maxval):
    fig, axs = plt.subplots(len(v.inits_vec),len(v.params_names),squeeze=False)
    for i_parname in range(len(v.params_names)):
        for j_init in range(len(v.inits_vec)):
            for k_param in range(len(v.params_vec)):
                for t in range(int(len(timesteps)/2),len(timesteps)):
                    axs[j_init,i_parname].plot(v.params_vec[k_param][i_parname],res[k_param,j_init,t,0],'b.',alpha=0.3)

            axs[j_init,i_parname].set_xlabel(v.params_names[i_parname])
            axs[j_init,0].set_ylabel(f"{v.inits_names[0]}(eq)")
            axs[j_init,i_parname].set_ylim([minval,maxval])