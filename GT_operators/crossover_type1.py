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
def co_type1(winner_list,atom_number,atom_x_size,atom_y_size):
    select_index = np.random.choice(list(range(len(winner_list))), 4)
    mom_data_1=winner_list[select_index[0]].transpose()[-atom_number:,:]
    mom_data_2=winner_list[select_index[1]].transpose()[-atom_number:,:]
    mom_data_3=winner_list[select_index[2]].transpose()[-atom_number:,:]
    mom_data_4=winner_list[select_index[3]].transpose()[-atom_number:,:]
    
    square_1 = np.reshape(mom_data_1,(int(atom_x_size),int(int(atom_y_size)),4))
    square_2 = np.reshape(mom_data_2,(int(atom_x_size),int(int(atom_y_size)),4))
    square_3 = np.reshape(mom_data_3,(int(atom_x_size),int(int(atom_y_size)),4))
    square_4 = np.reshape(mom_data_4,(int(atom_x_size),int(int(atom_y_size)),4))

    index_crossover_1,index_crossover_2,index_crossover_3= np.sort(np.random.randint(0,int(atom_x_size),3))
    rs = torch.rand(1)
    if rs<=0.2:
        part_1 = np.concatenate((square_1[:,:index_crossover_1] ,square_2[:,index_crossover_1:index_crossover_2] ),1)
        part_2 = np.concatenate((square_3[:,index_crossover_2:index_crossover_3]  ,square_4[:,index_crossover_3:]),1)
    elif 0.2<rs<=0.5:
        part_1 = np.concatenate((square_2[:,:index_crossover_1] ,square_1[:,index_crossover_1:index_crossover_2] ),1)
        part_2 = np.concatenate((square_3[:,index_crossover_2:index_crossover_3]  ,square_4[:,index_crossover_3:]),1)
    elif 0.5<rs<=0.8:
        part_1 = np.concatenate((square_1[:,:index_crossover_1] ,square_2[:,index_crossover_1:index_crossover_2] ),1)
        part_2 = np.concatenate((square_4[:,index_crossover_2:index_crossover_3]  ,square_3[:,index_crossover_3:]),1)
    elif 0.8<rs:
        part_1 = np.concatenate((square_1[:,:index_crossover_1] ,square_3[:,index_crossover_1:index_crossover_2] ),1)
        part_2 = np.concatenate((square_2[:,index_crossover_2:index_crossover_3]  ,square_4[:,index_crossover_3:]),1)
    
    mom_data= np.reshape(np.concatenate((part_1,part_2),1),(int(int(atom_x_size)*int(int(atom_y_size))),4))
    return mom_data
