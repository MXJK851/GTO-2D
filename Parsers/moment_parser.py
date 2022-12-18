import torch
import pandas as pd
import numpy as np
#build the graph
import time
import os

def moment_file_parser(mom_out_file):
    """
    :param mom_out_file moment file
    :type mom_out_file opened output file
    :return: np.array
    """        
   
    mom_output = pd.read_csv(mom_out_file, sep='\s+', header=None, skiprows=7)
    mon_all = mom_output[3]
    mom_x = mom_output[4]
    mom_y = mom_output[5]
    mom_z = mom_output[6]
    mon_all = np.array(mon_all)
    mom_states_x = np.array(mom_x)
    mom_states_y = np.array(mom_y)
    mom_states_z = np.array(mom_z)
    return mom_output,np.array([mon_all,mom_states_x, mom_states_y, mom_states_z])
