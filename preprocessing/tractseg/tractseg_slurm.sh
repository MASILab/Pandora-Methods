#!/bin/bash

#SBATCH -J tractseg
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --time=8:00:00
#SBATCH --mem=16G
#SBATCH -o /scratch/hansencb/tract_preprocessing/tractseg/logs/tractseg_%A_%a.out
#SBATCH -e /scratch/hansencb/tract_preprocessing/tractseg/logs/tractseg_%A_%a.err
#SBATCH --array=0-6%50

mapfile -t cmds < /scratch/hansencb/tract_preprocessing/tractseg/tractseg_cmds.txt
eval ${cmds[$SLURM_ARRAY_TASK_ID]}
