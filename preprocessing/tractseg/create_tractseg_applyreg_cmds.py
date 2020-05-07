import os

projs = ['/nfs/masi/hansencb/t1_tract_data/raw_data/NORMAL',
         '/nfs/masi/hansencb/t1_tract_data/raw_data/BLSA',
         '/nfs/masi/hansencb/t1_tract_data/raw_data/HCP']

cmd = '/scratch/hansencb/tract_preprocessing/tractseg/PrepareTractSegInputOutputACCRE.sh {} {} {}\n'

out_file = 'tractseg_apply_cmds.txt'
out_dir = "/nfs/masi/hansencb/t1_tract_data/learning/Output_TractSeg"
in_dir = "/nfs/masi/hansencb/t1_tract_data/learning/Input"

with open(out_file, 'w') as f:
    for d in projs:
        proj = d.split('/')[-1]
        for subj in os.listdir(d):
            subj_dir = os.path.join(d, subj)
            if os.path.isdir(subj_dir):
                for sess in os.listdir(subj_dir):
                    sess_dir = os.path.join(subj_dir, sess)

                    needs_run = True
                    out_path = os.path.join(out_dir, '{}_{}_{}'.format(proj,subj,sess))
                    in_path = os.path.join(in_dir, '{}_{}_{}'.format(proj,subj,sess), 'T1_N3_lin_atlas.nii.gz')
                    if os.path.isdir(out_path):
                        if len(os.listdir(out_path)) == 72 and os.path.isfile(in_path):
                            needs_run = False

                    if needs_run:
                        f.write(cmd.format(proj, subj, sess))



