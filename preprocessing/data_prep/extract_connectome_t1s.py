import os
from shutil import move

folder = '/nfs/masi/hansencb/t1_tract_data/raw_data/HCP_t1'
sess_add = ''
for zfile in os.listdir(folder):
    subj_id = zfile.split('_')[0]
    zpath = os.path.join(folder, zfile)
    if zfile.endswith('.zip'):
        os.system('unzip -d {} {}'.format(folder, zpath))

        subj_dir = os.path.join(folder, subj_id)
        sess_dir = os.path.join(subj_dir, subj_id + sess_add)
        os.mkdir(sess_dir)

        anat_dir = os.path.join(sess_dir, 'anat')
        os.mkdir(anat_dir)

        t1_path = os.path.join(subj_dir, 'unprocessed', '3T', 'T1w_MPR1', '{}_3T_T1w_MPR1.nii.gz'.format(subj_id))
        move(t1_path, os.path.join(anat_dir,'T1.nii.gz'))
