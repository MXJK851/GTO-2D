import imp
from sklearn.metrics import mean_poisson_deviance
import pandas as pd
import numpy as np
import time
import os
#import basic operators
from GT_operators.crossover_type1 import co_type1
from GT_operators.crossover_type2 import co_type2
from GT_operators.crossover_type3 import co_type3
from GT_operators.crossover_type4 import co_type4
from GT_operators.mutation_type1 import mu_type1
from GT_operators.mutation_type2 import mu_type2
from GT_operators.mutation_type3 import mu_type3
from GT_operators.mutation_type4 import mu_type4
from GT_operators.mutation_type5 import mu_type5
from GT_operators.mutation_type6 import mu_type6

'''
Basic 2D spin crossover and mutation operators 

for genetic tunneling
By Qichen Xu
'''
def corssover(type,winner_list,atom_number,atom_x_size,atom_y_size):
    match type:
        case 1:
            return co_type1(winner_list,atom_number,atom_x_size,atom_y_size)
        case 2:
            return co_type2(winner_list,atom_number,atom_x_size,atom_y_size)
        case 3:
            return co_type3(winner_list,atom_number,atom_x_size,atom_y_size)
        case 4:
            return co_type4(winner_list,atom_number,atom_x_size,atom_y_size)

def mutation(type,winner_list,atom_number,atom_x_size,atom_y_size):
    match type:
        case 1:
            return mu_type1(winner_list,atom_number,atom_x_size,atom_y_size)
        case 2:
            return mu_type2(winner_list,atom_number,atom_x_size,atom_y_size)
        case 3:
            return mu_type3(winner_list,atom_number,atom_x_size,atom_y_size)
        case 4:
            return mu_type4(winner_list,atom_number,atom_x_size,atom_y_size)
        case 5:
            return mu_type5(winner_list,atom_number,atom_x_size,atom_y_size)
        case 6:
            return mu_type6(winner_list,atom_number,atom_x_size,atom_y_size)
       

def crossover_mutation(parent_gen_eval_result,multi_factor,atom_x_size,atom_y_size,atom_number):
#important!!!  Now only support atom_x_size should equal to int(atom_y_size). atom_x_size%20 == 0
#Very welcome to extend this code from square case to another shape.
        caled_factor =multi_factor

        winner_list = []#this one is the spin configuration passed from the selection module
        for i in range(len(parent_gen_eval_result)):
            winner_list.append(parent_gen_eval_result[i][1][1])
        
        if np.random.rand(1)[0]<caled_factor:
            #here we applied crossover
            type = np.random.choice([1,2,3,4])
            return corssover(type,winner_list,atom_number,atom_x_size,atom_y_size)
        else:
            type = np.random.choice([1,2,3,4,5,6])
            return mutation(type,winner_list,atom_number,atom_x_size,atom_y_size)