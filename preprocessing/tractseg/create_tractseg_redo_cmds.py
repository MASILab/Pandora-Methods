import os

lname = 'QA_tractSeg.csv'

work_dir = '/scratch/hansencb/tract_preprocessing/tractseg/data/'
cmd = 'mkdir -p {} && ' \
      'scp -r hickory:{}/dwi {} && ' \
      'SINGULARITY_HOME=$(mktemp -d) && ' \
      'singularity exec --cleanenv --contain --home $SINGULARITY_HOME --bind /tmp:/tmp ' \
      '--bind {}/dwi:/data /scratch/hansencb/tract_preprocessing/tractseg/tractseg.simg bash ' \
      '-c \"source /neurodocker/startup.sh && TractSeg -i /data/Diffusion.nii.gz --raw_diffusion_input\" && ' \
      'mv {}/dwi/tractseg_output {}/dwi/tractseg &&'\
      'scp -r {}/dwi/tractseg hickory:{} && ' \
      'rm -rf {} && ' \
      'rmdir {}\n'

out_file = 'tractseg_redo_cmds.txt'

with open(out_file, 'w') as f:
    with open(lname, 'r') as fin:
        for line in fin.readlines():
            parts = line.split(',')
            proj, subj, sess = parts[1], parts[2], parts[3]
            sess_dir = os.path.join('/nfs/masi/hansencb/t1_tract_data/raw_data', proj, subj, sess)

            work_subj_dir = os.path.join(work_dir, subj)
            work_sess_dir = os.path.join(work_dir, subj, sess)
            dwi_path = os.path.join(sess_dir, 'dwi', 'Diffusion.nii.gz')
            out_dir = os.path.join(sess_dir, 'derivatives')

            if os.path.isfile(dwi_path):
                f.write(cmd.format(work_sess_dir, sess_dir, work_sess_dir,
                                   work_sess_dir, work_sess_dir, work_sess_dir, work_sess_dir, 
                                   out_dir, work_sess_dir, work_subj_dir))
            else:
                print(sess_dir)
