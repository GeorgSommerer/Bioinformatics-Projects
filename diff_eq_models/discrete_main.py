import math
from discrete_models import *

def plot_main(res,timesteps,v,plot_which):
    minval = np.min([0,np.min(res)])-0.1*np.abs(np.min([0,np.min(res)]))
    maxval = np.max([1,np.max(res)])+0.1*np.abs(np.max([1,np.max(res)]))  

    if (plot_which & 1 << 0):
        plot_timesteps(res,timesteps,v,minval,maxval)
    if (plot_which & 1 << 1):
        plot_phase(res,timesteps,v,minval,maxval)   
    if (plot_which & 1 << 2):
        plot_cobweb(res,timesteps,v,minval,maxval)  
    if (plot_which & 1 << 3):
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
For each set of parameters and each pair of variables, a phase diagram for all initial values is created.
Maybe add phase space: mvals, nvals = meshgrid(np.linspace) -> mdot, ndot = f(mvals, nvals), g(mvals, nvals) -> streamplot(mvals, nvals, mdot, ndot)
"""
def plot_phase(res,timesteps,v,minval,maxval):
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
            axs[j_init,i_param].set_xlim([minval,maxval])
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
                
        
def main():
    """
    models[i][0] is the name of the model, as has to be given as input to Set_Model
    models[i][1] is the number of timesteps n
    models[i][2] is the step size h; therefore, n*h is the total time passed
    models[i][3] is the plotting behavior: Position 0 stands for plot_timesteps, 1 for plot_phase, 2 for plot_cobweb, and 3 for plot_asymptotic
    """
    models = [
        ("Logistic",[400],[1],[0b1101]),
        ("Bifurcation",[200,30],[1,1],[0b1000,0b0101]), #0: bifurcation, 1: cobweb
        ("Logistic_Map",[100,30],[1,1],[0b1000,0b0101]), #0: bifurcation, 1: cobweb
        ("PDE_2",[30],[1],[0b0011]),
        ("LV_Euler",[5000],[0.01],[0b0011]),
        ("LV_PPM",[5000,50000],[0.01,0.01],[0b0011,0b0010]), # 0: standard analysis, 1: test for chaotic behavior
        ("LV_PPM_3",[5000],[0.01],[0b0011]),
        ("van_del_Pol",[10000],[0.01],[0b0011])
        ]
    chosen_model = 2
    chosen_params = 1

    n = models[chosen_model][1][chosen_params]
    h = models[chosen_model][2][chosen_params]
    timesteps = np.linspace(0,n*h,n)

    v = Set_Model(models[chosen_model][0],chosen_params,h)
    #For every pair (i,j) of parameters and initial values the model is iterated over, res_matrix contains the output for all variables throughout all timesteps
    res_matrix = np.empty([len(v.params_vec),len(v.inits_vec),len(timesteps),len(v.inits_names)])
    for i in range(len(v.params_vec)):
        for j in range(len(v.inits_vec)):
            mymodel = Calc_Model(v.functions,v.params_vec[i],v.inits_vec[j])
            for t in range(len(timesteps[1:])):
                mymodel.update()
                mymodel.observe()
            res_matrix[i,j,:,:] = mymodel.result
    plot_main(res_matrix,timesteps,v,models[chosen_model][3][chosen_params])

if __name__ == "__main__":
    main()