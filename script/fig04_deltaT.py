"""
Script to produce Figure 4 of the manuscript with temperature difference between the fluid and solid phases (delta T) from the grain-scale heat transport model compared to the experimental data.
This script reads experimental data and model results from the grain-scale heat transport model and plots the delta T in time series.

# Author: Haegyeong Lee
"""

# import Python packages
import numpy as np
import matplotlib.pyplot as plt

# import modules in a subfolder "package" required for running the current script
from package.moose_data import MOOSE_Data
from package.moose_postprocess import MOOSE_Postprocess
from package.extractFloat import *
from package.exp_data import Exp_Data
from package.bc_depth import BC_depth


# change working directory to the script directory
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# file path for reading data
dir_data = "../data"
dir_MOOSE =  "../results/hsf_max/"
dir_BC = dir_data + "/bc_data/"
dir_MOOSE_Gossler = "../results/hsf_empirical/"


##################
## Reading data ##
##################

# list of grain size and flow velocity for the loop
list_exp = [8, 6, 5, 3, 7, 4]
list_grain_size = ['05mm','10mm','15mm','20mm','25mm','30mm']

list_T_diff_Exp_time = []
list_T_diff_Exp_all_min = []
list_T_diff_Exp_all_max = []

list_time_moose = []
list_deltaT_moose = []
list_time_moose_Gossler = []
list_deltaT_moose_Gossler = []


for exp in list_exp:

    for grain_size in list_grain_size:

        ################
        ## Parameters ##
        ################

        if exp == 4:
            q = 0.000265
            q_md = 23
            t_max = 2000
        elif exp == 7:
            q = 0.000213
            q_md = 19
            t_max = 3000
        elif exp == 3:
            q = 0.000197
            q_md = 17
            t_max = 4000
        elif exp == 5:
            q = 0.000135
            q_md = 12
            t_max = 5000
        elif exp == 6:
            q = 0.000087
            q_md = 8
            t_max = 6000
        elif exp == 8:
            q = 0.000040
            q_md = 3
            t_max = 15000

        depth = 0.2

        rho_s = 2585
        cp_s = 759
        rho_f = 1000
        cp_f = 4180
        n = 0.37
        k_f = 0.6
        k_s = 1
        beta = 0

        print("----------------- Model with the grain size of "+grain_size+" and the flow velocity of "+str(q_md)+" m/d -----------------")

        #######################################################################################################

        ##############################
        ## Model results: max. h_sf ##
        ##############################

        # reading data of boundary condition used in the model by a module ./package/moose_data.py imported as MOOSE_Data

        MOOSE_bc_temp =  'Exp'+str(exp)+'_'+grain_size+'_BC_input_temp.csv'

        MOOSE_file = "LTNE_circle_Exp" + str(exp) + "_" + grain_size
        print(f"File for the model with max. h_sf is '{MOOSE_file}'")

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
        Tf_moose = MOOSE_Postprocess(moose_output= df_moose).Tf_1_LTNE()

        T0 = round(Tf_moose[0],2)
        T1 = round(Tf_moose.max(),2)

        Tf_moose = (Tf_moose  - T0)/(T1-T0)
        Ts_moose = MOOSE_Postprocess(moose_output= df_moose).Ts_LTNE()
        Ts_moose = (Ts_moose  - T0)/(T1-T0)

        deltaT_moose = Tf_moose - Ts_moose

        list_time_moose.append(time_moose)
        list_deltaT_moose.append(deltaT_moose)

        ###################################
        ## Model results: empirical h_sf ##
        ###################################

        # reading data of model results by a module ./package/moose_postprocess.py imported as MOOSE_Postprocess

        MOOSE_file_Gossler = "LTNE_circle_hsf_empirical_Exp" + str(exp) + "_" + grain_size
        print(f"File for the model with empirical h_sf is '{MOOSE_file_Gossler}'\n")
        MOOSE_output_file_Gossler =  MOOSE_file_Gossler + '_out.csv'

        Main_MOOSE_Data = MOOSE_Data()

        df_moose_Gossler = Main_MOOSE_Data.read_output(filename_moose = dir_MOOSE_Gossler+MOOSE_output_file_Gossler)   

        time_moose_Gossler = MOOSE_Postprocess(moose_output= df_moose_Gossler).time()
        Tf_moose_Gossler = MOOSE_Postprocess(moose_output= df_moose_Gossler).Tf_1_LTNE()
        Tf_moose_Gossler = (Tf_moose_Gossler  - T0)/(T1-T0)
        Ts_moose_Gossler = MOOSE_Postprocess(moose_output= df_moose_Gossler).Ts_LTNE()
        Ts_moose_Gossler = (Ts_moose_Gossler  - T0)/(T1-T0)

        deltaT_moose_Gossler = Tf_moose_Gossler - Ts_moose_Gossler

        list_time_moose_Gossler.append(time_moose_Gossler)
        list_deltaT_moose_Gossler.append(deltaT_moose_Gossler)

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

        exp_data_Tf.columns = range(exp_data_Tf.shape[1])
        exp_data_Ts.columns = range(exp_data_Ts.shape[1])

        T_diff_Exp_all = exp_data_Tf - exp_data_Ts

        if grain_size == "20mm":
            T_diff_Exp_all = T_diff_Exp_all.iloc[:,0:exp_data_Tf.shape[1]-1]
        elif grain_size == "25mm":
            T_diff_Exp_all = T_diff_Exp_all.iloc[:,0:exp_data_Tf.shape[1]-1]


        T_diff_Exp_all_max = T_diff_Exp_all.max(axis=1)
        T_diff_Exp_all_min = T_diff_Exp_all.min(axis=1)

        BTC_Tf = exp_data_Tf.iloc[:,[0,1]]
        BTC_Ts = exp_data_Ts.iloc[:,[0,1]]


        BTC_time = np.array(exp_data_time)

        BTC_Tf_LTNE_1 = np.array(BTC_Tf.iloc[:,0])
        BTC_Tf_LTNE_2 = np.array(BTC_Tf.iloc[:,1])

        BTC_Ts_LTNE = np.array(BTC_Ts.iloc[:,0])

        BTC_Tf_LTNE = BTC_Tf_LTNE_1
        deltaT_LTNE = BTC_Tf_LTNE - BTC_Ts_LTNE

        if grain_size == "05mm":
            read_exp_bc = BC_depth(exp = exp, grain_size= grain_size,dir_exp=dir_data,dir_model_BC=dir_BC).BC_df_inlet()
        else:
            read_exp_bc = BC_depth(exp = exp, grain_size= grain_size,dir_exp=dir_data,dir_model_BC=dir_BC).BC_df_depth()


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


        # calculate the difference array
        input_difference_array = np.absolute(BTC_Tf_LTNE-BC_50_T_exp)

        # find the index of minimum element from the array
        exp_input_index = np.nanargmin(input_difference_array)

        # find the index of minimum element from the array
        exp_bc_index = np.nanargmin(np.absolute(np.array(exp_bc_T)-BC_50_T_exp))

        # crop the experimental data by matching its heat input to the boundary condition of the model results

        if input_index > exp_bc_index:
            jump = int(input_index -exp_bc_index)


            T_diff_Exp_time = exp_bc_time+jump
            exp_bc_time = exp_bc_time+jump
            
        else:


            jump = int(exp_bc_index -input_index)

            T_diff_Exp_time = exp_bc_time[jump:]-jump
            T_diff_Exp_all_min = T_diff_Exp_all_min[jump:]
            T_diff_Exp_all_max = T_diff_Exp_all_max[jump:]

        list_T_diff_Exp_time.append(T_diff_Exp_time)
        list_T_diff_Exp_all_min.append(T_diff_Exp_all_min)
        list_T_diff_Exp_all_max.append(T_diff_Exp_all_max)


#######################################################################################################
##############
## Plotting ##
##############


q_list = ["3", "8", "12", "17", "19", "23"]
grain_size_list = ["5", "10", "15", "20", "25", "30"]

ft_size =7
linewidth = 1.5
alph_exp = 0.95
alph_model = 0.25

ylim_min = -0.07
ylim_max = 0.3
yticks = [0.00, 0.15, ylim_max]

color_hsf_max = '#753A50'
color_hsf_empir = '#DDA0AD'
color_exp = '#4E8C7A'
shade_model = "#B97289"
plt.rcParams.update({'font.size': ft_size})
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

num_row = len(list_exp)
num_col = len(list_grain_size)

fig, axs = plt.subplots(num_row,num_col, figsize=(7,7))
for f in range(len(list_grain_size)):

    axs[0,f].fill_between(list_T_diff_Exp_time[f],list_T_diff_Exp_all_min[f], list_T_diff_Exp_all_max[f], facecolor=color_exp, alpha=alph_exp, label="Experimental data")
    axs[0,f].plot(list_time_moose[f],list_deltaT_moose[f], color = color_hsf_max,label= "Model (max. $h_{sf}$)",linewidth=linewidth)
    axs[0,f].plot(list_time_moose_Gossler[f],list_deltaT_moose_Gossler[f], color = color_hsf_empir,linestyle = 'dashed',label= "Model (empirical $h_{sf}$)",linewidth=1)
    axs[0,f].set_xlim(0,15000)
    axs[0,f].set_ylim(ylim_min,ylim_max)
    axs[0,f].set_yticks(yticks)

    axs[1,f].fill_between(list_T_diff_Exp_time[f+num_col],list_T_diff_Exp_all_min[f+num_col], list_T_diff_Exp_all_max[f+num_col], facecolor=color_exp, alpha=alph_exp, label="Experimental data")
    axs[1,f].plot(list_time_moose[f+num_col],list_deltaT_moose[f+num_col], color = color_hsf_max,label= "Model (max. $h_{sf}$)",linewidth=linewidth)
    axs[1,f].plot(list_time_moose_Gossler[f+num_col],list_deltaT_moose_Gossler[f+num_col], color = color_hsf_empir,linestyle = 'dashed',label= "Model (empirical $h_{sf}$)",linewidth=1)
    axs[1,f].set_xlim(0,6000)
    axs[1,f].set_ylim(ylim_min,ylim_max)
    axs[1,f].set_yticks(yticks)

        
    axs[2,f].fill_between(list_T_diff_Exp_time[f+num_col*2],list_T_diff_Exp_all_min[f+num_col*2], list_T_diff_Exp_all_max[f+num_col*2], facecolor=color_exp, alpha=alph_exp, label="Experimental data")
    axs[2,f].plot(list_time_moose[f+num_col*2],list_deltaT_moose[f+num_col*2], color = color_hsf_max,label= "Model (max. $h_{sf}$)",linewidth=linewidth)
    axs[2,f].plot(list_time_moose_Gossler[f+num_col*2],list_deltaT_moose_Gossler[f+num_col*2], color = color_hsf_empir,linestyle = 'dashed',label= "Model (empirical $h_{sf}$)",linewidth=1)
    axs[2,f].set_xlim(0,5000)
    axs[2,f].set_ylim(ylim_min,ylim_max)
    axs[2,f].set_yticks(yticks)



    axs[3,f].fill_between(list_T_diff_Exp_time[f+num_col*3],list_T_diff_Exp_all_min[f+num_col*3], list_T_diff_Exp_all_max[f+num_col*3], facecolor=color_exp, alpha=alph_exp, label="Experimental data")
    axs[3,f].plot(list_time_moose[f+num_col*3],list_deltaT_moose[f+num_col*3], color = color_hsf_max,label= "Model (max. $h_{sf}$)",linewidth=linewidth)    
    axs[3,f].plot(list_time_moose_Gossler[f+num_col*3],list_deltaT_moose_Gossler[f+num_col*3], color = color_hsf_empir,linestyle = 'dashed',label= "Model (empirical $h_{sf}$)",linewidth=1)
    axs[3,f].set_xlim(0,4000)
    axs[3,f].set_ylim(ylim_min,ylim_max)
    axs[3,f].set_yticks(yticks)

    
    axs[4,f].fill_between(list_T_diff_Exp_time[f+num_col*4],list_T_diff_Exp_all_min[f+num_col*4], list_T_diff_Exp_all_max[f+num_col*4], facecolor=color_exp, alpha=alph_exp, label="Experimental data")
    axs[4,f].plot(list_time_moose[f+num_col*4],list_deltaT_moose[f+num_col*4], color = color_hsf_max,label= "Model (max. $h_{sf}$)",linewidth=linewidth)
    axs[4,f].plot(list_time_moose_Gossler[f+num_col*4],list_deltaT_moose_Gossler[f+num_col*4], color = color_hsf_empir,linestyle = 'dashed',label= "Model (empirical $h_{sf}$)",linewidth=1)
    axs[4,f].set_xlim(0,3000)
    axs[4,f].set_ylim(ylim_min,ylim_max)
    axs[4,f].set_yticks(yticks)



    axs[5,f].fill_between(list_T_diff_Exp_time[f+6*5],list_T_diff_Exp_all_min[f+6*5], list_T_diff_Exp_all_max[f+6*5], facecolor=color_exp, alpha=alph_exp, label="Experimental data")
    axs[5,f].plot(list_time_moose[f+6*5],list_deltaT_moose[f+6*5], color = color_hsf_max,label= "Model (max. $h_{sf}$)",linewidth=linewidth)
    axs[5,f].plot(list_time_moose_Gossler[f+6*5],list_deltaT_moose_Gossler[f+6*5], color = color_hsf_empir,linestyle = 'dashed',label= "Model (empirical $h_{sf}$)",linewidth=linewidth)
    axs[5,f].set_xlim(0,2000)
    axs[5,f].set_xlabel("Time [s]")
    axs[5,f].set_ylim(ylim_min,ylim_max)
    axs[5,f].set_yticks(yticks)
        

    for k in range(num_row):
        if k == 0:
            axs[k,f].text(2500, 0.35,  f'$d_p$ = {grain_size_list[f]} mm', fontsize=7)


        if f == 0:
            axs[k,f].set_ylabel('$q$ = '+q_list[k]+' m d$^{-1}$ \n\n Normalized $\Delta$T [-]', labelpad=5, fontsize=7)
        if not f == 0:
            axs[k,f].set_yticklabels([])
            


lines = [] 
labels = [] 
  
for ax in fig.axes: 
    Line, Label = ax.get_legend_handles_labels() 
    lines.extend(Line) 
    labels.extend(Label) 

labels_1 = [labels[i] for i in range(3)]
labels= labels_1

# create a single legend for the entire figure
fig.legend(lines, labels, loc='upper left', bbox_to_anchor=(0.32, 0.96), ncol=3, frameon=False,fontsize="7",markerscale=4) 

fig.align_ylabels(axs[:])
plt.subplots_adjust(wspace=0.2,hspace=0.3) 
# plt.savefig("fig04_deltaT.png",bbox_inches='tight')
plt.show()
