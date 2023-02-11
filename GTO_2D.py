from turtle import Turtle
import pandas as pd
import numpy as np
#build the graph
import time
from pathlib import Path
import json
import os
from tqdm import tqdm
import argparse
from GT_operators.comu_basic_2D import crossover_mutation
from Parsers.moment_parser import moment_file_parser
from Selection import creat_Winner,init_selection,evaluate_generation,parents_selection_for_store,creat_init,creat_elites,Roulette_Wheel,Steady_State,Tournament_selection
from Visualization.Ridgeline import plot_ridegline
'''
Parser domain
'''
parser = argparse.ArgumentParser(description='GTO-2D optimizer for monolayer spin system energy minimizer')

input_json = Path('./input_GTO.json').read_text()
args = argparse.Namespace(**json.loads(input_json))

parser.add_argument('--use_artificial_seed', default=False)
parser.add_argument('--backend', default='UppASD') #backend = 'NENN' neuralevolutionary network
parser.add_argument('--resource', default='Local')  #resource = 'HPC'
parser.add_argument('--generation_range', default=int(50))
parser.add_argument('--offspring_nunber', default=int(60))    
parser.add_argument('--number_of_random_init_gen', default=int(40))    #this one is for the random search
parser.add_argument('--opmode', default='H')  # opmode = 'S'
parser.add_argument('--simulate_max_step_seed', default= 'mcNstep  1200')    # simulate_max_step_seed= '  1200'
parser.add_argument('--simulate_max_step_SA', default= 'mcNstep  1200')  # simulate_max_step_SA= 'Nstep  1200'
parser.add_argument('--simulate_max_step_normal', default= 'mcNstep  1800') # simulate_max_step_normal= 'Nstep  1200'
parser.add_argument('--Elitism_Selection_flag', default=True)#if this Elitism Selection is true, we select best offsprings and keep it directly to next generation
parser.add_argument('--Elites_number', default=int(10))   
parser.add_argument('--Elitism_optimization_flag', default=True)        # if this flag is true, instead of keep it, we also put the elites into next generations optimization.
parser.add_argument('--Elitism_optimization_number', default=int(10))  
parser.add_argument('--selection_methods', default='Steady_State_Selection')    
parser.add_argument('--Steady_State_Selection_candidates', default=int(12))    
parser.add_argument('--Steady_State_Selection_number', default=int(4)) #each caididate pair length
parser.add_argument('--Roulette_Wheel_number', default=int(4)) 
parser.add_argument('--Tournament_selection_number', default=int(4)) 
parser.add_argument('--Tournament_selection_smallgroup_number', default=int(8)) 

# selection_methods = 'Roulette_Wheel_Selection'
# Roulette_Wheel_number = 4 #Roulette_Wheel_number parents set

# selection_methods = 'Tournament_selection'
# Tournament_selection_number = 4
# Tournament_selection_smallgroup_number = 8

parser.add_argument('--SA_activation', default=False)
parser.add_argument('--atom_x_size', default=int(60)) 
parser.add_argument('--atom_y_size', default=int(60)) 
parser.add_argument('--atom_number', default=int(60*60))
parser.add_argument('--GA_variance_threshold', default=float(1e-7)) 
parser.add_argument('--GA_var_threshold_range', default=int(10)) 
parser.add_argument('--multi_factor', default=float( 0.5))#this one is the ratio of crssover and mutation, which indicate corssover prob
parser.add_argument('--lattice_parameter', default='''1.00000   0.00000   0.00000 
0.00000   1.00000   0.00000
0.00000   0.00000   1.00000''') 
#TODO: add poscar and cif parser for crystal informations here
parser.add_argument('--simulate_temp', default=float( 0.0001)) 
parser.add_argument('--applied_field', default='''0 0 0''') 
parser.add_argument('--threshold_flag', default= 'Y')
parser.add_argument('--thresholdsteps', default= int(100))
parser.add_argument('--threshold_energy_value', default= float( 1e-9))
parser.add_argument('--threshold_moment_value', default= float( 1e-9))    
parser.add_argument('--sd_path', default= '/home/qichenx/software/UppASD/bin/sd.gfortran')
#sd_path = '/Users/qichen/opt/UppASD/UppASD_nsc/UppASD/source/sd'
#sd_path ='/proj/snic2014-8-7/users/x_qicxu/uppasd/UppASD-threshold/bin/sd.ifort'
parser.add_argument('--ridegline_plot_path_generations', default= './statistic_result_ridegline.svg' )
parser.add_argument('--ridegline_plot_path_elites', default= './elites_result_ridegline.svg')
args = parser.parse_args(namespace=args)    









if __name__ == '__main__':

    #Welcome page 
    logo = r'''
                     ,----,
                   ,/   .`|     ,----..
  ,----..        ,`   .'  :    /   /   \                    ,----,       ,---,
 /   /   \     ;    ;     /   /   .     :                 .'   .' \    .'  .' `\
|   :     :  .'___,/    ,'   .   /   ;.  \     ,---,.   ,----,'    | ,---.'     \
.   |  ;. /  |    :     |   .   ;   /  ` ;   ,'  .' |   |    :  .  ; |   |  .`\  |
.   ; /--`   ;    |.';  ;   ;   |  ; \ ; | ,---.'   ,   ;    |.'  /  :   : |  '  |
;   | ;  __  `----'  |  |   |   :  | ; | ' |   |    |   `----'/  ;   |   ' '  ;  :
|   : |.' .'     '   :  ;   .   |  ' ' ' : :   :  .'      /  ;  /    '   | ;  .  |
.   | '_.' :     |   |  '   '   ;  \; /  | :   |.'       ;  /  /-,   |   | :  |  '
'   ; : \  |     '   :  |    \   \  ',  /  `---'        /  /  /.`|   '   : | /  ;
'   | '/  .'     ;   |.'      ;   :    /              ./__;      :   |   | '` ,/
|   :    /       '---'         \   \ .'               |   :    .'    ;   :  .'
 \   \ .'                       `---`                 ;   | .'       |   ,.'
  `---`                                               `---'          '---'
  
  
Author: Qichen Xu 

Main Contributors: Zhuanglin Shen and Anna Delin. 

 
Department of Applied Physics, KTH Royal Institute of Technology

******************
Optimization start
******************
    '''

    print(logo)


    
    '''
    All hyperparameters:
    '''
    use_artificial_seed =eval( args.use_artificial_seed)
    #hyperparameter:
    backend = args.backend
    #backend = 'NENN' neuralevolutionary network

    #resource = 'HPC'
    resource =  args.resource

    generation_range= int(args.generation_range)

    offspring_nunber = int( args.offspring_nunber)
    number_of_random_init_gen =int(args.number_of_random_init_gen)
    #MODE chose
    opmode = args.opmode
    simulate_max_step_seed=  args.simulate_max_step_seed
    simulate_max_step_SA=  args.simulate_max_step_SA
    simulate_max_step_normal= args.simulate_max_step_normal
    
    # opmode = 'S'
    # simulate_max_step_seed= 'Nstep  1200'
    # simulate_max_step_SA= 'Nstep  1200'
    # simulate_max_step_normal= 'Nstep  1200'
    
    
    #if this Elitism Selection is true, we select best offsprings and keep it directly to next generation
    Elitism_Selection_flag =  eval(args.Elitism_Selection_flag)
    Elites_number = int(args.Elites_number)
    # if this flag is true, instead of keep it, we also put the elites into next generations optimization.
    Elitism_optimization_flag =eval( args.Elitism_optimization_flag)
    Elitism_optimization_number = int( args.Elitism_optimization_number)

    # selection_methods = 'Roulette_Wheel_Selection'
    # Roulette_Wheel_number = 4 #Roulette_Wheel_number parents set

    selection_methods =  args.selection_methods
    Steady_State_Selection_candidates = int( args.Steady_State_Selection_candidates)
    Steady_State_Selection_number =  int(args.Steady_State_Selection_number)
    Roulette_Wheel_number =int(args.Roulette_Wheel_number) 
    Tournament_selection_number =int(args.Tournament_selection_number) 
    Tournament_selection_smallgroup_number =int(args.Tournament_selection_smallgroup_number) 
    # selection_methods = 'Tournament_selection'
    # Tournament_selection_number = 4
    # Tournament_selection_smallgroup_number = 8

    #for system:
    SA_activation = eval(args.SA_activation)
    atom_number =int( args.atom_number)
    atom_x_size = int(args.atom_x_size)
    atom_y_size =int( args.atom_y_size)
    GA_variance_threshold = float( args.GA_variance_threshold)
    GA_var_threshold_range =  int(args.GA_var_threshold_range)

    #for GA

    multi_factor = float( args.multi_factor)
    lattice_parameter= args.lattice_parameter
     #TODO: add poscar and cif parser for crystal informations here

    simulate_temp =float( args.simulate_temp)

    applied_field = args.applied_field



    threshold_flag =  args.threshold_flag
    thresholdsteps =  int(args.thresholdsteps)
    
    threshold_energy_value =  float(args.threshold_energy_value)

    threshold_moment_value = float( args.threshold_moment_value)

    #sd_path = '/Users/qichen/opt/UppASD/UppASD_nsc/UppASD/source/sd'
    #sd_path ='/proj/snic2014-8-7/users/x_qicxu/uppasd/UppASD-threshold/bin/sd.ifort'
    sd_path =  args.sd_path

    ridegline_plot_path_generations =  args.ridegline_plot_path_generations
    ridegline_plot_path_elites =  args.ridegline_plot_path_elites





    fitness_data_list = []  
    elites_data_list = []
    time_list = []

    print('Simulated spin system size: {} * {}'.format(atom_x_size,atom_y_size))
    print('Simulation temperature: {}K'.format(simulate_temp))
    print('Variance threshold: {} mRy/atom'.format(GA_variance_threshold))



    if use_artificial_seed==True:
        artificial_print ='No artificial seeds exist.'
    else:
        artificial_print ='Artificial seeds imported'
    print(artificial_print)
    print('Local optimization engine: {} with threshold implemented by Zhuanglin Shen'.format(backend))
    if backend == 'UppASD':
        '''
        Initial seed section:
        '''
        #choose computional resources 
        if resource=='HPC':
            from UppASD_backend.Init_seed_HPC import  inpsd_initseed_generator,init_seed
            from UppASD_backend.Init_SA_HPC import inpsd_init_SA_generator, creat_init
            from UppASD_backend.Inpsd_normal_HPC import inpsd_init_normal_generator,creat_generation

        if resource=='Local':
            #note here we default use only 1 core for 1 offspring calculation.
            from UppASD_backend.Init_seed_Local import  inpsd_initseed_generator,init_seed
            from UppASD_backend.Init_SA_Local import inpsd_init_SA_generator, creat_init
            from UppASD_backend.Inpsd_normal_Local import inpsd_init_normal_generator,creat_generation

        
        #generate inpsd_init.dat
        inpsd_initseed_generator(atom_x_size,atom_y_size,lattice_parameter,simulate_temp,opmode,applied_field,simulate_max_step_seed,initseed_workdir='.')

        #generate inpsd_generation_SA.dat
        inpsd_init_SA_generator(atom_x_size,atom_y_size,lattice_parameter,simulate_temp,applied_field,opmode,simulate_max_step_SA,initseed_workdir='.')
        
        #generate inpsd_generation.dat
        inpsd_init_normal_generator(atom_x_size,atom_y_size,lattice_parameter,simulate_temp,opmode,applied_field,simulate_max_step_normal,threshold_flag,thresholdsteps,threshold_energy_value,threshold_moment_value,initseed_workdir='.')

        print('Start broadcasting seeds on potential energy surface')

        start_time = time.time() 

        with tqdm(total=offspring_nunber) as pbar:
            pbar.set_description("Initialized random seeds" )
            #Initial random search:
            init_prepare = []
            fitness_value_vis = []
            fitness_value_vis_temp = []
            index_seed = 0
            if SA_activation == True:
                #optional SA in the very begining
                while len(init_prepare)< offspring_nunber:
                    random_seed_folder = './seed_random_search_{}'.format(index_seed)
                    re_path = 're'
                    if not os.path.isdir(random_seed_folder):
                        os.makedirs(random_seed_folder)
                    creat_init(number_of_random_init_gen,sd_path,re_path,workdir=random_seed_folder)
                    fitness_list,fitness_value_vis = evaluate_generation(random_seed_folder+'/'+re_path) 
                    init_prepare_temp = init_selection(fitness_list) #delect too close initial point
                    init_prepare = init_prepare+init_prepare_temp
                    pbar.update(number_of_random_init_gen)
                    index_seed = index_seed +1
                for i in init_prepare:
                    fitness_value_vis_temp.append(i[0])
                fitness_value_vis = fitness_value_vis+fitness_value_vis_temp

                #take only number = offspring_nunber result as initial seed
                successful_seed,fitness_list_sort = parents_selection_for_store(init_prepare,offspring_nunber)
                fitness_value_vis.sort()
                fitness_data_list.append(fitness_value_vis[:offspring_nunber])
                time_list.append(time.time()-start_time)

                if Elitism_Selection_flag ==True:
                    elites_list_for_store,elites_fitness_list_sort = parents_selection_for_store(successful_seed,Elites_number)
                    creat_elites(elites_list_for_store,0,atom_number)
                    elites_data_list.append(elites_fitness_list_sort)
                
            else:
                while len(init_prepare)< offspring_nunber:
                    random_seed_folder = './seed_random_search_{}'.format(index_seed)
                    re_path = 're'
                    if not os.path.isdir(random_seed_folder):
                        os.makedirs(random_seed_folder)
                    init_seed(number_of_random_init_gen,sd_path,re_path,workdir=random_seed_folder)
                    fitness_list,fitness_value_vis = evaluate_generation(random_seed_folder+'/'+re_path) 
                    init_prepare_temp = init_selection(fitness_list) #delect too close initial point
                    init_prepare = init_prepare+init_prepare_temp
                    pbar.update(number_of_random_init_gen)
                    index_seed = index_seed +1
                for i in init_prepare:
                    fitness_value_vis_temp.append(i[0])
                fitness_value_vis = fitness_value_vis+fitness_value_vis_temp

                #take only number = offspring_nunber result as initial seed
                successful_seed,fitness_list_sort = parents_selection_for_store(init_prepare,offspring_nunber)
                fitness_value_vis.sort()
                fitness_data_list.append(fitness_value_vis[:offspring_nunber])
                time_list.append(time.time()-start_time)
                if Elitism_Selection_flag ==True:
                    elites_list_for_store,elites_fitness_list_sort = parents_selection_for_store(successful_seed,Elites_number)
                    creat_elites(elites_list_for_store,0,atom_number)
                    elites_data_list.append(elites_fitness_list_sort)
        #start literation    
        parents_list_for_store = successful_seed
        print('Start building genetic tunnel with {} '.format(selection_methods))
        for i in  (pbar := tqdm(range(generation_range))):    
            i = i+1
            pbar.set_description(f"Generations: ")
            next_generation_list = []

            if Elitism_optimization_flag == True:#in this flag the elites can be long life and have child, emm the winner of life.
                for elite_i in parents_list_for_store[:Elitism_optimization_number]:
                    next_generation_list = next_generation_list+[np.transpose(elite_i[1][1])]
                if selection_methods == 'Roulette_Wheel_Selection':
                    while len(next_generation_list)< offspring_nunber:
                        Roulette_Wheel_Selection_result = Roulette_Wheel(parents_list_for_store,Roulette_Wheel_number)
                        offspring_indvidual = crossover_mutation(Roulette_Wheel_Selection_result,multi_factor,atom_x_size,atom_y_size,atom_number)
                        next_generation_list = next_generation_list+[offspring_indvidual]

                if selection_methods == 'Steady_State_Selection':
                    parents_list_for_store = parents_list_for_store[Elitism_optimization_number:Elitism_optimization_number+Steady_State_Selection_candidates]
                    while len(next_generation_list)< offspring_nunber:
                        Steady_State_Selection_result = Steady_State(parents_list_for_store,Steady_State_Selection_number)
                        offspring_indvidual = crossover_mutation(Steady_State_Selection_result,multi_factor,atom_x_size,atom_y_size,atom_number)
                        next_generation_list = next_generation_list+[offspring_indvidual]

                if selection_methods == 'Tournament_selection':
                    while len(next_generation_list)< offspring_nunber:
                        Tournament_selection_result = Tournament_selection(parents_list_for_store,Tournament_selection_number,Tournament_selection_smallgroup_number)
                        offspring_indvidual = crossover_mutation(Tournament_selection_result,multi_factor,atom_x_size,atom_y_size,atom_number)
                        next_generation_list = next_generation_list+[offspring_indvidual]                                                               
            else:
                if selection_methods == 'Roulette_Wheel_Selection':
                    while len(next_generation_list)< offspring_nunber:
                        Roulette_Wheel_Selection_result = Roulette_Wheel(parents_list_for_store,Roulette_Wheel_number)
                        offspring_indvidual = crossover_mutation(Roulette_Wheel_Selection_result,multi_factor,atom_x_size,atom_y_size,atom_number)
                        next_generation_list = next_generation_list+[offspring_indvidual]

                if selection_methods == 'Steady_State_Selection':
                    parents_list_for_store = parents_list_for_store[0:Steady_State_Selection_candidates]
                    while len(next_generation_list)< offspring_nunber:
                        Steady_State_Selection_result = Steady_State(parents_list_for_store,Steady_State_Selection_number)
                        offspring_indvidual = crossover_mutation(Steady_State_Selection_result,multi_factor,atom_x_size,atom_y_size,atom_number)
                        next_generation_list = next_generation_list+[offspring_indvidual]

                if selection_methods == 'Tournament_selection':
                    while len(next_generation_list)< offspring_nunber:
                        Tournament_selection_result = Tournament_selection(parents_list_for_store,Tournament_selection_number,Tournament_selection_smallgroup_number)
                        offspring_indvidual = crossover_mutation(Tournament_selection_result,multi_factor,atom_x_size,atom_y_size,atom_number)
                        next_generation_list = next_generation_list+[offspring_indvidual]

            creat_generation(next_generation_list,i,sd_path,atom_number,re_path='re')
            next_gen_eval_result,fitness_value_vis = evaluate_generation( './generation_{}'.format(i)+'/'+re_path) 
            parents_list_for_store,fitness_list_sort = next_gen_eval_result,fitness_value_vis
            
            if Elitism_Selection_flag ==True:
                elites_list_for_store,elites_fitness_list_sort = parents_selection_for_store(parents_list_for_store+elites_list_for_store,Elites_number)
                creat_elites(elites_list_for_store,i,atom_number)
                elites_data_list.append(elites_fitness_list_sort)
            fitness_data_list.append(fitness_value_vis)
            time_list.append(time.time()-start_time)
            if np.var(fitness_list_sort[:GA_var_threshold_range]) <= GA_variance_threshold or np.var(elites_fitness_list_sort) <= GA_variance_threshold  :
                break
    
    print('Hit variance threshold: {}'.format(np.var(fitness_list_sort[:GA_var_threshold_range])))
    print('All minimazation is done')

    if backend == 'NENN':
        pass

    '''
    Visualization section
    '''
    print('...................')
    plot_ridegline(fitness_data_list,ridegline_plot_path_generations)        
    plot_ridegline(elites_data_list,ridegline_plot_path_elites)       

    #store data optional
    # np.save('./fitness_all', np.array(fitness_data_list))
    # np.save('./fitness_elite', np.array(elites_data_list))
    # np.save('./time', np.array(time_list))

    result_df = pd.DataFrame({'fitness_all':fitness_data_list,'fitness_elite' :elites_data_list,'time':np.array(time_list)})
    result_df.to_pickle("./Result_stat.pkl") 

    '''
    Clean section:
    In this section, we use the clean module to make sure middle-product are deleted after simulation.
    '''