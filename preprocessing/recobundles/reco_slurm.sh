#!/bin/bash

#SBATCH -J reco
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --time=48:00:00
#SBATCH --mem=32G
#SBATCH -o /scratch/hansencb/tract_preprocessing/recobundles/logs/reco_%A_%a.out
#SBATCH -e /scratch/hansencb/tract_preprocessing/recobundles/logs/reco_%A_%a.err
#SBATCH --array=1-3873%25

module load GCC/5.4.0-2.26  OpenMPI/1.10.3 FSL/5.0.10
module load Anaconda3/5.0.1
source activate reco
export PYTHONPATH="/home/hansencb/.conda/envs/reco/bin"
mapfile -t cmds < /scratch/hansencb/tract_preprocessing/recobundles/reco_cmds.txt
eval ${cmds[$SLURM_ARRAY_TASK_ID]}
