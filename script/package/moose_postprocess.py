import pandas as pd
import numpy as np


class MOOSE_Postprocess:

    def __init__(self,moose_output):
        self.moose_output = moose_output


    def time(self):

        time = np.array(self.moose_output['time'])
        return time
    
    def Tf_LTE_column(self, grain_size):

        self.grain_size = grain_size

        if grain_size == "05mm":
            Tf_point = "Tf_1"
        elif grain_size == "10mm":
            Tf_point = "Tf_2"
        elif grain_size == "15mm":
            Tf_point = "Tf_3"
        elif grain_size == "20mm":
            Tf_point = "Tf_4"
        elif grain_size == "25mm":
            Tf_point = "Tf_5"
        elif grain_size == "30mm":
            Tf_point = "Tf_6"

        Tf = np.array(self.moose_output[Tf_point])
        return Tf
    
    def Tf_LTE(self):

        Tf_point = "Tf_1"

        Tf = np.array(self.moose_output[Tf_point])
        return Tf
    
    def Tf_1_LTNE(self):

        Tf_1 = np.array(self.moose_output["Tf_1"])
        return Tf_1
    
    def Tf_2_LTNE(self):

        Tf_2 = np.array(self.moose_output["Tf_2"])
        return Tf_2
    
    def Ts_LTNE(self):

        Ts = np.array(self.moose_output["Ts"])
        return Ts
    
    def v_1_LTNE(self):

        v_1_array = np.array(self.moose_output["v_1"])

        v_1 = round(v_1_array[1],7)

        return v_1
    
    def v_2_LTNE(self):

        v_2_array = np.array(self.moose_output["v_2"])

        v_2 = round(v_2_array[1],7)

        return v_2
    
    def hsf_LTNE(self):

        hsf_moose = np.array(self.moose_output["hsf_Gossler"])
        return hsf_moose