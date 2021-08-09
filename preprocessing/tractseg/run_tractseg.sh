#!/bin/bash

#module load GCC/5.4.0-2.26  OpenMPI/1.10.3 FSL/5.0.10

DWI_DIR_PATH=$1
OUTPUT_PATH=$2

tmp_dir=$(mktemp -d -t tractseg-XXXXXXXXX)
mkdir $tmp_dir/dwi
mkdir $tmp_dir/tractseg

scp hickory:$DWI_DIR_PATH/* $tmp_dir/dwi/
#fslroi $tmp_dir/dwi/Diffusion.nii.gz $tmp_dir/dwi/b0.nii.gz 0 1
#bet $tmp_dir/dwi/b0.nii.gz $tmp_dir/dwi/nodif_brain_mask.nii.gz -m

singularity run  -B $tmp_dir:/data /scratch/hansencb/tract_preprocessing/tractseg/tractseg.sif TractSeg -i /data/dwi/Diffusion.nii.gz --raw_diffusion_input -o /data/tractseg

singularity run  -B $tmp_dir:/data /scratch/hansencb/tract_preprocessing/tractseg/tractseg.sif TractSeg -i /data/tractseg/peaks.nii.gz -o /data/tractseg --output_type endings_segmentation

singularity run  -B $tmp_dir:/data /scratch/hansencb/tract_preprocessing/tractseg/tractseg.sif TractSeg -i /data/tractseg/peaks.nii.gz -o /data/tractseg --output_type TOM

singularity run  -B $tmp_dir:/data /scratch/hansencb/tract_preprocessing/tractseg/tractseg.sif Tracking -i /data/tractseg/peaks.nii.gz -o /data/tractseg --tracking_format tck

scp -r $tmp_dir/tractseg hickory:$OUTPUT_PATH
rm -rf $tmp_dir
