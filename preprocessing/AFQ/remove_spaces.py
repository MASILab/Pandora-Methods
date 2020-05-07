import os
import shutil

projs = ['/nfs/masi/hansencb/t1_tract_data/raw_data/NORMAL',
         '/nfs/masi/hansencb/t1_tract_data/raw_data/BLSA',
         '/nfs/masi/hansencb/t1_tract_data/raw_data/HCP']


for d in projs:
    proj = d.split('/')[-1]
    for subj in os.listdir(d):
        subj_dir = os.path.join(d, subj)
        if os.path.isdir(subj_dir):
            for sess in os.listdir(subj_dir):
                sess_dir = os.path.join(subj_dir, sess)
                deriv_dir = os.path.join(sess_dir, 'derivatives', 'AFQ_clipped')
                if os.path.isdir(deriv_dir):
                    for tract in os.listdir(deriv_dir):
                        new_name = tract.replace(' ', '_')
                        src = os.path.join(deriv_dir, tract)
                        target = os.path.join(deriv_dir, new_name)
                        print('Moving {} to {}'.format(src, target))
                        shutil.move(src,target)




