from sklearn.metrics import mean_poisson_deviance
import torch
import pandas as pd
import numpy as np
import time
import os

'''
Basic 2D spin Mutation operators for genetic tunneling
By Qichen Xu
'''
def mu_type6(winner_list,atom_number,atom_x_size,atom_y_size):
    select_index = np.random.choice(list(range(len(winner_list))), 4)
    mom_data_1=winner_list[select_index[0]].transpose()[-atom_number:,:]
    mom_data_2=winner_list[select_index[1]].transpose()[-atom_number:,:]
    mom_data_3=winner_list[select_index[2]].transpose()[-atom_number:,:]
    mom_data_4=winner_list[select_index[3]].transpose()[-atom_number:,:]
    index_crossover_1= np.sort(np.random.randint(0,len(mom_data_4)-int(int(atom_x_size*atom_x_size)/5)-1,4))[0]

    rs = torch.rand(1)
    if rs<=0.2:
        part_1 = np.concatenate((mom_data_1[index_crossover_1:index_crossover_1+int(int(atom_x_size*atom_x_size)/5),:] ,mom_data_1[index_crossover_1:index_crossover_1+int(int(atom_x_size*atom_x_size)/5),:]))
        part_2 = np.concatenate((mom_data_1[index_crossover_1:index_crossover_1+int(int(atom_x_size*atom_x_size)/5),:] ,mom_data_1[index_crossover_1:index_crossover_1+int(int(atom_x_size*atom_x_size)/5),:]))
        part_3 = mom_data_1[index_crossover_1:index_crossover_1+int(int(atom_x_size*atom_x_size)/5),:]
    elif 0.2<rs<=0.5:
        mom_data_1 = mom_data_2
        part_1 = np.concatenate((mom_data_1[index_crossover_1:index_crossover_1+int(int(atom_x_size*atom_x_size)/5),:] ,mom_data_1[index_crossover_1:index_crossover_1+int(int(atom_x_size*atom_x_size)/5),:]))
        part_2 = np.concatenate((mom_data_1[index_crossover_1:index_crossover_1+int(int(atom_x_size*atom_x_size)/5),:] ,mom_data_1[index_crossover_1:index_crossover_1+int(int(atom_x_size*atom_x_size)/5),:]))
        part_3 = mom_data_1[index_crossover_1:index_crossover_1+int(int(atom_x_size*atom_x_size)/5),:]
    elif 0.5<rs<=0.8:
        mom_data_1 = mom_data_3
        part_1 = np.concatenate((mom_data_1[index_crossover_1:index_crossover_1+int(int(atom_x_size*atom_x_size)/5),:] ,mom_data_1[index_crossover_1:index_crossover_1+int(int(atom_x_size*atom_x_size)/5),:]))
        part_2 = np.concatenate((mom_data_1[index_crossover_1:index_crossover_1+int(int(atom_x_size*atom_x_size)/5),:] ,mom_data_1[index_crossover_1:index_crossover_1+int(int(atom_x_size*atom_x_size)/5),:]))
        part_3 = mom_data_1[index_crossover_1:index_crossover_1+int(int(atom_x_size*atom_x_size)/5),:]
    elif 0.8<rs:
        mom_data_1 = mom_data_4
        part_1 = np.concatenate((mom_data_1[index_crossover_1:index_crossover_1+int(int(atom_x_size*atom_x_size)/5),:] ,mom_data_1[index_crossover_1:index_crossover_1+int(int(atom_x_size*atom_x_size)/5),:]))
        part_2 = np.concatenate((mom_data_1[index_crossover_1:index_crossover_1+int(int(atom_x_size*atom_x_size)/5),:] ,mom_data_1[index_crossover_1:index_crossover_1+int(int(atom_x_size*atom_x_size)/5),:]))
        part_3 = mom_data_1[index_crossover_1:index_crossover_1+int(int(atom_x_size*atom_x_size)/5),:]
        
    mom_data= np.concatenate((part_1,part_2,part_3))
    mutation_zone = int(torch.rand(1)*600)# important  here you need to change one number of perturbation to get good result. and suitable for your case this number just for 10000 atoms.
    for i in range(10):
        index_mutation = np.random.randint(0,len(mom_data),1)
        a= index_mutation
        b = index_mutation+mutation_zone
        np.random.shuffle(mom_data[int(a):int(b)])
    return mom_data
