#!/bin/bash

#SBATCH -J reco
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --time=24:00:00
#SBATCH --mem=16G
#SBATCH -o /scratch/hansencb/tract_preprocessing/logs/reco_%A_%a.out
#SBATCH -e /scratch/hansencb/tract_preprocessing/logs/reco_%A_%a.err
#SBATCH --array=0-2%3

module load GCC/5.4.0-2.26  OpenMPI/1.10.3 FSL/5.0.10
module load Anaconda3/5.0.1
source activate reco
mapfile -t cmds < /scratch/hansencb/tract_preprocessing/reco_cmds.txt
eval ${cmds[$SLURM_ARRAY_TASK_ID]}
