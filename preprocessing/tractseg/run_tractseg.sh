#!/bin/bash

DWI_DIR_PATH=$1
OUTPUT_PATH=$2

tmp_dir=$(mktemp -d -t tractseg-XXXXXXXXX)
mkdir $tmp_dir/dwi
mkdir $tmp_dir/tractseg

scp hickory:$DWI_DIR_PATH/* $tmp_dir/dwi/

singularity exec --cleanenv --contain --home $SINGULARITY_HOME --bind $tmp_dir:/data docker://wasserth/tractseg_container:master TractSeg -i /data/dwi/Diffusion.nii.gz --raw_diffusion_input -o /data/tractseg

singularity exec --cleanenv --contain --home $SINGULARITY_HOME --bind $tmp_dir:/data docker://wasserth/tractseg_container:master TractSeg -i /data/tractseg/peak.nii.gz -o /data/tractseg --output_type endings_segmentation

singularity exec --cleanenv --contain --home $SINGULARITY_HOME --bind $tmp_dir:/data docker://wasserth/tractseg_container:master TractSeg -i /data/tractseg/peak.nii.gz -o /data/tractseg --output_type TOM

singularity exec --cleanenv --contain --home $SINGULARITY_HOME --bind $tmp_dir:/data docker://wasserth/tractseg_container:master Tracking -i /data/tractseg/peak.nii.gz -o /data/tractseg --tracking_format tck

scp -r $tmp_dir/tractseg/* hickory:$OUTPUT_PATH 
rm -rf $tmp_dir
