import os

l = '/nfs/masi/hansencb/t1_tract_data/preprocessing/reg/reg_last_last_time.csv'

atlas_path = '/scratch/hansencb/tract_preprocessing/reg/mni_icbm152_t1_tal_nlin_asym_09c_masked.nii.gz'
script_path = '/scratch/hansencb/tract_preprocessing/reg/Registration2AtlasSkullStrip.sh'
singularity_path = '/scratch/hansencb/tract_preprocessing/reg/reg.simg'
work_dir = '/scratch/hansencb/tract_preprocessing/reg/data/'
cmd = 'mkdir -p {} && scp -r hickory:{} {} && scp hickory:{} {} && ' \
      'singularity exec {} {} {} {} {} {} && scp -r {} hickory:{} && rm -rf {} && rmdir {}\n'

out_file = '/nfs/masi/hansencb/t1_tract_data/preprocessing/reg/reg_last_redo_cmds.txt'

with open(out_file, 'w') as f:
    with open(l, 'r') as fin:
        for line in fin.readlines():
            parts = line.strip().split(',')
            subj, sess, sess_dir = parts[1], parts[2], parts[3]
            if os.path.isdir(sess_dir):
                t1_dir = os.path.join(sess_dir, 'anat')
                b0_path = os.path.join(sess_dir, 'dwi', 'b0.nii.gz')
                subj_work_dir = os.path.join(work_dir, subj)
                sess_work_dir = os.path.join(work_dir, subj, sess)
                b0_work_path = os.path.join(sess_work_dir, 'b0.nii.gz')
                t1_work_dir = os.path.join(sess_work_dir, 'anat')
                out_work_path = os.path.join(sess_work_dir, 'reg')
                out_path = os.path.join(sess_dir, 'reg_redo')
                if os.path.isdir(t1_dir) and os.path.isfile(b0_path):
                    f.write(cmd.format(sess_work_dir, t1_dir, sess_work_dir, b0_path, b0_work_path,
                                singularity_path, script_path, b0_work_path, t1_work_dir, atlas_path,
                                out_work_path, out_work_path, out_path, sess_work_dir, subj_work_dir))
