import numpy as np
import nibabel as nib
from pathlib import Path

atlas_dir = Path('/nfs/masi/hansencb/t1_tract_data/AtlasesQA')
# methods = ['AFQ', 'AFQclipped', 'Recobundles', 'TractSeg', 'Xtract', 'Tracula']
# methods = ['AFQ']
# methods = ['AFQ', 'AFQclipped', 'TractSeg', 'Xtract', 'Tracula']
methods = ['RecoBundles']
for method in methods:
    method_dir = atlas_dir.joinpath(method)
    for fname in method_dir.iterdir():
        if fname.name.endswith('.nii.gz'):
            nii = nib.load(str(fname))
            img = nii.get_fdata()
            img = np.float32(img)

            new_nii = nib.Nifti1Image(img, nii.affine)
            nib.save(new_nii, fname)

    # method_dir = atlas_dir.joinpath(method, 'supplementary')
    # for fname in method_dir.iterdir():
    #     if fname.name.endswith('.nii.gz'):
    #         nii = nib.load(str(fname))
    #         img = nii.get_fdata()
    #         img = np.float32(img)
    #
    #         new_nii = nib.Nifti1Image(img, nii.affine)
    #         nib.save(new_nii, fname)

