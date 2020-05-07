import os
import shutil

data_dirs = ['/nfs/masi/hansencb/t1_tract_data/raw_data/HCP',
             '/nfs/masi/hansencb/t1_tract_data/raw_data/BLSA',
             '/nfs/masi/hansencb/t1_tract_data/raw_data/NORMAL']

for proj in data_dirs:
    for subj in os.listdir(proj):
        subj_path = os.path.join(proj, subj)
        for sess in os.listdir(subj_path):
            sess_path = os.path.join(subj_path, sess)
            reco_path = os.path.join(sess_path, 'derivatives', 'recobundles')
            target = os.path.join(sess_path, 'derivatives', 'recobundles_bak')

            if os.path.isdir(reco_path):
                print('Moving {} to {}'.format(reco_path, target))
                shutil.move(reco_path, target)