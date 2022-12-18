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
def mu_type3(winner_list,atom_number,atom_x_size,atom_y_size):
    select_index = np.random.choice(list(range(len(winner_list))), 4)
    mom_data_1=winner_list[select_index[0]].transpose()[-atom_number:,:]
    mom_data_2=winner_list[select_index[0]].transpose()[-atom_number:,:]
    mom_data_3=winner_list[select_index[0]].transpose()[-atom_number:,:]
    mom_data_4=winner_list[select_index[0]].transpose()[-atom_number:,:]
    
    square_1 = np.reshape(mom_data_1,(int(atom_x_size),int(int(atom_y_size)),4))
    square_2 = np.reshape(mom_data_2,(int(atom_x_size),int(int(atom_y_size)),4))
    square_3 = np.reshape(mom_data_3,(int(atom_x_size),int(int(atom_y_size)),4))
    square_4 = np.reshape(mom_data_4,(int(atom_x_size),int(int(atom_y_size)),4))
    
    
    index_crossover_1= np.sort(np.random.randint(0,int(int(atom_x_size)-int(int(atom_x_size)/4)-1),1))[0]
    index_crossover_2= np.sort(np.random.randint(0,int(int(atom_x_size)-int(int(atom_x_size)/5)-1),1))[0]
    index_crossover_3= np.sort(np.random.randint(0,int(int(atom_x_size)-int(int(atom_x_size)/10)-1),1))[0]
    rs = torch.rand(1)
    if rs<=0.3:
        part_1 = np.concatenate((square_1[:,index_crossover_1:index_crossover_1+int(int(atom_x_size)/4)] ,square_2[:,index_crossover_1:index_crossover_1+int(int(atom_x_size)/4)] ),1)
        part_2 = np.concatenate((square_3[:,index_crossover_1:index_crossover_1+int(int(atom_x_size)/4)]  ,square_4[:,index_crossover_1:index_crossover_1+int(int(atom_x_size)/4)]),1)
    elif 0.3<rs<=0.6:
        part_1 = np.concatenate((square_1[:,index_crossover_2:index_crossover_2+int(int(atom_x_size)/5)] ,square_2[:,index_crossover_2:index_crossover_2+int(int(atom_x_size)/5)],square_2[:,index_crossover_2:index_crossover_2+int(int(atom_x_size)/5)]),1)
        part_2 = np.concatenate((square_3[:,index_crossover_2:index_crossover_2+int(int(atom_x_size)/5)]  ,square_4[:,index_crossover_2:index_crossover_2+int(int(atom_x_size)/5)]),1)
    else:
        part_1 = np.concatenate((square_1[:,index_crossover_3:index_crossover_3+int(int(atom_x_size)/10)],
                                    square_1[:,index_crossover_3:index_crossover_3+int(int(atom_x_size)/10)],
                                    square_1[:,index_crossover_3:index_crossover_3+int(int(atom_x_size)/10)],
                                    square_1[:,index_crossover_3:index_crossover_3+int(int(atom_x_size)/10)],
                                    square_1[:,index_crossover_3:index_crossover_3+int(int(atom_x_size)/10)]),1)
        part_2 = part_1
    
    mom_data= np.reshape(np.concatenate((part_1,part_2),1),(int(int(atom_x_size)*int(atom_y_size)),4))
    mutation_zone = int(torch.rand(1)*600)# important  here you need to change one number of perturbation to get good result. and suitable for your case this number just for 10000 atoms.
    for i in range(10):
        index_mutation = np.random.randint(0,len(mom_data),1)
        a= index_mutation
        b = index_mutation+mutation_zone
        np.random.shuffle(mom_data[int(a):int(b)])
    return mom_data
