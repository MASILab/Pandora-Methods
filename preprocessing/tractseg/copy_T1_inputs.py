import os
import shutil

data_dirs = ['/nfs/masi/hansencb/t1_tract_data/raw_data/HCP',
             '/nfs/masi/hansencb/t1_tract_data/raw_data/BLSA',
             '/nfs/masi/hansencb/t1_tract_data/raw_data/NORMAL']

input_dir = '/nfs/masi/hansencb/t1_tract_data/learning/Input'

for proj in data_dirs:
    for subj in os.listdir(proj):
        subj_path = os.path.join(proj, subj)
        for sess in os.listdir(subj_path):
            sess_path = os.path.join(subj_path, sess)
            t1_path = os.path.join(sess_path, 'reg', 'T1_N3_lin_atlas.nii.gz')

            target = os.path.join(input_dir, '{}_{}_{}'.format(proj.split('/')[-1], subj, sess), 'T1_N3_lin_atlas.nii.gz')

            if not os.path.isfile(target):
                print('Copying {} to {}'.format(t1_path, target))
                #shutil.copy(t1_path, target)
