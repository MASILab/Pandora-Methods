import nibabel as nib
import numpy as np
import os

atlas_dir = '/nfs/masi/hansencb/t1_tract_data/Atlases/TractSegNonlinear'

out_file = 'bad_subjects.txt'
with open(out_file, 'w') as f:
    for sess in os.listdir(atlas_dir):
        sess_dir = os.path.join(atlas_dir, sess)
        if sess.startswith('HCP'):
            tract_path = os.path.join(sess_dir, 'AF_left.nii.gz')
            vol = nib.load(tract_path).get_fdata()
            if vol[52, 133, 16] != 0 or vol[52, 36, 105] != 0:
                f.write('{}\n'.format(tract_path))
