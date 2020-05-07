import os

projs = ['/nfs/masi/hansencb/t1_tract_data/raw_data/NORMAL',
         '/nfs/masi/hansencb/t1_tract_data/raw_data/BLSA',
         '/nfs/masi/hansencb/t1_tract_data/raw_data/HCP']

cmd = '/scratch/hansencb/tract_preprocessing/tracula/Atlas_OrganizeTracula_ACCRE.sh {} {} {}\n'

out_file = 'tracula_transform_cmds.txt'
out_dir = '/nfs/masi/hansencb/t1_tract_data/registered_data'

with open(out_file, 'w') as f:
    for d in projs:
        proj = d.split('/')[-1]
        for subj in os.listdir(d):
            subj_dir = os.path.join(d, subj)
            if os.path.isdir(subj_dir):
                for sess in os.listdir(subj_dir):
                    sess_dir = os.path.join(subj_dir, sess)
                    if os.path.isdir(os.path.join(sess_dir, 'derivatives', 'tracula')):
                        if not os.path.isdir(os.path.join(out_dir, 'TraculaLinear', '{}_{}_{}'.format(proj,subj,sess))) or \
                           not os.path.isdir(os.path.join(out_dir, 'TraculaNonlinear', '{}_{}_{}'.format(proj, subj, sess))):
                            f.write(cmd.format(proj, subj, sess))



