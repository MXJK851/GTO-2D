import pandas as pd
import numpy as np
#build the graph
import time
import os


def inpsd_init_normal_generator(atom_x_size,atom_y_size,lattice_parameter,simulate_temp,opmode,applied_field,simulate_max_step,threshold_flag,thresholdsteps,threshold_energy_value,threshold_moment_value,initseed_workdir='.'):
    inpsd_init = '''simid GA_optimizer
ncell   %s       %s         1                 System size
BC        P         P         0                 Boundary conditions (0=vacuum,P=periodic)

cell %s

Sym       0                                     Symmetry of lattice (0 for no, 1 for cubic, 2 for 2d cubic, 3 for hexagonal)

posfile  ./posfile
exchange ./exchange 
momfile  ./momfile
dm ./dm
anisotropy ./anisotropy

Mensemble 1
maptype 1
posfiletype C

do_prnstruct 0                                 Print lattice structure (0=no, 1=yes)
Initmag   4                                   (1=random, 2=cone, 3=spec., 4=file)
restartfile ./gen_restart.out
plotenergy   1
mode      %s                                      S=SD, M=MC           
Temp      %s         K                     Measurement phase parameters
damping   0.4                                Damping parameter
hfield  %s
%s                                 Number of time-steps
do_threshold    %s
thresholdstep   %s 
threshold_energy_value   %s
threshold_moment_value   %s
do_cumu Y
cumu_step 20
cumu_buff 1
do_avrg Y
avrg_step 20
avrg_buff 1
''' %(atom_x_size,atom_y_size,lattice_parameter,opmode,simulate_temp,applied_field,simulate_max_step,threshold_flag,thresholdsteps,threshold_energy_value,threshold_moment_value)
    with open('{}/inpsd_generation.dat'.format(initseed_workdir),'w') as f:
        f.write('{}'.format(inpsd_init))


def creat_generation(child_configuration,gen_number,sd_path,atom_number,re_path='re'):
    first3column = pd.DataFrame(data={'iterens':-np.ones(atom_number).astype(int),'iatom':np.ones(atom_number).astype(int),'iatom2':np.array(range(atom_number))+1})
    seed_number = len(child_configuration)    
    mypath = 'generation_{}'.format(gen_number)
    if not os.path.isdir(mypath):
        os.makedirs(mypath)
    for i in range(len(child_configuration)):
        mon_w = child_configuration[i]
        pd.concat([first3column,pd.DataFrame(mon_w)],axis=1).to_csv('./{}/{}.out'.format(mypath,i),header=False,index=False, sep=' ',float_format='%.5f')
        head= '''################################################################################ 
# File type: M
# Simulation type: EM_GT
# Number of atoms:     By setting
# Number of ensembles:         1
################################################################################
#iterens   iatom           |Mom|             M_x             M_y             M_z
'''
        with open('./{}/{}.out'.format(mypath,i),'r+') as f:
            original = f.read()
            f.seek(0)
            f.write('{}'.format(head))
            f.write(original)
        
#use bash scripts here to run UppASD MCMC
    
    bash_code = '''mkdir %s
for i in {0..%s}
do  
mkdir ./$i
cp ../inpsd_generation.dat ./$i/inpsd.dat
cp ../anisotropy ./$i
cp ../dm ./$i
cp ../exchange ./$i
cp ../momfile ./$i
cp ../posfile ./$i
cp ./$i.out ./$i/gen_restart.out
rm ./$i.out
done

for i in {0..%s}
do
cd ./$i
srun -n1 -N1 --exact %s  &
cd ..
done
wait

for i in {0..%s}
do
cd ./$i
totE=`tail -n1 totenergy.*.out | awk '{ print $2}'`
mv ./restart*.out ./$totE
cp ./$totE ../%s
cd ..
rm -r ./$i
totE=$0
done
wait 
''' %(re_path,seed_number-1,seed_number-1,sd_path,seed_number-1,re_path)
    with open('{}/UppASD_MCMC_laucher.bash'.format(mypath),'w') as f:
        f.write('{}'.format(bash_code))
    
    os.system('cd {}; bash UppASD_MCMC_laucher.bash >../intermedia_uppasd.printscreen'.format(mypath))

