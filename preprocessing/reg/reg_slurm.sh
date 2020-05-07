#!/bin/bash

#SBATCH -J reg
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --time=12:00:00
#SBATCH --mem=16G
#SBATCH -o /scratch/hansencb/tract_preprocessing/logs/reg_%A_%a.out
#SBATCH -e /scratch/hansencb/tract_preprocessing/logs/reg_%A_%a.err
#SBATCH --array=0-2421%1

mapfile -t cmds < /scratch/hansencb/tract_preprocessing/reg_BLSA_cmds.txt
eval ${cmds[$SLURM_ARRAY_TASK_ID]}
