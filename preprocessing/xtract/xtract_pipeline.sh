#!/bin/bash

SUBJ_PATH=$1
B0_PATH=$SUBJ_PATH/dwi/b0.nii.gz
BEDPOST_PATH=$SUBJ_PATH/derivatives/bedpostx
REG_SINGULARITY=/scratch/hansencb/tract_preprocessing/reg/reg.simg
ANTS_AFFINE=$SUBJ_PATH/reg/ANTS0GenericAffine.mat
ANTS_WARP=$SUBJ_PATH/reg/ANTS1InverseWarp.nii.gz
EPI_REG=$SUBJ_PATH/reg/epi_reg_d_ANTS.txt
STRUCTURE_FILE=/scratch/hansencb/tract_preprocessing/xtract/structureList
PROTOCOLS=/scratch/hansencb/tract_preprocessing/xtract/protocols
SINGULARITY=/scratch/hansencb/tract_preprocessing/fsl_601.simg
EYE=/scratch/hansencb/tract_preprocessing/xtract/eye.mat

tmp_dir=$(mktemp -d -t xtract-XXXXXXXX)
mkdir $tmp_dir/INPUTS
mkdir $tmp_dir/OUTPUTS

scp hickory:$ANTS_AFFINE $tmp_dir
scp hickory:$ANTS_WARP $tmp_dir
scp hickory:$EPI_REG $tmp_dir
scp hickory:$B0_PATH $tmp_dir/INPUTS/b0.nii.gz
scp -r hickory:$BEDPOST_PATH $tmp_dir/INPUTS/bedpostx

cp $STRUCTURE_FILE $tmp_dir/INPUTS/
cp $EYE $tmp_dir/INPUTS/
cp -r $PROTOCOLS $tmp_dir/INPUTS/protocols
for seed in $tmp_dir/INPUTS/protocols/*/*.nii.gz do
    antsApplyTransforms -d 3 -i $seed -r $tmp_dir/INPUTS/b0.nii.gz -t [$tmp_dir/epi_reg_d_ANTS.txt,1] -t [$tmp_dir/ANTS0GenericAffine.mat,1] -t $tmp_dir/ANTS1InverseWarp.nii.gz -o $seed
    fslcpgeom $tmp_dir/INPUTS/b0.nii.gz $seed
done

singularity exec --nv -B $tmp_dir/INPUTS:/INPUTS -B $tmp_dir/OUTPUTS:/OUTPUTS $SINGULARITY /extra/xtract_run.sh
mv $tmp_dir/OUTPUTS $tmp_dir/xtract
scp -r $tmp_dir/xtract hickory:$SUBJ_PATH/derivatives/
scp $tmp_dir/INPUTS/bedpostx/xfms/diff2standard hickory:$BEDPOST_PATH/xfms/
scp $tmp_dir/INPUTS/bedpostx/xfms/standard2diff hickory:$BEDPOST_PATH/xfms/
rm -rf $tmp_dir

