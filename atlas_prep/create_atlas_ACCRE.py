import torch
import numpy as np
import nibabel as nib
import os
from tqdm import tqdm
from multiprocessing import Process
import argparse
import tempfile
from paramiko import SSHClient
from scp import SCPClient

#
# def scp_here(paths, target_dir, scp):
#     i = 1
#     work_paths = []
#     for path in paths:
#         target_path = os.path.join(target_dir, '{}.nii.gz'.format(i))
#         scp.get(path, local_path=target_path)
#         work_paths.append(target_path)
#
#     return work_paths

def average_vols(paths, out_path, thresh, tmp_path, scp):
    total = None
    init = True
    num_used = 0

    with tqdm(total=len(paths)) as pbar:
        for i, path in enumerate(paths):
            scp.get(path, local_path=tmp_path)
            vol = nib.load(tmp_path).get_fdata()
            vol[vol<thresh] = 0
            vol[vol>=thresh] = 1
            if np.sum(vol) >= 10:
                if init:
                    total = vol
                    init = False
                else:
                    total = total + vol
                pbar.update(1)
                num_used += 1

    avg = total/num_used
    nft = nib.Nifti1Image(avg, nib.load(paths[0]).affine, nib.load(paths[0]).header)
    nib.save(nft, out_path)

    return num_used
    with open(out_path.strip('.nii.gz')+'_count.txt', 'w') as f:
        f.write('{}'.format(num_used))

def main():
    parser = argparse.ArgumentParser
    parser.add_argument('--paths', nargs='+', type=str)
    parser.add_argument('--out', type=str)
    parser.add_argument('--thresh', type=float)

    args = parser.parse_args()

    work_dir = tempfile.mkdtemp(prefix='wmatlas')

    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect('hickory')

    scp = SCPClient(ssh.get_transport())

    # work_paths = scp_here(args.paths, work_dir, scp)
    work_out = os.path.join(work_dir, 'out.nii.gz')
    # num_used = average_vols(work_paths, work_out, args.thresh)

    num_used = average_vols(args.paths, work_out, args.thresh, os.path.join(work_dir, 'tmp.nii.gz'), scp)
    scp.put(work_out, remote_path=args.out)

    count_file = os.path.join(work_dir, 'count.txt')
    with open(count_file, 'w') as f:
        f.write('{}'.format(num_used))

    scp.put(count_file, remote_path=args.out.strip('.nii.gz')+'_count.txt')


if __name__ == "__main__":
    main()
