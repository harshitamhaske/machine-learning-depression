#!/bin/bash
#SBATCH --time=1:00:00
#SBATCH --nodes=32
#SBATCH --ntasks-per-node=12
#SBATCH --cpus-per-task=1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=peregrine@compsy.nl
#SBATCH --job-name=python_cpu
#SBATCH --mem=8000
module load Python/3.5.1-foss-2016a
module load R/3.3.1-foss-2016a
module load Theano/0.7.0-goolfc-2.7.11-Python-3.4.2
module load matplotlib/1.5.1-foss-2016a-Python-3.5.1
module load Tk/8.6.4-foss-2016a-libX11-1.6.3
module load libX11/1.6.3-foss-2016a
gitdir="ICPE_machine_learning_workgroup"
cd $gitdir
#pip install --user -r requirements.txt
cd learner
echo "Running main.py"
export MPLBACKEND="agg"
mpirun python main.py

