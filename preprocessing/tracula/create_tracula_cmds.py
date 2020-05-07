import os

projs = ['/nfs/masi/hansencb/t1_tract_data/raw_data/NORMAL',
         '/nfs/masi/hansencb/t1_tract_data/raw_data/BLSA',
         '/nfs/masi/hansencb/t1_tract_data/raw_data/HCP']

cmd = '/scratch/hansencb/tract_preprocessing/tracula/tracula_pipeline_ACCRE.sh {} \n'

out_file = 'tracula_cmds.txt'

with open(out_file, 'w') as f:
    for d in projs:
        for subj in os.listdir(d):
            subj_dir = os.path.join(d, subj)
            if os.path.isdir(subj_dir):
                for sess in os.listdir(subj_dir):
                    sess_dir = os.path.join(subj_dir, sess)
                    if not os.path.isdir(os.path.join(sess_dir, 'derivatives', 'tracula')):
                        f.write(cmd.format(sess_dir))
