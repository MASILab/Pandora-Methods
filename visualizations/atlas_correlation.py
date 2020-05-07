import nibabel as nib
import numpy as np
import os
import glob
import scipy.spatial.distance as scidist
from multiprocessing import Process

def cross_corr(path1, path2, out_path):
    density_1 = nib.load(path1).get_fdata()
    density_2 = nib.load(path2).get_fdata()
    
    indices = np.where(density_1 + density_2 > 0)
    if np.array_equal(density_1, density_2):
        density_correlation = 1
    elif (np.sum(density_1) > 0 and np.sum(density_2) > 0) \
            and np.count_nonzero(density_1 * density_2):
        density_correlation = np.corrcoef(density_1[indices],
                                          density_2[indices])[0, 1]
    else:
        density_correlation = 0

    with open(out_path, 'w') as f:
        f.write('{}'.format(max(0, density_correlation)))

out_dir = 'tract_correlation'
proj_dir = '/nfs/masi/hansencb/t1_tract_data/Atlases'
atlas_dirs = ['AFQAtlases', 'AFQclippedAtlases', 'RecobundlesAtlases',
              'TractSegAtlases', 'TraculaAtlases', 'XtractAtlases']

os.makedirs(out_dir, exist_ok=True)

with open('wm_atlas_tract_paths.txt', 'r') as f:
    paths = [x.strip() for x in f.readlines()]

threads = []
for i in range(len(paths)):
    for j in range(i,len(paths)):
        out_path = os.path.join(out_dir, 'cc_{}_{}.txt'.format(i,j))
        if not os.path.isfile(out_path):
            threads.append(Process(target=cross_corr, args=(paths[i], paths[j], out_path,)))
            threads[-1].start()

        if len(threads) > 7:
            for thread in threads:
                thread.join()
            threads = []

for thread in threads:
    thread.join()
threads = []


with open('across_data_dice_paths.txt', 'r') as f:
   groups = [x.strip() for x in f.readlines()]

threads = []

out_dir = 'across_data_correlation'
os.makedirs(out_dir, exist_ok=True)

datasets = ['ALL', 'HCP', 'BLSA', 'NORMAL']
for group in groups:
   paths = group.split(',')
   tract = paths[0].split('/')[-1][0:-7]
   for i in range(len(paths)):
       for j in range(i,len(paths)):

           out_path = os.path.join(out_dir, 'cc_{}_{}_{}.txt'.format(datasets[i],datasets[j], tract))
           if not os.path.isfile(out_path):
               threads.append(Process(target=cross_corr, args=(paths[i], paths[j], out_path,)))
               threads[-1].start()

           if len(threads) > 7:
               for thread in threads:
                   thread.join()
               threads = []

for thread in threads:
   thread.join()
threads = []
