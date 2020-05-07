import nibabel as nib
import numpy as np
import os
import glob
import scipy.spatial.distance as scidist
from multiprocessing import Process

def dice(path1, path2, out_path):
    A = nib.load(path1).get_fdata().flatten()
    B = nib.load(path2).get_fdata().flatten()

    A[A < 0.5] = 0
    A[A >= 0.5] = 1

    B[B < 0.5] = 0
    B[B >= 0.5] = 1

    DC = 1-scidist.dice(A,B)

    with open(out_path, 'w') as f:
        f.write('{}'.format(DC))


def cont_dice(path1, path2, out_path):
    A = nib.load(path1).get_fdata().flatten()
    B = nib.load(path2).get_fdata().flatten()

    A = np.array([1, 0, 0, 1])
    B = np.array([0.1, 0, 0, 0.1])
    size_intersect = np.sum(A*B)
    size_a = np.sum(A)
    size_b = np.sum(B)

    if (size_intersect > 0):
        c = size_intersect/np.sum(A*np.sign(B))
    else:
        c = 1

    cDC = (2*size_intersect)/(c*size_a+size_b)
    print(cDC)
    with open(out_path, 'w') as f:
        f.write('{}'.format(cDC))



out_dir = 'across_data_dice_scores'
proj_dir = '/nfs/masi/hansencb/t1_tract_data/Atlases'
atlas_dirs = ['AFQcleanAtlases', 'AFQclippedAtlases', 'RecobundlesAtlases',
              'TractSegAtlases', 'TraculaAtlases', 'XtractAtlases']

# paths = []
# for atlas_dir in atlas_dirs:
#     names = glob.glob(os.path.join(proj_dir, atlas_dir, 'ALL', '*Nonlinear*.nii.gz'))
#     for name in names:
#         paths.append(os.path.join(proj_dir, atlas_dir, 'ALL', name))
#
# with open('wm_atlas_tract_paths.txt', 'w') as f:
#     f.write('\n'.join(paths))

# with open('across_data_dice_paths.txt', 'w') as f:
#     for atlas_dir in atlas_dirs:
#         names = glob.glob(os.path.join(proj_dir, atlas_dir, 'ALL', '*Nonlinear*.nii.gz'))
#         for name in names:
#             name = name.split('/')[-1]
#             f.write('{},{},{},{}\n'.format(os.path.join(proj_dir, atlas_dir, 'ALL', name),
#                                         os.path.join(proj_dir, atlas_dir, 'HCP', name),
#                                         os.path.join(proj_dir, atlas_dir, 'BLSA', name),
#                                         os.path.join(proj_dir, atlas_dir, 'NORMAL', name)))


# with open('wm_atlas_tract_paths.txt', 'r') as f:
#     paths = [x.strip() for x in f.readlines()]
#
# threads = []
# for i in range(len(paths)):
#     for j in range(i,len(paths)):
#         out_path = os.path.join(out_dir, 'dice_{}_{}.txt'.format(i,j))
#         # dice(paths[i], paths[j], out_path)
#         if not os.path.isfile(out_path):
#             threads.append(Process(target=dice, args=(paths[i], paths[j], out_path,)))
#             threads[-1].start()
#
#         # out_path = os.path.join(out_dir, 'contdice_{}_{}.txt'.format(i,j))
#         # cont_dice(paths[i], paths[j], out_path)
#         # threads.append(Process(target=cont_dice, args=(paths[i], paths[j], out_path,)))
#         # threads[-1].start()
#         #
#         if len(threads) > 15:
#             for thread in threads:
#                 thread.join()
#             threads = []
#
# for thread in threads:
#     thread.join()
# threads = []

with open('across_data_dice_paths.txt', 'r') as f:
    groups = [x.strip() for x in f.readlines()]

threads = []

datasets = ['ALL', 'HCP', 'BLSA', 'NORMAL']
for group in groups:
    paths = group.split(',')
    tract = paths[0].split('/')[-1][0:-7]
    for i in range(len(paths)):
        for j in range(i,len(paths)):

            out_path = os.path.join(out_dir, 'dice_{}_{}_{}.txt'.format(datasets[i],datasets[j], tract))
            # dice(paths[i], paths[j], out_path)
            if not os.path.isfile(out_path):
                threads.append(Process(target=dice, args=(paths[i], paths[j], out_path,)))
                threads[-1].start()

            # out_path = os.path.join(out_dir, 'contdice_{}_{}.txt'.format(i,j))
            # cont_dice(paths[i], paths[j], out_path)
            # threads.append(Process(target=cont_dice, args=(paths[i], paths[j], out_path,)))
            # threads[-1].start()
            #
            if len(threads) > 7:
                for thread in threads:
                    thread.join()
                threads = []

for thread in threads:
    thread.join()
threads = []