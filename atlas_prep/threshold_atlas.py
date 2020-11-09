import numpy as np
import nibabel as nib
from pathlib import Path

atlas_dir = Path('/nfs/masi/hansencb/t1_tract_data/AtlasesQA')
# methods = ['AFQ', 'AFQclipped', 'Recobundles', 'TractSeg', 'Xtract', 'Tracula']
# methods = ['AFQ']
methods = ['Recobundles']
for method in methods:
    method_dir = atlas_dir.joinpath(method)
    for fname in method_dir.iterdir():
        if fname.name.endswith('.nii.gz'):
            nii = nib.load(str(fname))
            img = nii.get_fdata()
            img[img<0.01] = 0

            new_nii = nib.Nifti1Image(img, nii.affine, header=nii.header)
            nib.save(new_nii, fname)
