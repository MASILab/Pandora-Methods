import os

proj_dir = '/nfs/masi/hansencb/t1_tract_data/raw_data/BLSA_xnat/BLSA/'

for subj in os.listdir(proj_dir):
    subj_dir = os.path.join(proj_dir, subj)
    if os.path.isdir(subj_dir):
        for sess in os.listdir(subj_dir):
            sess_dir = os.path.join(subj_dir, sess)
            if os.path.isdir(sess_dir):
                for scan in os.listdir(sess_dir):
                    if scan.endswith('dtiQA_v6'):
                        scan_dir = os.path.join(sess_dir, scan)
                        prep_dir = os.path.join(scan_dir, 'PREPROCESSED')
                        if os.path.isdir(prep_dir):
                            zip_file = os.path.join(prep_dir, 'PREPROCESSED.zip')
                            weird_dir = os.path.join(prep_dir, 'PREPROCESSED')

                            dwmri_files = [os.path.join(prep_dir, 'dwmri.nii.gz'),
                                           os.path.join(prep_dir, 'dwmri.bval'),
                                           os.path.join(prep_dir, 'dwmri.bvec'),
                                           os.path.join(prep_dir, 'mask.nii.gz')]

                            if os.path.isdir(weird_dir):
                                os.system('mv {}/* {}'.format(weird_dir, prep_dir))
                                os.system('rmdir {}'.format(weird_dir))

                            dwi_files_exist = True
                            for f in dwmri_files:
                                if not os.path.isfile(f):
                                    dwi_files_exist = False

                            if os.path.isfile(zip_file):
                                os.system('rm {}'.format(zip_file))

                            if not dwi_files_exist:
                                print('{} needs to be redownloaded'.format(sess_dir))