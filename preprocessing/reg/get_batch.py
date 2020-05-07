import os

batch_file = 'b0_iso_batches/batch_25.txt'

with open(batch_file, 'r') as f:
    for line in f.readlines():
        dwi_path, tmp_path, tmp_outpath, work_dir, slurm_path = line.strip().split(',')
        if os.path.isdir(work_dir):
            os.system('mv {} {}'.format(dwi_path, dwi_path+'_bak.nii.gz'))
            os.system('cp {} {}'.format(tmp_outpath, dwi_path))
            os.system('rm -rf {}'.format(work_dir))
