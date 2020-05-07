import os

batch_file = 'b0_iso_batches/batch_25.txt'

with open(batch_file, 'r') as f:
    for line in f.readlines():
        dwi_path, tmp_path, tmp_outpath, work_dir, slurm_path = line.strip().split(',')
        if not os.path.isdir(work_dir):
            os.mkdir(work_dir)
        os.system('cp {} {}'.format(dwi_path, tmp_path))
        os.system('sbatch {}'.format(slurm_path))
