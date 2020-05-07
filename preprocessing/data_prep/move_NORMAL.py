import os
from shutil import copy

proj_dir = '/fs4/masi/hansencb/NORMAL_preprocessed/NORMAL'
target_dir = '/nfs/masi/blaberj/tract1/data/raw_data/NORMAL'

if not os.path.isdir(target_dir):
    print('Making dir: {}'.format(target_dir))
    os.mkdir(target_dir)

for subj in os.listdir(proj_dir):
    subj_dir = os.path.join(proj_dir, subj)
    if os.path.isdir(subj_dir):
        for session in os.listdir(subj_dir):
            sess_dir = os.path.join(subj_dir, session)
            if os.path.isdir(sess_dir):

                scans = {'dti': [], 't1': [], 'seg': [], 't1seg': []}
                for scan in os.listdir(sess_dir):
                    scan_dir = os.path.join(sess_dir, scan)
                    if os.path.isdir(scan_dir):
                        if scan.endswith('dtiQA_v6'):
                            scans['dti'].append(scan_dir)
                        elif scan.endswith('Multi_Atlas_v2'):
                            scans['seg'].append(scan_dir)
                        else:
                            scans['t1'].append(scan_dir)

                if len(scans['dti']) > 0:
                    for t1 in scans['t1']:
                        for seg in scans['seg']:
                            if t1.split('-x-')[-1] == seg.split('-x-')[-2]:
                                scans['t1seg'].append((t1,seg))

                if len(scans['t1seg']) > 0:

                    if not os.path.isdir(os.path.join(target_dir, subj)):
                        print('Making dir: {}'.format(os.path.join(target_dir, subj)))
                        os.mkdir(os.path.join(target_dir, subj))
                    if not os.path.isdir(os.path.join(target_dir, subj, session)):
                        print('Making dir: {}'.format(os.path.join(target_dir, subj, session)))
                        os.mkdir(os.path.join(target_dir, subj, session))
                    if not os.path.isdir(os.path.join(target_dir, subj, session, 'anat')):
                        print('Making dir: {}'.format(os.path.join(target_dir, subj, session, 'anat')))
                        os.mkdir(os.path.join(target_dir, subj, session, 'anat'))
                    if not os.path.isdir(os.path.join(target_dir, subj, session, 'dwi')):
                        print('Making dir: {}'.format(os.path.join(target_dir, subj, session, 'dwi')))
                        os.mkdir(os.path.join(target_dir, subj, session, 'dwi'))
                    if not os.path.isdir(os.path.join(target_dir, subj, session, 't1seg')):
                        print('Making dir: {}'.format(os.path.join(target_dir, subj, session, 't1seg')))
                        os.mkdir(os.path.join(target_dir, subj, session, 't1seg'))

                    t1_name=''
                    for f in os.listdir(os.path.join(scans['t1seg'][0][0], 'NIFTI')):
                        if f.endswith('.nii.gz'):
                            t1_name = f
                    t1_path = os.path.join(scans['t1seg'][0][0], 'NIFTI', t1_name)
                    target_t1_path = os.path.join(target_dir, subj, session, 'anat', 'T1.nii.gz')

                    print('Copying {} \n\t to {}'.format(t1_path, target_t1_path))
                    copy(t1_path, target_t1_path)

                    seg_path = os.path.join(scans['t1seg'][0][1], 'SEG', 'orig_target_seg.nii.gz')
                    target_seg_path = os.path.join(target_dir, subj, session, 't1seg', 'seg.nii.gz')

                    print('Copying {} \n\t to {}'.format(seg_path, target_seg_path))
                    copy(seg_path, target_seg_path)

                    dwi_names = ['dwmri.nii.gz', 'dwmri.bval', 'dwmri.bvec',
                                 'inv_reg.mat', 'mask.nii.gz', 'subj_seg.nii.gz']
                    target_dwi_names = ['Diffusion.nii.gz', 'Diffusion.bvals', 'Diffusion.bvecs',
                                 'inv_reg.mat', 'mask.nii.gz', 'subj_seg.nii.gz']

                    max_dir_dwi = (0, '')
                    for dwi in scans['dti']:
                        bval_path = os.path.join(dwi, 'PREPROCESSED', 'dwmri.bval')
                        with open(bval_path, 'r') as bvf:
                            num_bvals = len(bvf.readline().split(' '))
                            if num_bvals > max_dir_dwi[0]:
                                max_dir_dwi = (num_bvals, dwi)

                    for i in range(len(dwi_names)):
                        path = os.path.join(max_dir_dwi[1], 'PREPROCESSED', dwi_names[i])
                        target_path = os.path.join(target_dir, subj, session, 'dwi', target_dwi_names[i])

                        if i in [3,5]:
                            try:
                                print('Copying {} \n\t to {}'.format(path, target_path))
                                copy(path, target_path)
                            except:
                                print('{} does not exist'.format(path))
                        else:
                            print('Copying {} \n\t to {}'.format(path, target_path))
                            copy(path, target_path)



