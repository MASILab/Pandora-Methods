import nibabel as nib
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str)
parser.add_argument('--output', type=str)
args = parser.parse_args()

nft = nib.load(args.input)
arr = nft.get_fdata()
arr = arr.astype(np.float32)

nft = nib.Nifti1Image(arr, nft.affine, nft.header)
nft.header.set_data_dtype(np.float32)
nib.save(nft, args.output)