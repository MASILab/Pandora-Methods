import os

projs = ['/nfs/masi/hansencb/t1_tract_data/raw_data/NORMAL',
         '/nfs/masi/hansencb/t1_tract_data/raw_data/HCP',
         '/nfs/masi/hansencb/t1_tract_data/raw_data/BLSA']


work_dir = '/scratch/hansencb/tract_preprocessing/tractseg'
cmd = 'mkdir -p {} && ' \
      'scp -r hickory:{}/dwi {} && ' \
      'SINGULARITY_HOME=$(mktemp -d) && ' \
      'singularity exec --cleanenv --contain --home $SINGULARITY_HOME --bind /tmp:/tmp ' \
      '--bind {}/dwi:/data /scratch/hansencb/tract_preprocessing/tractseg/tractseg.simg bash ' \
      '-c \"source /neurodocker/startup.sh && TractSeg -i /data/Diffusion.nii.gz --raw_diffusion_input\" && ' \
      'mkdir {}/derivatives && ' \
      'mv {}/dwi/tractseg_output {}/derivatives/tractseg && ' \
      'scp -r {}/derivatives hickory:{} && ' \
      'rm -rf {} && ' \
      'rmdir {}\n'

out_file = 'tractseg_cmds.txt'

with open(out_file, 'w') as f:
    for proj in projs:
        for subj in os.listdir(proj):
            subj_dir = os.path.join(proj, subj)
            if os.path.isdir(subj_dir):
                for sess in os.listdir(subj_dir):
                    sess_dir = os.path.join(subj_dir, sess)
                    if os.path.isdir(sess_dir):
                        work_subj_dir = os.path.join(work_dir, subj)
                        work_sess_dir = os.path.join(work_dir, subj, sess)
                        dwi_path = os.path.join(sess_dir, 'dwi', 'Diffusion.nii.gz')

                        if os.path.isfile(dwi_path) and not os.path.isdir(os.path.join(sess_dir, 'derivatives', 'tractseg')):
                            f.write(cmd.format(work_sess_dir, sess_dir, work_sess_dir, work_sess_dir,
                                               work_sess_dir, work_sess_dir, work_sess_dir, work_sess_dir,
                                               sess_dir, work_sess_dir, work_subj_dir))



