import os
from shutil import copy

proj_dir = '/nfs/HCP/retest/data'
target_dir = '/nfs/masi/hansencb/t1_tract_data/raw_data/HCP'

if not os.path.isdir(target_dir):
    print('Making dir: {}'.format(target_dir))
    os.mkdir(target_dir)

for subj in os.listdir(proj_dir):
    subj_dir = os.path.join(proj_dir, subj)
    if os.path.isdir(subj_dir):
        session = subj + '_retest'
        paths = {'dti': os.path.join(subj_dir, 'T1w/Diffusion/data.nii.gz'),
                 'bval': os.path.join(subj_dir, 'T1w/Diffusion/bvals'),
                 'bvec': os.path.join(subj_dir, 'T1w/Diffusion/bvecs'),
                 't1': os.path.join(subj_dir, 'T1w/T1w_acpc_dc_restore_1.25.nii.gz')}

        all_present = True
        for t in paths:
            if not os.path.isfile(paths[t]):
                all_present = False

        if all_present:
            print('Copying data for subject {}'.format(subj))
            target_subj = os.path.join(target_dir, subj)
            if not os.path.isdir(target_subj):
                os.mkdir(target_subj)
            target_sess = os.path.join(target_subj, session)
            if not os.path.isdir(target_sess):
                os.mkdir(target_sess)
            target_dwi = os.path.join(target_sess, 'dwi')
            if not os.path.isdir(target_dwi):
                os.mkdir(target_dwi)
            target_anat = os.path.join(target_sess, 'anat')
            if not os.path.isdir(target_anat):
                os.mkdir(target_anat)

            target_paths = {'dti': os.path.join(target_dwi, 'Diffusion.nii.gz'),
                            'bval': os.path.join(target_dwi, 'Diffusion.bvals'),
                            'bvec': os.path.join(target_dwi, 'Diffusion.bvecs'),
                            't1': os.path.join(target_anat, 'T1.nii.gz')}

            for t in paths:
                copy(paths[t], target_paths[t])






