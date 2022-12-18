# GTO-2D

## What is GTO-2D

GTO-2D is a metaheuristic optimization package based on genetic tunneling algorithm that designed for complex low-dimensional magnetic systems. Only magnetic interactions needed to start GTO-2D optimization, no extra prior knowledge or initial guess is needed. The potential user may include but is not limited to scientists that interesting in 2D magnetism. This package currently mainly uses the UppASD backend and accepts DFT-calculated interactions in the same format as UppASD.
 
<p align="center">
  <img src="misc/GTO2D.png" width="100%" title="GTO=2D">
<p align="justify">

## Installation
 * First install variance controlled UppASD package `UppASD_VT`:
   ```python
    upzip ./UppASD_VT.zip
    cd ./UppASD_VT
    bash ./setup_UppASD.sh   
    make <profile>  
   ```
Where `<profile>` is a suitable compiler profile, i.e. `ifort`, `gfortran`, `gfortran-osx` and so on.  

 * Then install `GTO-2D` package:
   ```python
    conda create --name gto2d python=3.10
    conda activate gto2d
    pip install -r requirements.txt
   ```
## Usage
### Toy demo with Bloch skyrmions
All magentic interaction data are prepared in the same style as UppASD package, more detail on input files can check on:
https://uppasd.github.io/UppASD-manual/

 * Running with prepared JSON input file:
   ```python
   cd ./Example/Toy/
   python ../../GTMCO_2D.py
   ```
    Before execution, please make sure `input_GTO.json` is exsit with all interaction files, it should looks like:
   ```python
    {
        "use_artificial_seed": "False",
        "backend":"UppASD",
        "resource":"Local",
        "generation_range":"50",
        "offspring_nunber":"18",   
        "number_of_random_init_gen":"18", 
        "opmode":"H", 
        "simulate_max_step_seed": "mcNstep  1800",   
        "simulate_max_step_SA": "mcNstep  1800",
        "simulate_max_step_normal": "mcNstep  1800",
        "Elitism_Selection_flag":"True",
        "Elites_number":"10",  
        "Elitism_optimization_flag":"True",    
        "Elitism_optimization_number":"10", 
        "selection_methods":"Steady_State_Selection",   
        "Steady_State_Selection_candidates":"12",   
        "Steady_State_Selection_number":"4",
        "SA_activation":"False",
        "atom_x_size":"60",
        "atom_y_size":"60",
        "atom_number":"3600",
        "GA_variance_threshold":"1e-10",
        "GA_var_threshold_range":"10",
        "multi_factor":"0.5",
        "lattice_parameter":"1.00000   0.00000   0.00000 \n 0.00000   1.00000   0.00000 \n 0.00000   0.00000   1.00000",
        "simulate_temp":"0.0001",
        "applied_field":"0 0 150",
        "threshold_flag": "Y",
        "thresholdsteps": "100",
        "threshold_energy_value": "1e-10",
        "threshold_moment_value": "1e-10",   
        "sd_path": "../../UppASD_VT/bin/sd.gfortran",
        "ridegline_plot_path_generations": "./statistic_result_ridegline.svg" ,
        "ridegline_plot_path_elites": "./elites_result_ridegline.svg"
    }
   ```

   If everything goes well, one welcome logo will print to the screen:
   ```python

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

    Main Contributors:Qichen Xu, Zhuanglin Shen, Olle Eriksson and Anna Delin.

    Department of Applied Physics, KTH Royal Institute of Technology

    ******************
    Optimization start
    ******************

    Simulated spin system size: 60 * 60
    Simulation temperature: 0.0001K
    Variance threshold: 1e-10 mRy/atom
    Artificial seeds imported
    Local optimization engine: UppASD with threshold implemented by Zhuanglin Shen
    Start broadcasting seeds on potential energy surface
   ```
  * Running with prepared JSON input and new flags:
    ```python
      python ./1/GTMCO_2D.py --offspring_nunber 40
    ```
    The GTO-2D will firstly consider values set by flag `--offspring_nunber 40`.

More demo can be find in our data repo:

xxxx (our paper's data)


### Cite us

If you used GTO-2D in your research work, we kindly request you condider citing our paper:

xxx