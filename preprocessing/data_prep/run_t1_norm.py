import os
from pathlib import Path
import multiprocessing

def t1_norm(sess):
    t1_path = Path.joinpath(sess, 'anat', 'T1.nii.gz')
    t1_n3_path = Path.joinpath(sess, 'anat', 'T1_N3.nii.gz')
    t1_norm_path = Path.joinpath(sess, 'anat', 'T1_NORM.nii.gz')
    cmd = '/nfs/masi/hansencb/t1_tract_data/preprocessing/normalize_T1.sh {} {} {}'.format(t1_path, t1_n3_path, t1_norm_path)
    os.system(cmd)

data_dir = '/nfs/masi/hansencb/t1_tract_data/raw_data'
proj_dirs = ['HCP_t1_retest']

threads = []
for proj in proj_dirs:
    proj_dir = os.path.join(data_dir, proj)
    subjs = Path(proj_dir)
    for subj in subjs.iterdir():
        sessions = Path(subj)
        if Path.is_dir(subj):
            for sess in sessions.iterdir():
                if Path.is_dir(Path.joinpath(sess, 'anat')):
                    t = multiprocessing.Process(target=t1_norm, args=(sess,))
                    threads.append(t)
                    t.start()

        if len(threads) >= 5:
            for thread in threads:
                thread.join()
            threads = []




