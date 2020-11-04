import torch
import numpy as np
import nibabel as nib
import os
from tqdm import tqdm
from multiprocessing import Process


def weighted_average_vols(paths, out_path, thresh, weights):
    avg = None
    init = True

    with tqdm(total=len(paths)) as pbar:
        for i, path in enumerate(paths):
            vol = nib.load(path).get_fdata()
            # vol[vol<thresh] = 0
            # vol[vol>=thresh] = 1
            if init:
                avg = vol * weights[i]
                init = False
            else:
                avg = avg + (vol * weights[i])
            pbar.update(1)

    nft = nib.Nifti1Image(avg, nib.load(paths[0]).affine, nib.load(paths[0]).header)
    nib.save(nft, out_path)

def average_vols(paths, out_path, thresh):
    total = None
    init = True

    with tqdm(total=len(paths)) as pbar:
        for i, path in enumerate(paths):
            vol = nib.load(path).get_fdata()
            vol[vol<thresh] = 0
            vol[vol>=thresh] = 1
            if init:
                total = vol
                init = False
            else:
                total = total + vol
            pbar.update(1)

    avg = total/len(paths)
    nft = nib.Nifti1Image(avg, nib.load(paths[0]).affine, nib.load(paths[0]).header)
    nib.save(nft, out_path)

def create_atlases(in_dir, out_dir, prefix, thresh):
    data = {}

    for sess in os.listdir(in_dir):
        if not sess.endswith('.bad'):
            parts = sess.split('_')
            proj = parts[0]
            if parts[1] == 'Morgan' or parts[1] == 'Cutting':
                subj = '_'.join(parts[1:5])
            elif parts[1] == 'Taylor':
                subj = '_'.join(parts[1:4])
            else:
                subj = parts[1]

            if proj not in data:
                data[proj] = {}

            sess_dir = os.path.join(in_dir, sess)

            for vol in os.listdir(sess_dir):
                if not vol.endswith('.bad'):
                    path = os.path.join(sess_dir, vol)

                    if vol not in data[proj]:
                        data[proj][vol] = [[], []]

                    if subj not in data[proj][vol][1]:
                        data[proj][vol][1].append(subj)
                        data[proj][vol][0].append(path)

    threads = []
    for project in data:
        proj_out = os.path.join(out_dir, project)
        if not os.path.isdir(proj_out):
            os.mkdir(proj_out)
        for label in data[project]:
            paths = data[project][label][0]
            out_path = os.path.join(proj_out, '{}_{}'.format(prefix, label))
            if not os.path.isfile(out_path):
                print('Creating {} atlas'.format(label[0:-7]))
                # average_vols(paths, out_path, thresh)
                threads.append(Process(target=average_vols, args=(paths, out_path, thresh,)))
                threads[-1].start()

                if len(threads) == 8:
                    for thread in threads:
                        thread.join()
                    threads = []

    for thread in threads:
        thread.join()
        threads = []

    all_out = os.path.join(out_dir, 'ALL')
    if not os.path.isdir(all_out):
        os.mkdir(all_out)

    for label in data[list(data.keys())[0]]:
        paths = []
        weights = []
        for project in data:
            proj_out = os.path.join(out_dir, project)
            paths.append(os.path.join(proj_out, '{}_{}'.format(prefix, label)))
            weights.append(len(data[project][label][0]))
        weights = np.array(weights)
        total = np.sum(weights)
        weights = weights / total
        out_path = os.path.join(all_out, '{}_{}'.format(prefix, label))
        # weighted_average_vols(paths, out_path, thresh, weights)
        if not os.path.isfile(out_path):
            threads.append(Process(target=weighted_average_vols, args=(paths, out_path, thresh, weights)))
            threads[-1].start()
            if len(threads) == 8:
                for thread in threads:
                    thread.join()
                threads = []

    for thread in threads:
        thread.join()


# out_dir = '/nfs/masi/hansencb/t1_tract_data/Atlases/TractSegAtlases'
# lin_dir = '/nfs/masi/hansencb/t1_tract_data/registered_data/TractSegLinear'
# nonlin_dir = '/nfs/masi/hansencb/t1_tract_data/registered_data/TractSegNonlinear'
#
# if not os.path.isdir(out_dir):
#     os.mkdir(out_dir)
#
# create_atlases(lin_dir, out_dir, 'TractSegLinear', 0.5)
# create_atlases(nonlin_dir, out_dir, 'TractSegNonlinear', 0.5)
#
# out_dir = '/nfs/masi/hansencb/t1_tract_data/Atlases/RecobundlesAtlases'
# lin_dir = '/nfs/masi/hansencb/t1_tract_data/registered_data/RecobundlesLinear'
# nonlin_dir = '/nfs/masi/hansencb/t1_tract_data/registered_data/RecobundlesNonlinear'
#
# if not os.path.isdir(out_dir):
#     os.mkdir(out_dir)
#
# create_atlases(lin_dir, out_dir, 'RecobundlesLinear', 0.5)
# create_atlases(nonlin_dir, out_dir, 'RecobundlesNonlinear', 0.5)
#
# out_dir = '/nfs/masi/hansencb/t1_tract_data/Atlases/XtractAtlases'
# lin_dir = '/nfs/masi/hansencb/t1_tract_data/registered_data/XtractLinear'
# nonlin_dir = '/nfs/masi/hansencb/t1_tract_data/registered_data/XtractNonlinear'
#
# if not os.path.isdir(out_dir):
#     os.mkdir(out_dir)
#
# create_atlases(lin_dir, out_dir, 'XtractLinear', 0.001)
# create_atlases(nonlin_dir, out_dir, 'XtractNonlinear', 0.001)
#
# out_dir = '/nfs/masi/hansencb/t1_tract_data/Atlases/TraculaAtlases'
# lin_dir = '/nfs/masi/hansencb/t1_tract_data/registered_data/TraculaLinear'
# nonlin_dir = '/nfs/masi/hansencb/t1_tract_data/registered_data/TraculaNonlinear'
#
# if not os.path.isdir(out_dir):
#     os.mkdir(out_dir)
#
# create_atlases(lin_dir, out_dir, 'TraculaLinear', 0.5)
# create_atlases(nonlin_dir, out_dir, 'TraculaNonlinear', 0.5)

out_dir = '/nfs/masi/hansencb/t1_tract_data/AtlasesQA/AFQAtlases'
lin_dir = '/nfs/masi/hansencb/t1_tract_data/registered_data/AFQcleanLinear'
nonlin_dir = '/nfs/masi/hansencb/t1_tract_data/registered_data/AFQcleanNonlinear'

if not os.path.isdir(out_dir):
    os.mkdir(out_dir)

create_atlases(lin_dir, out_dir, 'AFQLinear', 0.5)
create_atlases(nonlin_dir, out_dir, 'AFQNonlinear', 0.5)

# out_dir = '/nfs/masi/hansencb/t1_tract_data/AtlasesQA/AFQclippedAtlases'
# lin_dir = '/nfs/masi/hansencb/t1_tract_data/registered_data/AFQclippedLinear'
# nonlin_dir = '/nfs/masi/hansencb/t1_tract_data/registered_data/AFQclippedNonlinear'
#
# if not os.path.isdir(out_dir):
#     os.mkdir(out_dir)
#
# create_atlases(lin_dir, out_dir, 'AFQclippedLinear', 0.5)
# create_atlases(nonlin_dir, out_dir, 'AFQclippedNonlinear', 0.5)