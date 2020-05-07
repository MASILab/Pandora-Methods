import os

projs = ['/nfs/masi/hansencb/t1_tract_data/raw_data/NORMAL',
         '/nfs/masi/hansencb/t1_tract_data/raw_data/BLSA',
         '/nfs/masi/hansencb/t1_tract_data/raw_data/HCP']

cmd = '/scratch/hansencb/tract_preprocessing/xtract/Atlas_OrganizeXTRACT_ACCRE.sh {} {} {}\n'

out_file = 'xtract_transform_cmds.txt'
out_dir = '/nfs/masi/hansencb/t1_tract_data/registered_data'

with open(out_file, 'w') as f:
    for d in projs:
        proj = d.split('/')[-1]
        for subj in os.listdir(d):
            subj_dir = os.path.join(d, subj)
            if os.path.isdir(subj_dir):
                for sess in os.listdir(subj_dir):
                    sess_dir = os.path.join(subj_dir, sess)
                    if os.path.isdir(os.path.join(sess_dir, 'derivatives', 'xtract')):
                        if not os.path.isdir(os.path.join(out_dir, 'XtractLinear', '{}_{}_{}'.format(proj,subj,sess))) or \
                           not os.path.isdir(os.path.join(out_dir, 'XtractNonlinear', '{}_{}_{}'.format(proj, subj, sess))):
                            f.write(cmd.format(proj, subj, sess))



