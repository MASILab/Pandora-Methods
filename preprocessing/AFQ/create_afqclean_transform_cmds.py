import os

projs = ['/nfs/masi/hansencb/t1_tract_data/raw_data/NORMAL',
         '/nfs/masi/hansencb/t1_tract_data/raw_data/BLSA',
         '/nfs/masi/hansencb/t1_tract_data/raw_data/HCP']

cmd = '/scratch/hansencb/tract_preprocessing/AFQ/Atlas_OrganizeAFQclean_ACCRE.sh {} {} {}\n'

out_file = 'afqclean_transform_cmds.txt'
out_dir = '/nfs/masi/hansencb/t1_tract_data/registered_data'

with open(out_file, 'w') as f:
    for d in projs:
        proj = d.split('/')[-1]
        for subj in os.listdir(d):
            subj_dir = os.path.join(d, subj)
            if os.path.isdir(subj_dir):
                for sess in os.listdir(subj_dir):
                    sess_dir = os.path.join(subj_dir, sess)
                    if os.path.isdir(os.path.join(sess_dir, 'derivatives', 'AFQ_clean')):
                        linear_out = os.path.join(out_dir, 'AFQcleanLinear', '{}_{}_{}'.format(proj,subj,sess))
                        nonlin_out = os.path.join(out_dir, 'AFQcleanNonlinear', '{}_{}_{}'.format(proj, subj, sess))
                        if not os.path.isdir(linear_out) or not os.path.isdir(nonlin_out):
                            f.write(cmd.format(proj, subj, sess))
                        elif len(os.listdir(linear_out)) < 20:
                            f.write(cmd.format(proj, subj, sess))


