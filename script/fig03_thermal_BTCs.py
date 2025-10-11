"""
Script to produce Figure 3 of the manuscript with thermal breakthrough curves (BTCs) from grain-scale heat transport model compared to the experimental data.
This script reads experimental data and model results and plots the thermal BTCs.

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

# selecting grain size and flow velocity
exp_list = [7, 4]
grain_size_list = ['20mm','30mm']

# selecting a replica among 4 replicas for a specific grain size and flow velocity
replica_list = [3, 3, 3, 2]
select_Tf_list = [2, 1, 2, 2]

count = -1

list_BTC_time = []
list_BTC_Tf_LTNE = []
list_BTC_Ts_LTNE = []

list_time_moose = []
list_Tf_moose = []
list_Ts_moose = []

list_time_moose_Gossler = []
list_Tf_moose_Gossler = []
list_Ts_moose_Gossler = []
list_hsf_moose_Gossler =[]

list_replica_in = []
list_select_Tf = []

for exp in exp_list:

    for grain_size in grain_size_list:

        count = int(count + 1)

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
            q = 0.000004
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

        print("-------------------------------------- Model with the grain size of "+grain_size+" and the flow velocity of "+str(q_md)+" m/d --------------------------------------")

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

        # Sampling Tf of one temperature sensor from experimental data ##############################

        replica = replica_list[count]

        list_replica_in.append(replica)


        replica_unit = [(replica - 1)*2, (replica - 1)*2 + 1]

        BTC_Tf = exp_data_Tf.iloc[:,[replica_unit[0],replica_unit[1]]]
        BTC_Ts = exp_data_Ts.iloc[:,[replica_unit[0],replica_unit[1]]]

        BTC_time = np.array(exp_data_time)

        BTC_Tf_LTNE_1 = np.array(BTC_Tf.iloc[:,0])
        BTC_Tf_LTNE_2 = np.array(BTC_Tf.iloc[:,1])

        BTC_Ts_LTNE = np.array(BTC_Ts.iloc[:,0])

        select_Tf = str(select_Tf_list[count])


        list_select_Tf.append(select_Tf)

        if select_Tf == "1":

            BTC_Tf_LTNE = BTC_Tf_LTNE_1
            deltaT_LTNE = BTC_Tf_LTNE - BTC_Ts_LTNE

        elif select_Tf == "2":
            BTC_Tf_LTNE = BTC_Tf_LTNE_2
            deltaT_LTNE = BTC_Tf_LTNE - BTC_Ts_LTNE

       
        ## Post processing ######################################################################

        # find t_50 for boundary condition input in the model

        T0_bc = round(read_bc_T[0],2)
        T1_bc = round(read_bc_T.max(),2)

        BC_input_50 = (T1_bc + T0_bc)/2

        # find the index of t_50 
        input_difference_array = np.absolute(read_bc_T-BC_input_50)        
        input_index = np.nanargmin(input_difference_array)


        # find t_50 for boundary condition measured in experiments
        read_exp_bc = BC_depth(exp = exp, grain_size= grain_size, dir_exp=dir_data, dir_model_BC=dir_BC).BC_df_depth()


        exp_bc_T = read_exp_bc.iloc[:,1]
        exp_bc_time = read_exp_bc.iloc[:,0]


        BC_50_T_exp = 0.5

        # find the index of minimum element from the array
        exp_bc_index = np.nanargmin(np.absolute(np.array(exp_bc_T)-BC_50_T_exp))

        jump = int(exp_bc_index -input_index)

        # crop the experimental data by matching its heat input to the boundary condition of the model results

        BTC_time = BTC_time[jump:]-jump
        BTC_Tf_LTNE = BTC_Tf_LTNE[jump:]
        BTC_Ts_LTNE = BTC_Ts_LTNE[jump:]

        list_BTC_time.append(BTC_time)
        list_BTC_Tf_LTNE.append(BTC_Tf_LTNE)
        list_BTC_Ts_LTNE.append(BTC_Ts_LTNE)

        list_time_moose.append(time_moose)
        list_Tf_moose.append(Tf_moose)
        list_Ts_moose.append(Ts_moose)

        list_time_moose_Gossler.append(time_moose_Gossler)
        list_Tf_moose_Gossler.append(Tf_moose_Gossler)
        list_Ts_moose_Gossler.append(Ts_moose_Gossler)


#######################################################################################################
##############
## Plotting ##
##############

grain_size_list_plt = ['20 mm','30 mm']


plt.rcParams.update({'font.size': 8})
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300


color_model =   [
    "#E4A2A7",  # Cool Blush Rose
    "#C36B74",  # Muted Mauve Red
    "#8B404C"   # Desaturated Plum Clay
]
linewidth = 2
linewidth_s = 1.8
markersize_x = 3.5
markersize_o = 2.5


fig, axs = plt.subplots(2,2, figsize=(6,4))

axs[0,0].scatter(list_BTC_time[0], list_BTC_Tf_LTNE[0], color ='#1E90FF',label= "T$_\mathrm{f}$ - Experimental data",s=3)
axs[0,0].scatter(list_BTC_time[0], list_BTC_Ts_LTNE[0], color ='lightgreen',label= "T$_\mathrm{s}$ - Experimental data",s=3)
axs[0,0].plot(list_time_moose[0], list_Tf_moose[0], color =  color_model[2],label= "T$_\mathrm{f}$ - Model (max. $h_{sf}$)",linewidth=linewidth)
axs[0,0].plot(list_time_moose[0], list_Ts_moose[0], color =  color_model[2],linestyle='-', marker='o', markevery=80,markersize=markersize_o,label= "T$_\mathrm{s}$ - Model (max. $h_{sf}$)",linewidth=linewidth_s)
axs[0,0].plot(list_time_moose_Gossler[0], list_Tf_moose_Gossler[0], color = color_model[0],linestyle = 'dashed', label= "T$_\mathrm{f}$ - Model (empirical $h_{sf}$)",linewidth=linewidth)
axs[0,0].plot(list_time_moose_Gossler[0], list_Ts_moose_Gossler[0], color = color_model[0], linestyle=(0, (1, 1)),label= "T$_\mathrm{s}$ - Model (empirical $h_{sf}$)",linewidth=linewidth_s)
axs[0,0].text(1200, 1.2,  '$d_p$ = '+grain_size_list_plt[0], fontsize=8)
axs[0,0].set_xlim(0,3000)
axs[0,0].set_ylabel('$q$ = 19 m d$^{-1}$ \n\n Normalized temperature [-]', labelpad=10)


axs[0,1].scatter(list_BTC_time[1], list_BTC_Tf_LTNE[1], color ='#1E90FF',label= "Tf - Experimental data",s=3)
axs[0,1].scatter(list_BTC_time[1], list_BTC_Ts_LTNE[1], color ='lightgreen',label= "Ts - Experimental data",s=3)
axs[0,1].plot(list_time_moose[1], list_Tf_moose[1],color = color_model[2],label= "Tf - Model (Max. $h_{sf}$)",linewidth=linewidth)
axs[0,1].plot(list_time_moose[1], list_Ts_moose[1],color =  color_model[2],linestyle='-', marker='o', markevery=80,markersize=markersize_o,label= "Ts - Model (Max. $h_{sf}$)",linewidth=linewidth_s)
axs[0,1].plot(list_time_moose_Gossler[1], list_Tf_moose_Gossler[1], color = color_model[0],linestyle = 'dashed',label= "Tf - Model (Empirical $h_{sf}$)",linewidth=linewidth)
axs[0,1].plot(list_time_moose_Gossler[1], list_Ts_moose_Gossler[1], color = color_model[0], linestyle=(0, (1, 1)),label= "Ts - Model (Empirical $h_{sf}$)",linewidth=linewidth_s)

axs[0,1].set_xlim(0,3000)
axs[0,1].text(1200, 1.2,  '$d_p$ = '+grain_size_list_plt[1], fontsize=8)
axs[0,1].set_yticklabels([])


axs[1,0].scatter(list_BTC_time[2], list_BTC_Tf_LTNE[2], color ='#1E90FF',label= "Tf - Experimental data",s=3)
axs[1,0].scatter(list_BTC_time[2], list_BTC_Ts_LTNE[2], color ='lightgreen',label= "Ts - Experimental data",s=3)
axs[1,0].plot(list_time_moose[2], list_Tf_moose[2],color =  color_model[2],label= "Tf - Model (Max. $h_{sf}$)",linewidth=linewidth)
axs[1,0].plot(list_time_moose[2], list_Ts_moose[2],color = color_model[2],linestyle='-', marker='o', markevery=80,markersize=markersize_o,label= "Ts - Model (Max. $h_{sf}$)",linewidth=linewidth_s)
axs[1,0].plot(list_time_moose_Gossler[2], list_Tf_moose_Gossler[2], color = color_model[0],linestyle = 'dashed',label="Tf - Model (Empirical $h_{sf}$)",linewidth=linewidth)
axs[1,0].plot(list_time_moose_Gossler[2], list_Ts_moose_Gossler[2], color = color_model[0], linestyle=(0, (1, 1)), label= "Ts - Model (Empirical $h_{sf}$)",linewidth=linewidth_s)
axs[1,0].set_ylabel('$q$ = 23 m d$^{-1}$ \n\n Normalized temperature [-]', labelpad=10)
axs[1,0].set_xlabel("Time [s]", labelpad=10)
axs[1,0].set_xlim(0,2500)


axs[1,1].scatter(list_BTC_time[3], list_BTC_Tf_LTNE[3], color ='#1E90FF',label= "Tf - Experimental data",s=3)
axs[1,1].scatter(list_BTC_time[3], list_BTC_Ts_LTNE[3], color ='lightgreen',label= "Ts - Experimental data",s=3)
axs[1,1].plot(list_time_moose[3], list_Tf_moose[3],color = color_model[2],label= "Tf - Model (Max. $h_{sf}$)",linewidth=linewidth)
axs[1,1].plot(list_time_moose[3], list_Ts_moose[3],color =  color_model[2],linestyle='-', marker='o', markevery=80,markersize=markersize_o,label= "Ts - Model (Max. $h_{sf}$)",linewidth=linewidth_s)
axs[1,1].plot(list_time_moose_Gossler[3], list_Tf_moose_Gossler[3], color = color_model[0],linestyle = 'dashed',label= "Tf - Model (Empirical $h_{sf}$)",linewidth=linewidth)
axs[1,1].plot(list_time_moose_Gossler[3], list_Ts_moose_Gossler[3], color = color_model[0], linestyle=(0, (1, 1)), label= "Ts - Model (Empirical $h_{sf}$)",linewidth=linewidth_s)
axs[1,1].set_xlabel("Time [s]", labelpad=10)
axs[1,1].set_xlim(0,2500)
axs[1,1].set_yticklabels([])


lines = []
labels = []

for ax in fig.axes:
    Line, Label = ax.get_legend_handles_labels()
    lines.extend(Line)
    labels.extend(Label)

labels_1 = [labels[i] for i in range(3)]
labels_2 = [labels[k] for k in (3,4,5)]
labels= labels_1 + labels_2

# Create a single legend for the entire figure, placed at the top
fig.legend(lines, labels, loc='upper left', bbox_to_anchor=(0.11, 1.08), ncol=3, frameon=False,fontsize="7",markerscale=1)

plt.subplots_adjust(wspace=0.1,hspace=0.2)
# plt.savefig("fig03_BTC.png", bbox_inches='tight')
plt.show()