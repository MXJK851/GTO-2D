import pandas as pd
import numpy as np
#build the graph
import time
import os
from Parsers.moment_parser import moment_file_parser

def creat_Winner(child_configuration,gen_number,atom_number):
    first3column = pd.DataFrame(data={'iterens':-np.ones(atom_number).astype(int),'iatom':np.ones(atom_number).astype(int),'iatom2':np.array(range(atom_number))+1})
    mypath = 'Winner_{}'.format(gen_number)
    if not os.path.isdir(mypath):
        os.makedirs(mypath)
    for i in range(len(child_configuration)):
        mon_w = child_configuration[i][1][0]
        pd.concat([first3column,pd.DataFrame(mon_w)],axis=1).drop(columns=[0,1,2]).to_csv('./{}/{}.out'.format(mypath,i),header=False,index=False, sep=' ',float_format='%.5f')
        head= '''################################################################################
# File type: M
# Simulation type: S
# Number of atoms:     65536
# Number of ensembles:         1
################################################################################
#iterens   iatom           |Mom|             M_x             M_y             M_z
'''
        with open('./{}/{}.out'.format(mypath,i),'r+') as f:
            original = f.read()
            f.seek(0)
            f.write('{}'.format(head))
            f.write(original)


def creat_elites(child_configuration,gen_number,atom_number):
    first3column = pd.DataFrame(data={'iterens':-np.ones(atom_number).astype(int),'iatom':np.ones(atom_number).astype(int),'iatom2':np.array(range(atom_number))+1})
    mypath = 'Elites_{}'.format(gen_number)
    if not os.path.isdir(mypath):
        os.makedirs(mypath)
    for i in range(len(child_configuration)):
        mon_w = child_configuration[i][1][0]
        pd.concat([first3column,pd.DataFrame(mon_w)],axis=1).drop(columns=[0,1,2]).to_csv('./{}/{}.out'.format(mypath,i),header=False,index=False, sep=' ',float_format='%.5f')
        head= '''################################################################################
# File type: M
# Simulation type: S
# Number of atoms:     65536
# Number of ensembles:         1
################################################################################
#iterens   iatom           |Mom|             M_x             M_y             M_z
'''
        with open('./{}/{}.out'.format(mypath,i),'r+') as f:
            original = f.read()
            f.seek(0)
            f.write('{}'.format(head))
            f.write(original)



def creat_init(child_configuration,atom_number):
    first3column = pd.DataFrame(data={'iterens':-np.ones(atom_number).astype(int),'iatom':np.ones(atom_number).astype(int),'iatom2':np.array(range(atom_number))+1})
    mypath = 'final_seed'
    if not os.path.isdir(mypath):
        os.makedirs(mypath)
    for i in range(len(child_configuration)):
        mon_w = child_configuration[i][1][0]
        pd.concat([first3column,pd.DataFrame(mon_w)],axis=1).drop(columns=[0,1,2]).to_csv('./{}/{}.out'.format(mypath,i),header=False,index=False, sep=' ',float_format='%.5f')
        head= '''################################################################################
# File type: M
# Simulation type: S
# Number of atoms:     65536
# Number of ensembles:         1
################################################################################
#iterens   iatom           |Mom|             M_x             M_y             M_z
'''
        with open('./{}/{}.out'.format(mypath,i),'r+') as f:
            original = f.read()
            f.seek(0)
            f.write('{}'.format(head))
            f.write(original)

def init_selection(candidates):
    #we use fitness strategy
    parents_list = []
    fitness_list = []
    for i in candidates:
        fitness_list.append(i[0])
    fitness_list_sort= np.sort(fitness_list)
    #remove too close one
    #https://stackoverflow.com/questions/65905055/how-to-delete-very-close-values-to-a-numpy-array
    threshold = 0.000001
    diff = np.empty(fitness_list_sort.shape)
    diff[0] = np.inf  # always retain the 1st element
    diff[1:] = np.diff(fitness_list_sort)
    mask = diff > threshold
    new_fitness_list_sort = fitness_list_sort[mask]
    for i in new_fitness_list_sort:
        parents_list.append(candidates[fitness_list.index(i)])
    return parents_list

#here maybe a problem,but I test it (check here if something happened)
def evaluate_generation(re_folder):
    #note that we use 0,1,2,3,4,5.out to represent each indivedure in generation
    fitness_list = []
    fitness_value_all = []
    for i in os.listdir(re_folder):
        if i[0] != ".":
            fitness_list.append([float(i),moment_file_parser('{}/{}'.format(re_folder,i))])
            fitness_value_all.append(float(i))
    fitness_list.sort()
    fitness_value_all.sort()
    return fitness_list,fitness_value_all

def parents_selection_for_store(candidates,candidate_list_len):
    #we use fitness strategy
    parents_list = []
    fitness_list = []
    for i in candidates:
        fitness_list.append(i[0])
    fitness_list_sort= np.sort(fitness_list)
    for i in fitness_list_sort[:candidate_list_len]:
        parents_list.append(candidates[fitness_list.index(i)])
    fitness_list_sort = fitness_list_sort[:candidate_list_len]
        
    return parents_list,fitness_list_sort

def Roulette_Wheel_one_shot(parents_list_for_store):

    max = sum([f[0] for f in parents_list_for_store])
    
    selection_probs = [f[0]/max for f in parents_list_for_store]

    return parents_list_for_store[np.random.choice(len(parents_list_for_store), p=selection_probs)]

def Roulette_Wheel(parents_list_for_store,Roulette_Wheel_number):
    Roulette_Wheel_Selection_result = []
    for i in range(Roulette_Wheel_number):
        Roulette_Wheel_Selection_result = Roulette_Wheel_Selection_result+[Roulette_Wheel_one_shot(parents_list_for_store)]
    return Roulette_Wheel_Selection_result

def Steady_State(parents_list_for_store,Steady_State_Selection_number):
    Steady_State_Selection_result = []
    select_index = np.random.choice(list(range(len(parents_list_for_store))), Steady_State_Selection_number)
    for i in select_index:
        Steady_State_Selection_result = Steady_State_Selection_result+[parents_list_for_store[i]]
    return Steady_State_Selection_result

def Tournament_selection(parents_list_for_store,Tournament_selection_number,Tournament_selection_smallgroup_number):
    Steady_State_Selection_result = []
    for ts in range(Tournament_selection_number):
        temp_group = []
        select_index = np.random.choice(list(range(len(parents_list_for_store))), Tournament_selection_smallgroup_number)
        for i in select_index:
            temp_group = temp_group+[parents_list_for_store[i]]
        temp_group.sort
        Steady_State_Selection_result = Steady_State_Selection_result+[temp_group[0]]
    return Steady_State_Selection_result