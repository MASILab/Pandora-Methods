#!/bin/bash

SUBJ_PATH=$1
B0_PATH=$SUBJ_PATH/dwi/b0.nii.gz
BEDPOST_PATH=$SUBJ_PATH/derivatives/bedpostx
ANTS_AFFINE=$SUBJ_PATH/reg/ANTS0GenericAffine.mat
ANTS_WARP=$SUBJ_PATH/reg/ANTS1InverseWarp.nii.gz
EPI_REG=$SUBJ_PATH/reg/epi_reg_d_ANTS.txt
STRUCTURE_FILE=/nfs/masi/hansencb/t1_tract_data/preprocessing/xtract/structureList
PROTOCOLS=/nfs/masi/hansencb/t1_tract_data/preprocessing/xtract/protocols
SINGULARITY=/nfs/masi/hansencb/t1_tract_data/preprocessing/fsl_601.simg
EYE=/nfs/masi/hansencb/t1_tract_data/preprocessing/xtract/eye.mat

tmp_dir=$(mktemp -d -t xtract-XXXXXXXX)
mkdir $tmp_dir/INPUTS
mkdir $tmp_dir/OUTPUTS

cp $ANTS_AFFINE $tmp_dir
cp $ANTS_WARP $tmp_dir
cp $EPI_REG $tmp_dir

#convert_xfm -omat $tmp_dir/INPUTS/epi_reg_inv_d.mat -inverse $tmp_dir/INPUTS/epi_reg_d.mat

cp $B0_PATH $tmp_dir/INPUTS/b0.nii.gz
cp -r $BEDPOST_PATH $tmp_dir/INPUTS/bedpostx
cp $SUBJ_PATH/anat/T1.nii.gz $tmp_dir/

cp $STRUCTURE_FILE $tmp_dir/INPUTS/
cp $EYE $tmp_dir/INPUTS/
cp -r $PROTOCOLS $tmp_dir/INPUTS/protocols
for seed in $tmp_dir/INPUTS/protocols/*/*.nii.gz 
do
    antsApplyTransforms -d 3 -i $seed -r $tmp_dir/INPUTS/b0.nii.gz -t [$tmp_dir/epi_reg_d_ANTS.txt,1] -t [$tmp_dir/ANTS0GenericAffine.mat,1] -t $tmp_dir/ANTS1InverseWarp.nii.gz -o $seed
    fslcpgeom $tmp_dir/INPUTS/b0.nii.gz $seed
done

singularity exec --nv -B $tmp_dir/INPUTS:/INPUTS -B $tmp_dir/OUTPUTS:/OUTPUTS $SINGULARITY /extra/xtract_run.sh
mv $tmp_dir/OUTPUTS $tmp_dir/xtract
cp -r $tmp_dir/xtract $SUBJ_PATH/derivatives/
cp $tmp_dir/INPUTS/bedpostx/xfms/diff2standard $BEDPOST_PATH/xfms/
cp $tmp_dir/INPUTS/bedpostx/xfms/standard2diff $BEDPOST_PATH/xfms/
