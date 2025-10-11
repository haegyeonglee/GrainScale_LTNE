import numpy as np
import pandas as pd

class BC_depth:
  
    def __init__(self,exp,grain_size,dir_exp,dir_model_BC):
        self.exp = exp
        self.grain_size = grain_size
        self.dir_exp = dir_exp
        self.dir_model_BC = dir_model_BC
        
        

    def __str__(self):

        model_grain_05mm = "05mm"

        if self.grain_size == "10mm":
            model_grain = "05mm"
        if self.grain_size == "15mm":
            model_grain = "10mm"
        if self.grain_size == "20mm":
            model_grain = "15mm"
        if self.grain_size == "25mm":
            model_grain = "20mm"
        if self.grain_size == "30mm":
            model_grain = "25mm"

        bc_grain_size = model_grain if self.grain_size != "05mm" else model_grain_05mm

        if self.grain_size == "05mm":
            bc_file  = 'Exp'+str(self.exp)+ '_BC_input_temp_K.csv'
        else:
            bc_file  = "Exp" + str(self.exp) + '_' + bc_grain_size +'_BC_input_temp.csv'

        return "BC Data: " + bc_file

    
    def BC_df_inlet(self):

        dir_exp = self.dir_exp + "/"

        file_T_BC = 'Exp'+str(self.exp)+ '_BC_input_temp_K.csv'

        BTC_T_Exp = pd.read_csv(f"{dir_exp}{file_T_BC}")


        T_data = BTC_T_Exp.iloc[:,1]


        ######################################################################################################################

        dir_model_BC = self.dir_model_BC+ "/"
        model_bc_temp =  'Exp'+str(self.exp)+'_05mm_BC_input_temp.csv'
        read_MOOSE_bc = pd.read_csv(f"{dir_model_BC}{model_bc_temp}")
        read_bc_T = read_MOOSE_bc.iloc[:,1]

        T_0 = round(read_bc_T[0],2)
        T_1 = round(read_bc_T.max(),2)


        ######################################################################################################################

        T_BC_data_crop = (T_data[1:len(T_data)]-T_0)/(T_1 - T_0)

        t = np.linspace(1, len(T_BC_data_crop), len(T_BC_data_crop))

        data = pd.DataFrame({'time': t, 'T': T_BC_data_crop})

        return data
    
    
    def BC_df_depth(self):

        if self.grain_size == "10mm":
            model_grain = "05mm"
        if self.grain_size == "15mm":
            model_grain = "10mm"
        if self.grain_size == "20mm":
            model_grain = "15mm"
        if self.grain_size == "25mm":
            model_grain = "20mm"
        if self.grain_size == "30mm":
            model_grain = "25mm"

        dir_exp = self.dir_exp + "/"

        file_exp_BTC = "Exp"+ str(self.exp) + "_data_normalized.csv"

        BTC_T_Exp = pd.read_csv(f"{dir_exp}{file_exp_BTC}")    

        sensor_unit = ['T_05mm_diff_2_1','T_05mm_diff_2_2', 'T_05mm_diff_3_1', 'T_05mm_diff_4_1', 'T_05mm_diff_4_2', 'T_10mm_diff_1_1', 'T_10mm_diff_1_2', 'T_10mm_diff_2_1', 'T_10mm_diff_2_2', 'T_10mm_diff_3_1', 'T_10mm_diff_3_2', 'T_10mm_diff_4_1', 'T_10mm_diff_4_2', 'T_15mm_diff_1_1', 'T_15mm_diff_1_2', 'T_15mm_diff_2_1', 'T_15mm_diff_2_2', 'T_15mm_diff_3_1', 'T_15mm_diff_3_2', 'T_15mm_diff_4_1', 'T_15mm_diff_4_2', 'T_20mm_diff_1_1', 'T_20mm_diff_1_2', 'T_20mm_diff_2_1', 'T_20mm_diff_2_2', 'T_20mm_diff_3_1', 'T_20mm_diff_3_2', 'Tf_20mm_diff_4', 'T_25mm_diff_1_1', 'T_25mm_diff_1_2', 'T_25mm_diff_2_1', 'T_25mm_diff_2_2', 'T_25mm_diff_3_1', 'T_25mm_diff_3_2', 'Tf_25mm_diff_4', 'T_30mm_diff_1_1', 'T_30mm_diff_1_2', 'T_30mm_diff_2_1', 'T_30mm_diff_2_2', 'T_30mm_diff_3_1', 'T_30mm_diff_3_2', 'T_30mm_diff_4_1', 'T_30mm_diff_4_2']
        sensor_Tf = ['JQ552_36_CH3', 'JQ552_36_CH4', 'JO332_20_CH3', 'JO332_54_CH3', 'JO332_54_CH4', 'CX032_97_CH3', 'CX032_97_CH4', 'AR887_89_CH3', 'AR887_89_CH4', 'JY892_39_CH1', 'JY892_39_CH2', 'JY892_39_CH3', 'JY892_39_CH4','JY892_35_CH1','JY892_35_CH2','JY892_35_CH3','JY892_35_CH4','JY892_38_CH1','JY892_38_CH2','JY892_38_CH3','JY892_38_CH4', 'CX032_94_CH1', 'CX032_94_CH2', 'CX032_94_CH3', 'CX032_94_CH4', 'JY892_33_CH1', 'JY892_33_CH2', 'JY892_33_CH4', 'JY892_86_CH1', 'JY892_86_CH2', 'JY892_86_CH3', 'JY892_86_CH4', 'JY892_111_CH1', 'JY892_111_CH2', 'JY892_111_CH4', 'JY892_51_CH1', 'JY892_51_CH2', 'JY892_51_CH3', 'JY892_51_CH4', 'JY892_53_CH1', 'JY892_53_CH2', 'JY892_53_CH3', 'JY892_53_CH4']

        peak_in_unit = [sensor_unit.index(item) for item in sensor_unit if model_grain in item]

        count_sensor = peak_in_unit

        BTC_time = BTC_T_Exp.loc[0:len(BTC_T_Exp),"Time"] #551 for Exp4
        BTC_Tf = pd.DataFrame({'time': BTC_time})


        for count in count_sensor:
            BTC_Tf[count] = BTC_T_Exp.loc[0:len(BTC_T_Exp),sensor_Tf[count]] #550 for Exp4

        if model_grain == "05mm":

            plt_Exp_f2_1_05mm = np.array(BTC_Tf.iloc[:,1])

            plt_Exp_f2_2_05mm = np.array(BTC_Tf.iloc[:,2])

            plt_Exp_f3_1_05mm = np.array(BTC_Tf.iloc[:,3])

            plt_Exp_f4_1_05mm = np.array(BTC_Tf.iloc[:,4])

            plt_Exp_f4_2_05mm = np.array(BTC_Tf.iloc[:,5])

            Exp_05mm_Tf_ave = np.mean( np.array([plt_Exp_f2_1_05mm, plt_Exp_f2_2_05mm,plt_Exp_f3_1_05mm,plt_Exp_f4_1_05mm,plt_Exp_f4_2_05mm]), axis=0 )


        elif model_grain == "10mm":

            plt_Exp_f1_1_10mm = np.array(BTC_Tf.iloc[:,1])

            plt_Exp_f1_2_10mm = np.array(BTC_Tf.iloc[:,2])

            plt_Exp_f2_1_10mm = np.array(BTC_Tf.iloc[:,3])

            plt_Exp_f2_2_10mm = np.array(BTC_Tf.iloc[:,4])

            plt_Exp_f3_1_10mm = np.array(BTC_Tf.iloc[:,5])

            plt_Exp_f3_2_10mm = np.array(BTC_Tf.iloc[:,6])

            plt_Exp_f4_1_10mm = np.array(BTC_Tf.iloc[:,7])

            plt_Exp_f4_2_10mm = np.array(BTC_Tf.iloc[:,8])

            Exp_10mm_Tf_ave = np.mean( np.array([plt_Exp_f1_1_10mm,plt_Exp_f1_2_10mm,plt_Exp_f2_1_10mm,plt_Exp_f2_2_10mm,plt_Exp_f3_1_10mm,plt_Exp_f3_2_10mm,plt_Exp_f4_1_10mm,plt_Exp_f4_2_10mm]), axis=0 )



        elif model_grain == "15mm":

            plt_Exp_f1_1_15mm = np.array(BTC_Tf.iloc[:,1])

            plt_Exp_f1_2_15mm = np.array(BTC_Tf.iloc[:,2])

            plt_Exp_f2_1_15mm = np.array(BTC_Tf.iloc[:,3])

            plt_Exp_f2_2_15mm = np.array(BTC_Tf.iloc[:,4])

            plt_Exp_f3_1_15mm = np.array(BTC_Tf.iloc[:,5])

            plt_Exp_f3_2_15mm = np.array(BTC_Tf.iloc[:,6])

            plt_Exp_f4_1_15mm = np.array(BTC_Tf.iloc[:,7])

            plt_Exp_f4_2_15mm = np.array(BTC_Tf.iloc[:,8])

            Exp_15mm_Tf_ave = np.mean( np.array([plt_Exp_f1_1_15mm,plt_Exp_f1_2_15mm,plt_Exp_f2_1_15mm,plt_Exp_f2_2_15mm,plt_Exp_f3_1_15mm,plt_Exp_f3_2_15mm,plt_Exp_f4_1_15mm,plt_Exp_f4_2_15mm]), axis=0 )



        elif model_grain == "20mm":

            plt_Exp_f1_1_20mm = np.array(BTC_Tf.iloc[:,1])

            plt_Exp_f1_2_20mm = np.array(BTC_Tf.iloc[:,2])

            plt_Exp_f2_1_20mm = np.array(BTC_Tf.iloc[:,3])

            plt_Exp_f2_2_20mm = np.array(BTC_Tf.iloc[:,4])

            plt_Exp_f3_1_20mm = np.array(BTC_Tf.iloc[:,5])

            plt_Exp_f3_2_20mm = np.array(BTC_Tf.iloc[:,6])

            Exp_20mm_Tf_ave = np.mean( np.array([plt_Exp_f1_1_20mm,plt_Exp_f1_2_20mm,plt_Exp_f2_1_20mm,plt_Exp_f2_2_20mm,plt_Exp_f3_1_20mm,plt_Exp_f3_2_20mm]), axis=0 )



        elif model_grain == "25mm":

            plt_Exp_f1_1_25mm = np.array(BTC_Tf.iloc[:,1])

            plt_Exp_f1_2_25mm = np.array(BTC_Tf.iloc[:,2])

            plt_Exp_f2_1_25mm = np.array(BTC_Tf.iloc[:,3])

            plt_Exp_f2_2_25mm = np.array(BTC_Tf.iloc[:,4])

            plt_Exp_f3_1_25mm = np.array(BTC_Tf.iloc[:,5])

            plt_Exp_f3_2_25mm = np.array(BTC_Tf.iloc[:,6])

            Exp_25mm_Tf_ave = np.mean( np.array([plt_Exp_f1_1_25mm,plt_Exp_f1_2_25mm,plt_Exp_f2_1_25mm,plt_Exp_f2_2_25mm,plt_Exp_f3_1_25mm,plt_Exp_f3_2_25mm]), axis=0 )


        if model_grain == "05mm":
            T_data = Exp_05mm_Tf_ave
        if model_grain == "10mm":
            T_data = Exp_10mm_Tf_ave
        if model_grain == "15mm":
            T_data = Exp_15mm_Tf_ave
        if model_grain == "20mm":
            T_data = Exp_20mm_Tf_ave
        if model_grain == "25mm":
            T_data = Exp_25mm_Tf_ave

        ######################################################################################################################

        dir_model_BC = self.dir_model_BC
        model_bc_temp =  'Exp'+str(self.exp)+'_05mm_BC_input_temp.csv'
        read_MOOSE_bc = pd.read_csv(f"{dir_model_BC}{model_bc_temp}")
        read_bc_T = read_MOOSE_bc.iloc[:,1]

        T_0 = round(read_bc_T[0],2)
        T_1 = round(read_bc_T.max(),2)

        ######################################################################################################################

        T_BC_data_crop = T_data[1:len(T_data)]

        t = np.linspace(1, len(T_BC_data_crop), len(T_BC_data_crop))

        data = pd.DataFrame({'time': t, 'T': T_BC_data_crop})

        return data