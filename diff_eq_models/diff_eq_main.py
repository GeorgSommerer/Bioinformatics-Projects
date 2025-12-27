
from diff_eq_models import *
from diff_eq_plot import *

def main():
    """
    models[i][0] is the name of the model, as has to be given as input to Set_Model
    models[i][1] is the number of timesteps n
    models[i][2] is the step size h; therefore, n*h is the total time passed
    models[i][3] is the plotting behavior: Position 0 stands for plot_timesteps, 1 for plot_trajectory_2D, 2 for plot_trajectory_3D, 3 for plot_cobweb, and 4 for plot_asymptotic
    """
    models = [
        ("Logistic",[400],[1],[0b11001]),
        ("Bifurcation",[200,30],[1,1],[0b1000,0b01001]), #0: bifurcation, 1: cobweb
        ("Logistic_Map",[100,30],[1,1],[0b10000,0b01001]), #0: bifurcation, 1: cobweb
        ("PDE_2",[30],[1],[0b00011]),
        ("LV_Euler",[5000],[0.01],[0b00011]),
        ("LV_PPM",[5000,50000],[0.01,0.01],[0b0011,0b00010]), # 0: standard analysis, 1: test for chaotic behavior
        ("LV_PPM_3",[5000],[0.01],[0b00111]),
        ("van_del_Pol",[10000],[0.01],[0b00011]), 
        ("Lorenz",[3000,3000,3000],[0.01,0.01,0.01],[0b00111,0b00111,0b00111]) # 0: vary s, 1: vary r, 2: vary b
        ]
    chosen_model = 8
    chosen_params = 2

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