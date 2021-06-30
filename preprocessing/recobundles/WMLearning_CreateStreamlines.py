#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tempfile
import fire
import subprocess 
import shutil
import os
from os import path as osp
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt 
from fury import actor, window, ui 
from time import time
from pathlib import Path

import dipy
import dipy.data as dpd
import dipy.direction.peaks as dpp
import dipy.reconst.dti as dti 
from dipy.io.image import load_nifti, save_nifti
from dipy.io import read_bvals_bvecs
from dipy.core.gradients import gradient_table
from dipy.reconst.dti import TensorModel
from dipy.io.streamline import load_trk, save_trk
from dipy.segment.mask import median_otsu
from dipy.reconst.csdeconv import auto_response, ConstrainedSphericalDeconvModel
from dipy.direction import peaks_from_model
from dipy.tracking.local_tracking import LocalTracking
from dipy.tracking.utils import seeds_from_mask, random_seeds_from_mask
from dipy.tracking.streamline import Streamlines
from dipy.tracking import utils
from dipy.io.streamline import save_trk
from dipy.io.stateful_tractogram import Space, StatefulTractogram
from dipy.data import read_isbi2013_2shell
from dipy.io.stateful_tractogram import Space, StatefulTractogram
from dipy.io.streamline import load_trk, save_trk, load_tractogram, save_tractogram
from dipy.tracking.streamline import compress_streamlines
from dipy.tracking.stopping_criterion import (ActStoppingCriterion,
                                              BinaryStoppingCriterion,
                                              ThresholdStoppingCriterion) 

def create_streamlines(data_dir_path, raw_data_path, mni_template,seed_counts=1000000,use_tmp_dir=True):
    print('seed_counts: ' + str(seed_counts))
    seed_counts = int(seed_counts)

    data_dir_path = Path(data_dir_path)
    raw_dir_path = Path(raw_data_path)
    template_path = Path(mni_template)

    file=(raw_dir_path/'dwmri.nii.gz').as_posix()
    bvalue=(raw_dir_path/'dwmri.bval').as_posix()
    bvector=(raw_dir_path/'dwmri.bvec').as_posix()
    
    ##### SCHILLING CHANGES ##########
    trk2tdi=dipy.TrackDensityMap()
    trk2tdi.inputs.reference=file
    ##################################

    # Create recobundles derivatives path
    derivatives_dir_path = data_dir_path/'TRACTOGRAPHY-recobundles'
    derivatives_dir_path.mkdir(parents=True, exist_ok=True)

    # Create job directory
    if use_tmp_dir:
        job_dir_path = Path(tempfile.mkdtemp())
    else:
        job_dir_path = Path((derivatives_dir_path/'working').as_posix())
        if not osp.exists(job_dir_path):
            os.makedirs(job_dir_path)
    print('Job directory: ' + job_dir_path.as_posix())

    # Load nifti
    nii = nib.load(file)

    # Make sure nifti is isotropic; if not, make it isotropic
    pixdim = nii.header['pixdim'][1:4]
    if np.unique(pixdim).size != 1:
        print('Not isotropic! Making it isotropic...')
        pix_res = pixdim.max()
        new_file = (derivatives_dir_path/'Diffusion.nii.gz').as_posix()
        flirt_cmd = 'flirt -in ' + file + ' -ref ' + file + ' -applyisoxfm ' + str(pix_res) + ' -out ' + new_file
        print('Running: ' + flirt_cmd)
        subprocess.check_call(flirt_cmd, shell=True)

        # Set new path
        file = new_file

        # re-load nifti
        nii = nib.load(file)

    # LOAD DATA
    data, affine = load_nifti(file)

    bvals, bvecs = read_bvals_bvecs(bvalue, bvector)

    # Get b0 and highest bval shell
    bval_idx = np.logical_or(bvals < 50, bvals > (bvals.max() - 100))

    print('Selecting indices: ' + str(np.transpose(np.argwhere(bval_idx))))

    data = data[:, :, :, bval_idx]
    bvecs = bvecs[bval_idx, :]
    bvals = bvals[bval_idx]

    gtab = gradient_table(bvals, bvecs)

    img = nib.load(file)
    volume= data.shape[:3]
    voxel= img.header.get_zooms()[:3]

    # Brain extraction using Median Ostu
    sphere = dpd.get_sphere('repulsion724')

    # Create mask
    mask_path = derivatives_dir_path/'mask.nii.gz'
    bet_cmd = 'bet ' + file + ' ' + mask_path.as_posix() + ' -R -m -f 0.2'
    print('Running: ' + bet_cmd)
    subprocess.check_call(bet_cmd, shell=True)

    # Load mask
    mask_mask_path = derivatives_dir_path/'mask_mask.nii.gz'
    mask, _ = load_nifti(mask_mask_path.as_posix())
    # mask = mask[:, :, :, 0] # Leon editing mask to be 3D instead of 4D ***

    print(subprocess.check_output('which bet', shell=True))
    print(data.shape)
    print(mask.shape)

    # Tensor Model
    print('Started DTI processing ...')
    tenmodel = TensorModel(gtab)
    tenfit = tenmodel.fit(data, mask=mask)
    print('Finished DTI processing ...')

    # CSD
    print('Started CSD')
    response, ratio = auto_response(gtab, data, roi_radius=10, fa_thr=0.7)
    print('Finished response')
    csd_model = ConstrainedSphericalDeconvModel(gtab, response)
    csd_peaks = peaks_from_model(model=csd_model,
                                 data=data,
                                 sphere=sphere,
                                 mask=mask,
                                 relative_peak_threshold=.5,
                                 min_separation_angle=25,
                                 parallel=True,
                                 normalize_peaks=True)

    # Generating streamlines
    threshold_criterion = ThresholdStoppingCriterion(tenfit.fa, .2)

    # higher the number of seeds, higher the number of generated streamlines
    seeds = random_seeds_from_mask(tenfit.fa > 0.3, seeds_count=seed_counts,seed_count_per_voxel=False, affine=np.eye(4))

    streamline_generator = LocalTracking(csd_peaks, threshold_criterion,
                                         seeds, affine=np.eye(4),
                                         step_size=0.5, return_all=True)

    streamlines = Streamlines(streamline_generator)

    print(len(streamlines))

    streamlines = compress_streamlines(streamlines, tol_error=0.2)

    streamlines_path = job_dir_path/'streamlines.trk'
    sft = StatefulTractogram(streamlines, nii, Space.VOX)
    save_trk(sft, streamlines_path.as_posix(), streamlines)

    dipy_slr_cmd = 'dipy_slr "' + (template_path/'whole_brain_MNI.trk').as_posix() + '" "' + streamlines_path.as_posix() + '" --out_dir ' + job_dir_path.as_posix()
    print('Running: ' + dipy_slr_cmd)
    subprocess.check_call(dipy_slr_cmd, shell=True)

    dipy_rb_cmd = 'dipy_recobundles "' + (job_dir_path/'moved.trk').as_posix() + '" "' + (template_path/'bundles'/'*.trk').as_posix() + '" --force --mix_names --refine --out_dir ' + job_dir_path.as_posix()
    print('Running: ' + dipy_rb_cmd)
    subprocess.check_call(dipy_rb_cmd, shell=True)

    # LEON DEBUGGING ***
    debug_str = '*** DEBUGGING ***'

    for f_trk in job_dir_path.glob('*.npy'):
        try:
            dipy_lb_cmd = 'dipy_labelsbundles "' + streamlines_path.as_posix() + '" "' + f_trk.as_posix() + '" --force --mix_names --out_dir ' + job_dir_path.as_posix()
            print('Running: ' + dipy_lb_cmd)
            subprocess.check_call(dipy_lb_cmd, shell=True)
            # LEON DEBUGGING ***
            ok_str = '*** seed_counts = ' + str(seed_counts) + ', ok with input ' + str(f_trk.as_posix()) + ' (' + str(os.path.getsize(f_trk.as_posix())) + ' bytes)'
            print(ok_str)
            debug_str = debug_str + '\n' + ok_str
        except:
            # LEON DEBUGGING ***
            err_str = '*** seed_counts = ' + str(seed_counts) + ', error with input ' + str(f_trk.as_posix()) + ' (' + str(os.path.getsize(f_trk.as_posix())) + ' bytes)'
            print(err_str)
            debug_str = debug_str + '\n' + err_str
            pass

    for f_trk in job_dir_path.glob('*recognized_orig.trk'):
        try:
            input_tractogram = nib.streamlines.load(f_trk.as_posix())
            trk2tdi = dipy.tracking.utils.density_map(streamlines=input_tractogram.streamlines, affine=affine, vol_dims=data.shape[:3])
            save_nifti(fname=(derivatives_dir_path/(f_trk.stem + '.nii.gz')).as_posix(), data=trk2tdi, affine=affine)
            trk2tdi.inputs.in_file=f_trk.as_posix()
            trk2tdi.inputs.out_filename=(derivatives_dir_path/(f_trk.stem + '.nii.gz')).as_posix()
            trk2tdi.run()
            
        except:
            pass


    if use_tmp_dir:
        print('Removing job directory...')
        shutil.rmtree(job_dir_path)
    print(debug_str)
    return 0

if __name__ == '__main__':
    fire.Fire(create_streamlines)
