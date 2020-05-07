import os

d = '/nfs/masi/hansencb/t1_tract_data/raw_data/BLSA'

slurm = '#!/bin/bash \n\
#SBATCH --nodes=1\n\
#SBATCH --ntasks=1\n\
#SBATCH --mem=16G\n\
#SBATCH --time=4:00:00\n\
#SBATCH --output={}/logs/{}.log\n\
module load GCC/5.4.0-2.26  OpenMPI/1.10.3 FSL/5.0.10\n\
flirt -ref {} -in {} -out {} -applyisoxfm 2.2'

slurm_dir = './b0_iso_slurms'
batch_dir = './b0_iso_batches'

cmd = 'flirt -ref {} -in {} -out {} -applyisoxfm 2.2'
tmp_dir = '/scratch/hansencb/tract_preprocessing'
batch = []
batch_num = 1
for subj in os.listdir(d):
    subj_dir = os.path.join(d, subj)
    for sess in os.listdir(subj_dir):
        sess_dir = os.path.join(subj_dir, sess)
        dwi_path = os.path.join(sess_dir, 'dwi', 'Diffusion.nii.gz')
        work_dir = os.path.join(tmp_dir, sess)
        temp_path = os.path.join(work_dir, 'uniso_Diffusion.nii.gz')
        temp_out_path = os.path.join(work_dir, 'Diffusion.nii.gz')
        if os.path.isfile(dwi_path):
            with open(os.path.join(slurm_dir, sess)+'.slurm', 'w') as f:
                f.write(slurm.format(tmp_dir, sess, temp_path, temp_path, temp_out_path))
            batch.append(','.join([dwi_path, temp_path, temp_out_path, work_dir, os.path.join(slurm_dir, sess)+'.slurm']))

            if len(batch) >= 100:
                with open(os.path.join(batch_dir, 'batch_{}.txt'.format(batch_num)), 'w') as f:
                    for b in batch:
                        f.write('{}\n'.format(b))
                batch = []
                batch_num += 1

if len(batch) != 0:
    with open(os.path.join(batch_dir, 'batch_{}.txt'.format(batch_num)), 'w') as f:
        for b in batch:
            f.write('{}\n'.format(b))
    batch = []
    batch_num += 1





