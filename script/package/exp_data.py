import pandas as pd
import numpy as np


class Exp_Data:

    sensor_unit = ['T_05mm_diff_2_1','T_05mm_diff_2_2', 'T_05mm_diff_3_1', 'T_05mm_diff_4_1', 'T_05mm_diff_4_2', 'T_10mm_diff_1_1', 'T_10mm_diff_1_2', 'T_10mm_diff_2_1', 'T_10mm_diff_2_2', 'T_10mm_diff_3_1', 'T_10mm_diff_3_2', 'T_10mm_diff_4_1', 'T_10mm_diff_4_2', 'T_15mm_diff_1_1', 'T_15mm_diff_1_2', 'T_15mm_diff_2_1', 'T_15mm_diff_2_2', 'T_15mm_diff_3_1', 'T_15mm_diff_3_2', 'T_15mm_diff_4_1', 'T_15mm_diff_4_2', 'T_20mm_diff_1_1', 'T_20mm_diff_1_2', 'T_20mm_diff_2_1', 'T_20mm_diff_2_2', 'T_20mm_diff_3_1', 'T_20mm_diff_3_2', 'Tf_20mm_diff_4', 'T_25mm_diff_1_1', 'T_25mm_diff_1_2', 'T_25mm_diff_2_1', 'T_25mm_diff_2_2', 'T_25mm_diff_3_1', 'T_25mm_diff_3_2', 'Tf_25mm_diff_4', 'T_30mm_diff_1_1', 'T_30mm_diff_1_2', 'T_30mm_diff_2_1', 'T_30mm_diff_2_2', 'T_30mm_diff_3_1', 'T_30mm_diff_3_2', 'T_30mm_diff_4_1', 'T_30mm_diff_4_2']
    sensor_Ts = ['AR887_89_CH2', 'AR887_89_CH2', 'JO332_20_CH2', 'JO332_54_CH2', 'JO332_54_CH2', 'CX032_97_CH1', 'CX032_97_CH1', 'AR887_89_CH1', 'AR887_89_CH1', 'JO332_20_CH1', 'JO332_20_CH1', 'JO332_54_CH1', 'JO332_54_CH1','CX032_96_CH4','CX032_96_CH4','JQ552_38_CH4','JQ552_38_CH4','JQ552_71_CH4','JQ552_71_CH4','JY892_27_CH4','JY892_27_CH4', 'CX032_96_CH3', 'CX032_96_CH3', 'JQ552_38_CH3', 'JQ552_38_CH3', 'JQ552_71_CH3', 'JQ552_71_CH3', 'JY892_33_CH3', 'CX032_96_CH2', 'CX032_96_CH2', 'JQ552_38_CH2', 'JQ552_38_CH2', 'JQ552_71_CH2', 'JQ552_71_CH2', 'JY892_111_CH3', 'CX032_96_CH1', 'CX032_96_CH1', 'JQ552_38_CH1', 'JQ552_38_CH1', 'JQ552_71_CH1', 'JQ552_71_CH1', 'JY892_27_CH1', 'JY892_27_CH1']
    sensor_Tf = ['JQ552_36_CH3', 'JQ552_36_CH4', 'JO332_20_CH3', 'JO332_54_CH3', 'JO332_54_CH4', 'CX032_97_CH3', 'CX032_97_CH4', 'AR887_89_CH3', 'AR887_89_CH4', 'JY892_39_CH1', 'JY892_39_CH2', 'JY892_39_CH3', 'JY892_39_CH4','JY892_35_CH1','JY892_35_CH2','JY892_35_CH3','JY892_35_CH4','JY892_38_CH1','JY892_38_CH2','JY892_38_CH3','JY892_38_CH4', 'CX032_94_CH1', 'CX032_94_CH2', 'CX032_94_CH3', 'CX032_94_CH4', 'JY892_33_CH1', 'JY892_33_CH2', 'JY892_33_CH4', 'JY892_86_CH1', 'JY892_86_CH2', 'JY892_86_CH3', 'JY892_86_CH4', 'JY892_111_CH1', 'JY892_111_CH2', 'JY892_111_CH4', 'JY892_51_CH1', 'JY892_51_CH2', 'JY892_51_CH3', 'JY892_51_CH4', 'JY892_53_CH1', 'JY892_53_CH2', 'JY892_53_CH3', 'JY892_53_CH4']


    def __init__(self, dir_data, grain_size, exp):
        self.dir_data = dir_data
        self.grain_size = grain_size
        self.exp = exp

    def __str__(self):
        return "Data file: Exp"+ str(self.exp) + "_data_normalized.csv" + " for grain size of " + self.grain_size


    def read_exp_data(self):
        dir_exp = self.dir_data + "/"
        filename_exp = "Exp"+ str(self.exp) + "_data_normalized.csv"

        BTC_T_Exp = pd.read_csv(f"{dir_exp}{filename_exp}")

        return BTC_T_Exp

    def read_exp_data_time(self):
        dir_exp = self.dir_data + "/"
        filename_exp = "Exp"+ str(self.exp) + "_data_normalized.csv"

        BTC_T_Exp = pd.read_csv(f"{dir_exp}{filename_exp}")
        BTC_time = BTC_T_Exp.loc[1:len(BTC_T_Exp),'Time'] #551 for Exp4

        return BTC_time
    
    def read_exp_data_Tf(self):
        dir_exp = self.dir_data + "/"
        filename_exp = "Exp"+ str(self.exp) + "_data_normalized.csv"

        BTC_T_Exp = pd.read_csv(f"{dir_exp}{filename_exp}")
        BTC_time = BTC_T_Exp.loc[1:len(BTC_T_Exp),'Time'] #551 for Exp4
        BTC_Tf = pd.DataFrame({'time': BTC_time})

        BTC_time = np.array(BTC_time)
        header = []

        count_sensor = [self.sensor_unit.index(item) for item in self.sensor_unit if self.grain_size in item]

        for i in count_sensor:
            BTC_Tf[i] = BTC_T_Exp.loc[0:len(BTC_T_Exp),self.sensor_Tf[i]] #550 for Exp4
            header.append(self.sensor_Tf[i])

        BTC_Tf = BTC_Tf.iloc[:,1:]

        BTC_Tf.columns = header

        return BTC_Tf
    
    def read_exp_data_Ts(self):
        dir_exp = self.dir_data + "/"
        filename_exp = "Exp"+ str(self.exp) + "_data_normalized.csv"

        BTC_T_Exp = pd.read_csv(f"{dir_exp}{filename_exp}")
        BTC_time = BTC_T_Exp.loc[1:len(BTC_T_Exp),'Time'] #551 for Exp4
        BTC_Ts = pd.DataFrame({'time': BTC_time})

        BTC_time = np.array(BTC_time)
        header = []

        count_sensor = [self.sensor_unit.index(item) for item in self.sensor_unit if self.grain_size in item]

        for i in count_sensor:
            BTC_Ts[i] = BTC_T_Exp.loc[0:len(BTC_T_Exp),self.sensor_Ts[i]] #550 for Exp4
            header.append(self.sensor_Ts[i])

        BTC_Ts = BTC_Ts.iloc[:,1:]

        BTC_Ts.columns = header

        return BTC_Ts
    