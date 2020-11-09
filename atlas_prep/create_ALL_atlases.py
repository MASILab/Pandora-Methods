import torch
import numpy as np
import nibabel as nib
import os
from tqdm import tqdm
from multiprocessing import Process

def weighted_average_vols(paths, out_path, weights):
    avg = None
    init = True

    with tqdm(total=len(paths)) as pbar:
        for i, path in enumerate(paths):
            vol = nib.load(path).get_fdata()
            if init:
                avg = vol * weights[i]
                init = False
            else:
                avg = avg + (vol * weights[i])
            pbar.update(1)

    nft = nib.Nifti1Image(avg, nib.load(paths[0]).affine, nib.load(paths[0]).header)
    nib.save(nft, out_path)


def create_atlases(out_dir, prefix):
    projs = ['HCP', 'BLSA', 'NORMAL']
    data = {}

    for proj in projs:
        proj_dir = os.path.join(out_dir, proj)
        for fname in os.listdir(proj_dir):
            if fname.startswith(prefix) and fname.endswith('.nii.gz'):
                if fname not in data:
                    data[fname] = [[],[]]
                img_path = os.path.join(proj_dir, fname)
                count_path = os.path.join(proj_dir, fname.strip('.nii.gz')+'_count.txt')
                with open(count_path, 'r') as f:
                    count = int(f.readline())
                data[fname][0].append(img_path)
                data[fname][1].append(count)

    keys = []
    with open(os.path.join(out_dir, 'order.txt'), 'r') as f:
        for line in f.readlines():
            keys.append(line.strip())

    info_path = os.path.join(out_dir, '{}_info.csv'.format(prefix))
    with open(info_path, 'w') as f:
        f.write('ID,Tract Name,#HCP,#BLSA,#NORMAL,#ALL\n')
        i = 0
        for k in keys:
            if k in data:
                counts = data[k][1]
                tract = '_'.join(k.split('_')[1:]).replace('.nii.gz', '')
                tract = tract.replace('__labels__recognized_orig', '')
                tract = tract.replace('streamlines_moved_', '')
                f.write('{},{},{},{},{},{}\n'.format(i,tract,counts[0],counts[1],counts[2],np.sum(counts)))
                i+=1

    # all_out = os.path.join(out_dir, 'ALL')
    # if not os.path.isdir(all_out):
    #     os.mkdir(all_out)
    #
    # threads = []
    # for fname in data:
    #     out_path = os.path.join(all_out, fname)
    #     paths = data[fname][0]
    #     weights = np.array(data[fname][1])
    #     weights = weights/np.sum(weights)
    #     # weighted_average_vols(paths, out_path, weights)
    #     if not os.path.isfile(out_path):
    #         threads.append(Process(target=weighted_average_vols, args=(paths, out_path, weights)))
    #         threads[-1].start()
    #         if len(threads) == 4:
    #             for thread in threads:
    #                 thread.join()
    #             threads = []
    #
    # for thread in threads:
    #     thread.join()



# out_dir = '/nfs/masi/hansencb/t1_tract_data/AtlasesQA/TractSeg'
#
# create_atlases(out_dir, 'TractSegLinear')
# create_atlases(out_dir, 'TractSegNonlinear')
#
out_dir = '/nfs/masi/hansencb/t1_tract_data/AtlasesQA/RecoBundles'

create_atlases(out_dir, 'RecoBundlesLinear')
create_atlases(out_dir, 'RecoBundlesNonlinear')
#
# out_dir = '/nfs/masi/hansencb/t1_tract_data/AtlasesQA/Xtract'
#
# create_atlases(out_dir, 'XtractLinear')
# create_atlases(out_dir, 'XtractNonlinear')
#
# out_dir = '/nfs/masi/hansencb/t1_tract_data/AtlasesQA/Tracula'
#
# create_atlases(out_dir, 'TraculaLinear')
# create_atlases(out_dir, 'TraculaNonlinear')
#
# out_dir = '/nfs/masi/hansencb/t1_tract_data/AtlasesQA/AFQ'
#
# create_atlases(out_dir, 'AFQLinear')
# create_atlases(out_dir, 'AFQNonlinear')
#
# out_dir = '/nfs/masi/hansencb/t1_tract_data/AtlasesQA/AFQclipped'
#
# create_atlases(out_dir, 'AFQclippedLinear')
# create_atlases(out_dir, 'AFQclippedNonlinear')