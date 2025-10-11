import pandas as pd
import numpy as np


class MOOSE_Data:

    def __init__(self):
        pass

    def read_IC(self, filename_moose):

        self.filename_moose = filename_moose

        data = []
    
        with open(filename_moose, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if line.startswith("#") or len(line) == 0:
                    continue
                data.append(line)
                if line.startswith("T_in"):
                    break
        return data
    
    def read_IC_knownT(self, filename_bc):

        self.filename_bc = filename_bc

        bc_data = pd.read_csv(filename_bc)

        return bc_data


    def read_output(self, filename_moose):

        df_moose = pd.read_csv(filename_moose)
        df_moose = df_moose.iloc[1:]

        return df_moose
    
