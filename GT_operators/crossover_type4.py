from sklearn.metrics import mean_poisson_deviance
import torch
import pandas as pd
import numpy as np
import time
import os

'''
Basic 2D spin crossover operators for genetic tunneling
By Qichen Xu
'''
def co_type4(winner_list,atom_number,atom_x_size,atom_y_size):
    select_index = np.random.choice(list(range(len(winner_list))), 4)
    mom_data_1=winner_list[select_index[0]].transpose()[-atom_number:,:]
    mom_data_2=winner_list[select_index[1]].transpose()[-atom_number:,:]
    mom_data_3=winner_list[select_index[2]].transpose()[-atom_number:,:]
    mom_data_4=winner_list[select_index[3]].transpose()[-atom_number:,:]
    index_crossover_4 = np.sort(np.random.randint(0,len(mom_data_4),3))
    rs = torch.rand(1)
    if rs<=0.2:
        part_1 = np.concatenate((mom_data_1[0:index_crossover_4[0],:] ,mom_data_2[index_crossover_4[0]:index_crossover_4[1],:]))
        part_2 = np.concatenate((mom_data_3[index_crossover_4[1]:index_crossover_4[2],:] ,mom_data_4[index_crossover_4[2]:,:]))
    elif 0.2<rs<=0.5:
        part_1 = np.concatenate((mom_data_2[0:index_crossover_4[0],:] ,mom_data_1[index_crossover_4[0]:index_crossover_4[1],:]))
        part_2 = np.concatenate((mom_data_4[index_crossover_4[1]:index_crossover_4[2],:] ,mom_data_3[index_crossover_4[2]:,:]))
    elif 0.5<rs<=0.8:
        part_1 = np.concatenate((mom_data_1[0:index_crossover_4[0],:] ,mom_data_2[index_crossover_4[0]:index_crossover_4[1],:]))
        part_2 = np.concatenate((mom_data_4[index_crossover_4[1]:index_crossover_4[2],:] ,mom_data_3[index_crossover_4[2]:,:]))
    elif 0.8<rs:
        part_1 = np.concatenate((mom_data_1[0:index_crossover_4[0],:] ,mom_data_3[index_crossover_4[0]:index_crossover_4[1],:]))
        part_2 = np.concatenate((mom_data_2[index_crossover_4[1]:index_crossover_4[2],:] ,mom_data_4[index_crossover_4[2]:,:]))
        
    mom_data= np.concatenate((part_1,part_2))
    return mom_data
