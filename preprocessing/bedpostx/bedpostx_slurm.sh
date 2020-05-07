#!/bin/bash

#SBATCH -J bedpostx
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --time=48:00:00
#SBATCH --mem=16G
#SBATCH -o /scratch/hansencb/tract_preprocessing/bedpostx/logs/reg_%A_%a.out
#SBATCH -e /scratch/hansencb/tract_preprocessing/bedpostx/logs/reg_%A_%a.err
#SBATCH --array=0-0%1

mapfile -t cmds < /scratch/hansencb/tract_preprocessing/bedpostx/bedpostx_NORMAL_cmds.txt
eval ${cmds[$SLURM_ARRAY_TASK_ID]}
