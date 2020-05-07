#!/bin/bash

#SBATCH --account=vuiis_masi_gpu_acc
#SBATCH --partition=pascal
#SBATCH --gres=gpu:1
#SBATCH -J xtract
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --time=24:00:00
#SBATCH --mem=16G
#SBATCH -o /scratch/hansencb/tract_preprocessing/xtract/logs/xtract_%A_%a.out
#SBATCH -e /scratch/hansencb/tract_preprocessing/xtract/logs/xtract_%A_%a.err
#SBATCH --array=0-5

mapfile -t cmds < /scratch/hansencb/tract_preprocessing/xtract/xtract_cmds.txt
eval ${cmds[$SLURM_ARRAY_TASK_ID]}
