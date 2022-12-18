import pandas as pd
import numpy as np
#build the graph
import time
import os
import subprocess

def inpsd_initseed_generator(atom_x_size,atom_y_size,lattice_parameter,simulate_temp,opmode,applied_field,simulate_max_step,initseed_workdir='.'):
    inpsd_init = '''simid GA_optimizer
ncell   %s       %s         1                 System size
BC        P         P         0                 Boundary conditions (0=vacuum,P=periodic)

cell %s

Sym       0                                     Symmetry of lattice (0 for no, 1 for cubic, 2 for 2d cubic, 3 for hexagonal)

posfile  ./posfile
exchange ./exchange 
momfile  ./momfile
dm ./dm
#anisotropy ./anisotropy

Mensemble 1
maptype 1
posfiletype C

do_prnstruct 0                                 Print lattice structure (0=no, 1=yes)

Initmag   1                                   (1=random, 2=cone, 3=spec., 4=file)

mode      %s                                      S=SD, M=MC           
Temp      %s         K                     Measurement phase parameters
damping   0.4                                Damping parameter
hfield  %s
%s                                 Number of time-steps
plotenergy   1
''' %(atom_x_size,atom_y_size,lattice_parameter,opmode,simulate_temp,applied_field,simulate_max_step)
    with open('{}/inpsd_init.dat'.format(initseed_workdir),'w') as f:
        f.write('{}'.format(inpsd_init))
    




def init_seed(seed_number,sd_path,re_path,workdir='./seed'):
    #use bash scripts here to run UppASD MCMC
    bash_code = '''mkdir %s
for i in {0..%s}
do
mkdir ./$i
cp ../inpsd_init.dat ./$i/inpsd.dat
echo -e "\ntseed $RANDOM\n" >> ./$i/inpsd.dat
cp ../anisotropy ./$i
cp ../dm ./$i
cp ../exchange ./$i
cp ../momfile ./$i
cp ../posfile ./$i
done
wait

export OMP_NUM_THREADS=1
for i in {0..%s}
do
cd ./$i
%s  &
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
totE=$0
rm -r ./$i
done
wait 
''' %(re_path,seed_number-1,seed_number-1,sd_path,seed_number-1,re_path)
    with open('{}/UppASD_MCMC_laucher.bash'.format(workdir),'w') as f:
        f.write('{}'.format(bash_code))
    
    #subprocess.run(['cd {}'.format(workdir), 'bash UppASD_MCMC_laucher.bash'],shell=True,capture_output=False)

    os.system('cd {}; bash UppASD_MCMC_laucher.bash >../intermedia_uppasd.printscreen'.format(workdir))
    
