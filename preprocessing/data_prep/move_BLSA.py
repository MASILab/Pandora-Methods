import os
from shutil import move

dwi_dir = '/nfs/masi/hansencb/t1_tract_data/raw_data/BLSA_dwi/BLSA'
t1_dir = '/nfs/masi/hansencb/t1_tract_data/raw_data/BLSA_T1/BLSA'

target_dir = '/nfs/masi/hansencb/t1_tract_data/raw_data/BLSA'

for subj in os.listdir(dwi_dir):
    dwi_subj_dir = os.path.join(dwi_dir, subj)
    t1_subj_dir = os.path.join(t1_dir, subj)

    subj_id = subj.split('_')[-1]

    if os.path.isdir(t1_subj_dir):
        for sess in os.listdir(dwi_subj_dir):
            dwi_sess_dir = os.path.join(dwi_subj_dir, sess)
            t1_sess_dir = os.path.join(t1_subj_dir, sess)
            if os.path.isdir(t1_sess_dir):
                dwi_scan_dir = ''
                t1_scan_dir = ''
                for scan in os.listdir(dwi_sess_dir):
                    if scan.endswith('dtiQA_v6'):
                        dwi_scan_dir = os.path.join(dwi_sess_dir, scan)
                        break
                for scan in os.listdir(t1_sess_dir):
                    if scan.endswith('T1wStructuralMRI'):
                        t1_scan_dir = os.path.join(t1_sess_dir, scan)
                        break

                if os.path.isdir(dwi_scan_dir) and os.path.isdir(t1_scan_dir):
                    dwi_paths = [os.path.join(dwi_scan_dir, 'PREPROCESSED/dwmri.nii.gz'),
                                 os.path.join(dwi_scan_dir, 'PREPROCESSED/dwmri.bval'),
                                 os.path.join(dwi_scan_dir, 'PREPROCESSED/dwmri.bvec'),
                                 os.path.join(dwi_scan_dir, 'PREPROCESSED/mask.nii.gz')]
                    t1_path = ''
                    for fname in os.listdir(os.path.join(t1_scan_dir, 'NIFTI')):
                        if 'MPRAGE' in fname and '.nii.gz' in fname:
                            t1_path = os.path.join(t1_scan_dir, 'NIFTI', fname)

                    dwi_exists = True
                    for p in dwi_paths:
                        if not os.path.isfile(p):
                            dwi_exists = False

                    if dwi_exists:
                        target_subj = os.path.join(target_dir, subj_id)
                        if not os.path.isdir(target_subj):
                            os.mkdir(target_subj)

                        target_sess = os.path.join(target_subj, sess)
                        if not os.path.isdir(target_sess):
                            os.mkdir(target_sess)

                        target_dwi = os.path.join(target_sess, 'dwi')
                        if not os.path.isdir(target_dwi):
                            os.mkdir(target_dwi)

                        target_anat = os.path.join(target_sess, 'anat')
                        if not os.path.isdir(target_anat):
                            os.mkdir(target_anat)

                        dwi_targets = [os.path.join(target_dwi, 'Diffusion.nii.gz'),
                                       os.path.join(target_dwi, 'Diffusion.bvals'),
                                       os.path.join(target_dwi, 'Diffusion.bvecs'),
                                       os.path.join(target_dwi, 'mask.nii.gz')]
                        t1_target = os.path.join(target_anat, 'T1.nii.gz')

                        for i in range(len(dwi_paths)):
                            # print('moving {} to {}'.format(dwi_paths[i], dwi_targets[i]))
                            move(dwi_paths[i], dwi_targets[i])

                        # print('moving {} to {}'.format(t1_path, t1_target))
                        move(t1_path, t1_target)







