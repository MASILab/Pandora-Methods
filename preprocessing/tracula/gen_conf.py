import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--work_dir', type=str)
args = parser.parse_args()
work_dir = args.work_dir

free_dir = os.path.join(work_dir, 'OUTPUTS', 'freesurfer')
sd = os.path.join(work_dir, 'OUTPUTS', 'tracula')
subj_id = 'subj'
nii = os.path.join(work_dir, 'INPUTS', 'Diffusion.nii.gz')
bval = os.path.join(work_dir, 'INPUTS', 'Diffusion.bvals')
bvec = os.path.join(work_dir, 'INPUTS', 'Diffusion.bvecs')

conf_path = '/nfs/masi/hansencb/t1_tract_data/preprocessing/tracula/trac.conf'
out = os.path.join(work_dir, 'INPUTS', 'trac.conf')

with open(conf_path, 'r') as f:
    conf = f.read()

conf = conf.format(free_dir, sd, subj_id, nii, bvec, bval)

with open(out, 'w') as f:
    f.write(conf)


