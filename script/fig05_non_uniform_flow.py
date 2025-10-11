"""
Script to produce Figure 5 of the manuscript with temperature difference between the fluid and solid phases (delta T) from the non-uniform flow heat transport model compared to the experimental data.
This script reads experimental data and model results from the non-uniform flow model and plots the delta T in time series.

# Author: Haegyeong Lee
"""

# Import Python packages
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd

# Import modules in a subfolder "package" required for running the current script
from package.moose_data import MOOSE_Data
from package.moose_postprocess import MOOSE_Postprocess
from package.extractFloat import *
from package.exp_data import Exp_Data
from package.bc_depth import BC_depth

# Change working directory to the script directory
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# file path for reading data
dir_data = "../data"
dir_MOOSE =  "../results/non_uniform_flow/"
dir_BC = dir_data + "/bc_data/"

##################
## Reading data ##
##################

# selecting non-uniform flow model, grain size and flow velocity
K_dist_list = [1, 2, 3]
exp_list = [3, 4]
grain_size_list = ["05mm", "15mm"]

list_time_moose = []
list_deltaT_moose_1 = []
list_deltaT_moose_2 = []
list_exp_data_time = []
list_omega = []



for grain_size in grain_size_list:
    
    for exp in exp_list:

        for K_dist in K_dist_list:

            ###############
            ## Parameter ##
            ###############

            if exp == 4:
                q = 0.000265
                t_max = 2000
            elif exp == 7:
                q = 0.000213
                t_max = 3000
            elif exp == 3:
                q = 0.000197
                t_max = 4000
            elif exp == 5:
                q = 0.000135
                t_max = 5000
            elif exp == 6:
                q = 0.000087
                t_max = 6000
            elif exp == 8:
                q = 0.000040
                t_max = 15000

            depth = 0.2

            rho_s = 2585
            cp_s = 759
            rho_f = 997
            cp_f = 4180
            n = 0.37
            k_f = 0.6
            k_s = 1
            mu = 0.001002
            g = 9.8
            K_hyd = 0.00323
            beta = 0

            #######################################################################################################

            ###########################################
            ## Model results: non-uniform flow model ##
            ###########################################

            # reading data of boundary condition used in the model by a module ./package/moose_data.py imported as MOOSE_Data

            MOOSE_bc_temp =  'Exp'+str(exp)+'_'+grain_size+'_BC_input_temp.csv'

            MOOSE_file = "LTNE_circle_K_dist_" + str(K_dist) + "_Exp" + str(exp) + "_" + grain_size
            print("File for the non-uniform model is ", MOOSE_file)

            MOOSE_output_file =  MOOSE_file + '_out.csv'
            MOOSE_input_file = MOOSE_file + '.i'

            Main_MOOSE_Data = MOOSE_Data()

            read_MOOSE_bc = Main_MOOSE_Data.read_IC_knownT(filename_bc = dir_BC +MOOSE_bc_temp)

            read_bc_T = read_MOOSE_bc.iloc[:,1]
            read_bc_time = read_MOOSE_bc.iloc[:,0]
            T0_moose_bc = round(read_bc_T[0],2)
            T1_moose_bc = round(read_bc_T.max(),2)

            read_bc_T = (read_bc_T  - T0_moose_bc)/(T1_moose_bc-T0_moose_bc)

            # reading data of model results by a module ./package/moose_postprocess.py imported as MOOSE_Postprocess

            df_moose = Main_MOOSE_Data.read_output(filename_moose = dir_MOOSE+MOOSE_output_file)   

            time_moose = MOOSE_Postprocess(moose_output= df_moose).time()
            Tf_moose_1 = MOOSE_Postprocess(moose_output= df_moose).Tf_1_LTNE()
            Tf_moose_2 = MOOSE_Postprocess(moose_output= df_moose).Tf_2_LTNE()

            T0 = round(Tf_moose_1[0],2)
            T1 = round(Tf_moose_1.max(),2)

            Tf_moose_1 = (Tf_moose_1  - T0)/(T1-T0)
            Tf_moose_2 = (Tf_moose_2  - T0)/(T1-T0)
            Ts_moose = MOOSE_Postprocess(moose_output= df_moose).Ts_LTNE()
            Ts_moose = (Ts_moose  - T0)/(T1-T0)

            deltaT_moose_1 = Tf_moose_1 - Ts_moose
            deltaT_moose_2 = Tf_moose_2 - Ts_moose

            list_time_moose.append(time_moose)
            list_deltaT_moose_1.append(deltaT_moose_1)
            list_deltaT_moose_2.append(deltaT_moose_2)

            
            ### Permeability in non-uniform flow model domain #################################################
            
            df_K = pd.read_csv("K_vari_permeability.csv")

            rows_grain_size = df_K.loc[df_K['size'] == grain_size ]  # Select rows with index labels 0 and 2
            k_left = rows_grain_size.loc[rows_grain_size['K_vari'] == "K"+str(K_dist),'k_left'].values[0]
            k_right = rows_grain_size.loc[rows_grain_size['K_vari'] == "K"+str(K_dist),'k_right'].values[0]

            omega = k_left/k_right

            list_omega.append(omega)
            

        #######################################################################################################
        #######################
        ## Experimental data ##
        #######################

        # reading experimental data by a module ./package/exp_data.py imported as MOOSE_Postprocess

        select_probe = Exp_Data(exp = str(exp), dir_data=dir_data, grain_size=grain_size)

        BTC_T_Exp = select_probe.read_exp_data()

        exp_data_time = select_probe.read_exp_data_time()
        exp_data_Tf = select_probe.read_exp_data_Tf()
        exp_data_Ts = select_probe.read_exp_data_Ts()

        list_exp_data_time.append(exp_data_time)

        exp_data_Tf.columns = range(exp_data_Tf.shape[1])
        exp_data_Ts.columns = range(exp_data_Ts.shape[1])

        T_diff_Exp_all = exp_data_Tf - exp_data_Ts

        if grain_size == "20mm":
            T_diff_Exp_all = T_diff_Exp_all.iloc[:,0:exp_data_Tf.shape[1]-1]
        elif grain_size == "25mm":
            T_diff_Exp_all = T_diff_Exp_all.iloc[:,0:exp_data_Tf.shape[1]-1]

        T_diff_Exp_all_max = T_diff_Exp_all.max(axis=1)
        T_diff_Exp_all_min = T_diff_Exp_all.min(axis=1)


        if grain_size == "05mm":
            read_exp_bc = BC_depth(exp = exp, grain_size= grain_size, dir_exp=dir_data, dir_model_BC=dir_BC).BC_df_inlet()
        else:
            read_exp_bc = BC_depth(exp = exp, grain_size= grain_size, dir_exp=dir_data, dir_model_BC=dir_BC).BC_df_depth()


        exp_bc_T = read_exp_bc.iloc[:,1]
        exp_bc_time = read_exp_bc.iloc[:,0]

        ## Post processing ######################################################################

        # find t_50 for boundary condition input in the model

        T0_bc = round(read_bc_T[0],2)
        T1_bc = round(read_bc_T.max(),2)

        BC_input_50 = (T1_bc + T0_bc)/2

        # find the index of t_50 
        input_difference_array = np.absolute(read_bc_T-BC_input_50)
        input_index = np.nanargmin(input_difference_array) 

        BC_50_T_exp = 0.5

        exp_bc_index = np.nanargmin(np.absolute(np.array(exp_bc_T)-BC_50_T_exp))

        jump = int(exp_bc_index -input_index)

        # crop the experimental data by matching its heat input to the boundary condition of the model results
        
        if exp == exp_list[0] and grain_size == grain_size_list[0]:
            T_diff_Exp_time_1 = exp_bc_time[jump:]-jump
            T_diff_Exp_all_min_1 = T_diff_Exp_all_min[jump:]
            T_diff_Exp_all_max_1 = T_diff_Exp_all_max[jump:]

            T_diff_Exp_all_1 = T_diff_Exp_all[jump:]


        elif exp == exp_list[1] and grain_size == grain_size_list[0]:
            T_diff_Exp_time_2 = exp_bc_time[jump:]-jump
            T_diff_Exp_all_2 = T_diff_Exp_all[jump:]
            T_diff_Exp_all_min_2 = T_diff_Exp_all_min[jump:]
            T_diff_Exp_all_max_2 = T_diff_Exp_all_max[jump:]

        elif exp == exp_list[0] and grain_size == grain_size_list[1]:
            T_diff_Exp_time_3 = exp_bc_time[jump:]-jump
            T_diff_Exp_all_min_3 = T_diff_Exp_all_min[jump:]
            T_diff_Exp_all_max_3 = T_diff_Exp_all_max[jump:]

            T_diff_Exp_all_3 = T_diff_Exp_all[jump:]


        elif exp == exp_list[1] and grain_size == grain_size_list[1]:
            T_diff_Exp_time_4 = exp_bc_time[jump:]-jump
            T_diff_Exp_all_4 = T_diff_Exp_all[jump:]
            T_diff_Exp_all_min_4 = T_diff_Exp_all_min[jump:]
            T_diff_Exp_all_max_4 = T_diff_Exp_all_max[jump:]


#######################################################################################################
##############
## Plotting ##
##############

grain_size_list_plt = ['5 mm','15 mm']

xlim_max_exp4 = 2000
xlim_max_exp3 = 2500

ylim = [-0.05,0.2]
ylim_2 = [-0.05,0.2]
title_x = 650
title_x_model = 450
title_y = 0.17
title_y_2 = 0.17
title_x_led_1 = 1400
title_y_led_1 = 0.14


ft_size = 8
ft_size_legend = 6

line = 1.5

plt.rcParams.update({'font.size': ft_size})
plt.rcParams['axes.linewidth'] = 1
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.top'] = False
plt.rcParams['ytick.right'] = True

color_exp ='#5C9E88'



color_model =   [
    "#E4A2A7",  # Cool Blush Rose
    "#C36B74",  # Muted Mauve Red
    "#8B404C"   # Desaturated Plum Clay
]

color_list = [
    "#C4E3CB",  # Pale Mint
    "#B2E19B",  # Frosted Lime
    "#A0DA92",  # Celery Green
    "#88D27F",  # Fresh Meadow
    "#70C873",  # Muted Jade
    "#5EBB8A",  # Seafoam Green
    "#4EAD7E",  # Sage Mist
    "#3D9F73"   # Soft Teal Green
]

replica_label = [r'replica 1 - $\Delta T_{L}$', r'replica 1 - $\Delta T_{R}$', r'replica 2 - $\Delta T_{L}$', r'replica 2 - $\Delta T_{R}$', r'replica 3 - $\Delta T_{L}$', r'replica 3 - $\Delta T_{R}$', r'replica 4 - $\Delta T_{L}$', r'replica 4 - $\Delta T_{R}$']

colors = ['tab:blue', 'tab:orange', 'tab:green']  # Colors for A, B, C

fig, axs = plt.subplots(4,2, figsize=(6,7))


for q in range(T_diff_Exp_all_1.shape[1]):

    color_list= color_list

    axs[0,0].scatter(T_diff_Exp_time_1, T_diff_Exp_all_1.iloc[:,q], label= replica_label[q], color = color_list[q],s=2) 
    axs[0,0].set_xticklabels([])
    axs[0,0].set_yticklabels([])
    axs[0,0].set_xlim([0,xlim_max_exp3])
    axs[0,0].set_ylim(ylim)
    axs[0,0].yaxis.tick_right()
    axs[0,0].text(xlim_max_exp3*0.27,title_y_2,"Experimental $\Delta$$T(t)$")
    axs[0,0].text(900, 0.24,  '$d_p$ = '+grain_size_list_plt[0])
    axs[0,0].text(-0.22*xlim_max_exp3, -0.09, '$q$ = 17 m d$^{-1}$', rotation=90, va='center')

        
fill = axs[1,0].fill_between(T_diff_Exp_time_1,T_diff_Exp_all_min_1, T_diff_Exp_all_max_1, facecolor=color_exp, alpha=0.35, label="Experimental $\Delta$$T$ range")
axs[1,0].plot(list_time_moose[0],list_deltaT_moose_1[0], color = color_model[0],label= "Model ($\omega$= "+str(round(list_omega[0],2))+ ")",linewidth=line)
axs[1,0].plot(list_time_moose[1],list_deltaT_moose_1[1], color = color_model[1],label= "Model ($\omega$= "+str(round(list_omega[1],2))+ ")",linewidth=line)
axs[1,0].plot(list_time_moose[2],list_deltaT_moose_1[2], color =  color_model[2],label= "Model ($\omega$= "+str(round(list_omega[2],2))+ ")",linewidth=line)
axs[1,0].plot(list_time_moose[0],list_deltaT_moose_2[0], linestyle='--', color = color_model[0],label= "Model ($\omega$= "+str(round(list_omega[0],2))+ ")",linewidth=line)
axs[1,0].plot(list_time_moose[1],list_deltaT_moose_2[1], linestyle='--', color = color_model[1],label= "Model ($\omega$= "+str(round(list_omega[1],2))+ ")",linewidth=line)
axs[1,0].plot(list_time_moose[2],list_deltaT_moose_2[2], linestyle='--', color =  color_model[2],label= "Model ($\omega$= "+str(round(list_omega[2],2))+ ")",linewidth=line)
axs[1,0].set_xlim([0,xlim_max_exp3])
axs[1,0].set_ylim(ylim)
axs[1,0].set_xticklabels([])
axs[1,0].set_yticklabels([])
axs[1,0].yaxis.tick_right()
axs[1,0].text(xlim_max_exp3*0.15,title_y_2,"Modeled $\Delta$$T(t)$ with varied $\omega$")
scenarios = ["$\omega$= "+str(round(list_omega[0],2)), "$\omega$= "+str(round(list_omega[1],2)), "$\omega$= "+str(round(list_omega[2],2))]
case_styles = ['-', '--']  # Case 1 and Case 2
scenario_legend = [
            Line2D([0], [0], color=color_model[k], lw=1.5, label=f'{scenarios[k]}')
            for k in range(0, len(scenarios))  # Only B and C
        ]

# Add legend to subplot
axs[1,0].legend(handles=scenario_legend , loc='upper right',bbox_to_anchor=(0.96, 0.82), fontsize=ft_size_legend, frameon=False,handlelength=1.2)


for k in range(T_diff_Exp_all_2.shape[1]):

    color_list= color_list

    axs[2,0].scatter(T_diff_Exp_time_2, T_diff_Exp_all_2.iloc[:,k], label=  replica_label[k], color = color_list[k],s=2)
    axs[2,0].set_xlim([0,xlim_max_exp4])
    axs[2,0].set_xticklabels([])
    axs[2,0].set_yticklabels([])
    axs[2,0].yaxis.tick_right()
    axs[2,0].set_ylim(ylim_2)
    axs[2,0].text(xlim_max_exp4*0.27,title_y_2,"Experimental $\Delta$$T(t)$")
    axs[2,0].text(-0.22*xlim_max_exp4, -0.09, '$q$ = 23 m d$^{-1}$', rotation=90, va='center')

axs[3,0].fill_between(T_diff_Exp_time_2,T_diff_Exp_all_min_2, T_diff_Exp_all_max_2, facecolor=color_exp, alpha=0.35, label="Experimental $\Delta$$T$ range")
axs[3,0].plot(list_time_moose[3],list_deltaT_moose_1[3], color = color_model[0],label= "Model ($\omega$= "+str(round(list_omega[3],2))+ ")",linewidth=line)
axs[3,0].plot(list_time_moose[4],list_deltaT_moose_1[4], color = color_model[1],label= "Model ($\omega$= "+str(round(list_omega[4],2))+ ")",linewidth=line)
axs[3,0].plot(list_time_moose[5],list_deltaT_moose_1[5], color = color_model[2],label= "Model ($\omega$= "+str(round(list_omega[5],2))+ ")",linewidth=line)
axs[3,0].plot(list_time_moose[3],list_deltaT_moose_2[3], linestyle='--', color = color_model[0],label= "Model ($\omega$= "+str(round(list_omega[3],2))+ ")",linewidth=line)
axs[3,0].plot(list_time_moose[4],list_deltaT_moose_2[4], linestyle='--', color = color_model[1],label= "Model ($\omega$= "+str(round(list_omega[4],2))+ ")",linewidth=line)
axs[3,0].plot(list_time_moose[5],list_deltaT_moose_2[5], linestyle='--', color =  color_model[2],label= "Model ($\omega$= "+str(round(list_omega[5],2))+ ")",linewidth=line)
axs[3,0].set_xlim([0,xlim_max_exp4])
axs[3,0].set_ylim(ylim_2)
axs[3,0].set_xticklabels([])
axs[3,0].set_yticklabels([])
axs[3,0].yaxis.tick_right()
axs[3,0].text(xlim_max_exp4*0.15,title_y_2,"Modeled $\Delta$$T(t)$ with varied $\omega$")
scenarios = ["$\omega$= "+str(round(list_omega[3],2)), "$\omega$= "+str(round(list_omega[4],2)), "$\omega$= "+str(round(list_omega[5],2))]
scenario_legend = [
            Line2D([0], [0], color=color_model[k], lw=1.5, label=f'{scenarios[k]}')
            for k in range(0, len(scenarios))  # Only B and C
        ]
axs[3,0].legend(handles=scenario_legend , loc='upper right',bbox_to_anchor=(0.96, 0.82), fontsize=ft_size_legend, frameon=False,handlelength=1.2)

for q in range(T_diff_Exp_all_3.shape[1]):

    color_list= color_list

    axs[0,1].scatter(T_diff_Exp_time_3, T_diff_Exp_all_3.iloc[:,q], label= replica_label[q], color = color_list[q],s=2)
    axs[0,1].set_xticklabels([])
    axs[0,1].set_yticklabels([])
    axs[0,1].yaxis.tick_right()
    axs[0,1].set_xlim([0,xlim_max_exp3])
    axs[0,1].set_ylim(ylim)
    axs[0,1].text(xlim_max_exp3*0.27,title_y_2,"Experimental $\Delta$$T(t)$")
    axs[0,1].text(900, 0.24,  '$d_p$ = '+grain_size_list_plt[1])

axs[1,1].fill_between(T_diff_Exp_time_3,T_diff_Exp_all_min_3, T_diff_Exp_all_max_3, facecolor=color_exp, alpha=0.35, label="Experimental $\Delta$$T$ range")
axs[1,1].plot(list_time_moose[6],list_deltaT_moose_1[6], color =  color_model[0],label= "Model ($\omega$= "+str(round(list_omega[6],2))+ ")",linewidth=line)
axs[1,1].plot(list_time_moose[7],list_deltaT_moose_1[7], color = color_model[1],label= "Model ($\omega$= "+str(round(list_omega[7],2))+ ")",linewidth=line)
axs[1,1].plot(list_time_moose[8],list_deltaT_moose_1[8], color = color_model[2],label= "Model ($\omega$= "+str(round(list_omega[8],2))+ ")",linewidth=line)
axs[1,1].plot(list_time_moose[6],list_deltaT_moose_2[6], linestyle='--', color = color_model[0],label= "Model ($\omega$= "+str(round(list_omega[6],2))+ ")",linewidth=line)
axs[1,1].plot(list_time_moose[7],list_deltaT_moose_2[7], linestyle='--', color = color_model[1],label= "Model ($\omega$= "+str(round(list_omega[7],2))+ ")",linewidth=line)
axs[1,1].plot(list_time_moose[8],list_deltaT_moose_2[8], linestyle='--', color =  color_model[2],label= "Model ($\omega$= "+str(round(list_omega[8],2))+ ")",linewidth=line)
axs[1,1].set_xlim([0,xlim_max_exp3])
axs[1,1].set_ylim(ylim)
axs[1,1].set_xticklabels([])
axs[1,1].yaxis.set_label_position('right')
axs[1,1].yaxis.tick_right()
axs[1,1].set_ylabel('Normalized $\Delta$T [-]')
axs[1,1].text(xlim_max_exp3*0.15,title_y_2,"Modeled $\Delta$$T(t)$ with varied $\omega$")
scenarios = ["$\omega$= "+str(round(list_omega[6],2)), "$\omega$= "+str(round(list_omega[7],2)), "$\omega$= "+str(round(list_omega[8],2))]
scenario_legend = [
            Line2D([0], [0], color=color_model[k], lw=1.5, label=f'{scenarios[k]}')
            for k in range(0, len(scenarios))  # Only B and C
        ]
axs[1,1].legend(handles=scenario_legend , loc='upper left',bbox_to_anchor=(0.03, 0.82), fontsize=ft_size_legend, frameon=False,handlelength=1.2)

for k in range(T_diff_Exp_all_4.shape[1]):

    color_list= color_list


    axs[2,1].scatter(T_diff_Exp_time_4, T_diff_Exp_all_4.iloc[:,k], label= replica_label[k], color = color_list[k],s=2)
    axs[2,1].set_xlim([0,xlim_max_exp4])
    axs[2,1].set_xticklabels([])
    axs[2,1].set_yticklabels([])
    axs[2,1].yaxis.tick_right()
    axs[2,1].set_ylim(ylim_2)
    axs[2,1].text(xlim_max_exp4*0.27,title_y_2,"Experimental $\Delta$$T(t)$")

axs[3,1].fill_between(T_diff_Exp_time_4,T_diff_Exp_all_min_4, T_diff_Exp_all_max_4, facecolor=color_exp, alpha=0.35, label="Experimental $\Delta$$T$ range")
axs[3,1].plot(list_time_moose[9],list_deltaT_moose_1[9], color = color_model[0],label= "Model ($\omega$= "+str(round(list_omega[9],2))+ ")",linewidth=line)
axs[3,1].plot(list_time_moose[10],list_deltaT_moose_1[10], color =  color_model[1],label= "Model ($\omega$= "+str(round(list_omega[10],2))+ ")",linewidth=line)
axs[3,1].plot(list_time_moose[11],list_deltaT_moose_1[11], color = color_model[2],label= "Model ($\omega$= "+str(round(list_omega[11],2)) + ")",linewidth=line)
axs[3,1].plot(list_time_moose[9],list_deltaT_moose_2[9], linestyle='--', color = color_model[0],label= "Model ($\omega$= "+str(round(list_omega[9],2))+ ")",linewidth=line)
axs[3,1].plot(list_time_moose[10],list_deltaT_moose_2[10], linestyle='--', color = color_model[1],label= "Model ($\omega$= "+str(round(list_omega[10],2))+ ")",linewidth=line)
axs[3,1].plot(list_time_moose[11],list_deltaT_moose_2[11], linestyle='--', color =  color_model[2],label= "Model ($\omega$= "+str(round(list_omega[11],2))+ ")",linewidth=line)
axs[3,1].set_xlim([0,xlim_max_exp4])
axs[3,1].set_ylim(ylim_2)
axs[3,1].set_xlabel("Time [s]")
axs[3,1].yaxis.set_label_position('right')
axs[3,1].yaxis.tick_right()
axs[3,1].set_ylabel('Normalized $\Delta$T [-]')
axs[3,1].text(xlim_max_exp4*0.15,title_y_2,"Modeled $\Delta$$T(t)$ with varied $\omega$")
scenarios = ["$\omega$= "+str(round(list_omega[9],2)), "$\omega$= "+str(round(list_omega[10],2)), "$\omega$= "+str(round(list_omega[11],2))]
scenario_legend = [
            Line2D([0], [0], color=color_model[k], lw=2, label=f'{scenarios[k]}')
            for k in range(0, len(scenarios))  # Only B and C
        ]
axs[3,1].legend(handles=scenario_legend , loc='upper left',bbox_to_anchor=(0.03, 0.82), fontsize=ft_size_legend, frameon=False,handlelength=1.2)


lines_1 = [] 
labels = [] 
  
for ax in fig.axes: 
    Line, Label = ax.get_legend_handles_labels() 
    # print(Label) 
    lines_1.extend(Line) 
    labels.extend(Label) 

labels_1 = [labels[i] for i in range(18)]
# labels_2 = [labels[k] for k in (6,7,8)]
labels_exp= replica_label
labels_exp_range= r'Experimental $\Delta T$ range'
labels_model_left= r'Modeled $\Delta T_{L}$'
labels_model_right= r'Modeled $\Delta T_{R}$'
print(labels_exp)

lines_exp= lines_1[5:13]
lines_exp_range= lines_1[13]
lines_model_left= lines_1[14]
lines_model_right= lines_1[17]

labels = labels_exp + [labels_exp_range] + [labels_model_left] + [labels_model_right]

lines = lines_exp + [lines_exp_range] + [lines_model_left] + [lines_model_right]
print(lines)


fig.legend(
    handles=lines[:8],
    labels=labels[:8],
    loc='upper left',
    bbox_to_anchor=(0.05, 1.005),
    ncol=4,
    columnspacing=1.0,
    handletextpad=0.5,
    labelspacing=0.8,
    fontsize='small',markerscale=2,
    frameon=False
)

custom_handles = [
    
    fill,  
    Line2D([0], [0], color='k', linestyle='-'),                  
    Line2D([0], [0], color='k', linestyle='--')                 
]

fig.legend(
    handles=custom_handles,
    labels=labels[8:],
    loc='upper left',
    bbox_to_anchor=(0.73, 1.005),  
    ncol=1,
    handletextpad=0.5,
    labelspacing=0.5,
    fontsize='small',
    frameon=False
)

fig.align_ylabels(axs[:])
plt.subplots_adjust(wspace=0.1,hspace=0.1) 
# plt.savefig("fig05_deltaT_non_uniform_flow.png", bbox_inches='tight')
plt.show()

