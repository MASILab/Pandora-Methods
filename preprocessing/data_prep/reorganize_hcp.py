import os
from shutil import move

dwi_dir = '/nfs/masi/hansencb/t1_tract_data/raw_data/HCP_bak'
t1_dir = '/nfs/masi/hansencb/t1_tract_data/raw_data/HCP_t1'
t1_retest_dir = '/nfs/masi/hansencb/t1_tract_data/raw_data/HCP_t1_retest'
out_dir = '/nfs/masi/hansencb/t1_tract_data/raw_data/HCP'

for subj in os.listdir(dwi_dir):
    subj_dir = os.path.join(dwi_dir, subj)
    if os.path.isdir(subj_dir):
        for sess in os.listdir(subj_dir):
            sess_dir = os.path.join(subj_dir, sess)
            if os.path.isdir(sess_dir):
                sess_out = os.path.join(out_dir, subj, sess)
                os.makedirs(sess_out, exist_ok=True)
                if os.path.isdir(os.path.join(sess_dir, 'dwi')):
                    print('move {} to {}'.format(os.path.join(sess_dir, 'dwi'),os.path.join(sess_out, 'dwi')))
                    move(os.path.join(sess_dir, 'dwi'), os.path.join(sess_out, 'dwi'))
                t1_path = os.path.join(t1_dir, subj, sess, 'anat')
                if sess.endswith('retest'):
                    t1_path = os.path.join(t1_retest_dir, subj, sess, 'anat')

                if os.path.isdir(t1_path):
                    print('move {} to {}'.format(t1_path, os.path.join(sess_out, 'anat')))
                    move(t1_path, os.path.join(sess_out, 'anat'))

