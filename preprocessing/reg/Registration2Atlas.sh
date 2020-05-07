#!/bin/bash

# Get inputs
B0_D_PATH=$1
T1_PATH=$2
T1_ATLAS_PATH=$3
RESULTS_PATH=$4

export FSLOUTPUTTYPE=NIFTI_GZ

#B0_D_PATH=/nfs/masi/hansencb/t1_tract_data/sample/BLSA_0270/BLSA_0270_25-0_10/dwi/B0.nii.gz
#T1_PATH=/nfs/masi/hansencb/t1_tract_data/sample/BLSA_0270/BLSA_0270_25-0_10/anat/
#T1_ATLAS_PATH=/nfs/masi/schilkg1/LearningWM/data/atlases/mni_icbm152_t1_tal_nlin_asym_09c.nii.gz
#RESULTS_PATH=/nfs/masi/hansencb/t1_tract_data/sample/BLSA_0270/BLSA_0270_25-0_10/reg/
#C3D_PATH=/home-local/schilkg1/c3d-1.1.0-Linux-gcc64/bin
#ANTMAN=/home-nfs/masi-shared-home/home/local/VANDERBILT/schilkg1/ANTS_13_FEB_2019/bin/ants/bin/

echo -------
echo INPUTS:
echo Distorted b0 path: $B0_D_PATH
echo T1 path: $T1_PATH
echo T1 atlas path: $T1_ATLAS_PATH
echo Results path: $RESULTS_PATH

# Create temporary job directory
JOB_PATH=$(mktemp -d)
echo -------
echo Job directory path: $JOB_PATH

# Make results directory
echo -------
echo Making results directory...
mkdir -p $RESULTS_PATH

# Skull strip T1
echo -------
echo Skull stripping T1
T1_MASK_PATH=$JOB_PATH/T1_mask.nii.gz
BET_CMD="bet $T1_PATH/T1.nii.gz $T1_MASK_PATH -f .4 -R -m"
echo $BET_CMD
eval $BET_CMD
# fsleyes $T1_MASK_PATH $T1_PATH/T1.nii.gz $JOB_PATH/T1_mask_mask.nii.gz 

# epi_reg distorted b0 to T1; wont be perfect since B0 is distorted
echo -------
echo epi_reg distorted b0 to T1
EPI_REG_D_PATH=$JOB_PATH/epi_reg_d
EPI_REG_D_MAT_PATH=$JOB_PATH/epi_reg_d.mat
EPI_REG_CMD="epi_reg --epi=$B0_D_PATH --t1=$T1_PATH/T1.nii.gz --t1brain=$T1_MASK_PATH --out=$EPI_REG_D_PATH"
echo $EPI_REG_CMD
eval $EPI_REG_CMD
# fsleyes $T1_MASK_PATH $T1_PATH/T1.nii.gz $EPI_REG_D_PATH

# Convert FSL transform to ANTS transform
echo -------
echo converting FSL transform to ANTS transform
EPI_REG_D_ANTS_PATH=$JOB_PATH/epi_reg_d_ANTS.txt
C3D_CMD="c3d_affine_tool -ref $T1_PATH/T1.nii.gz -src $B0_D_PATH $EPI_REG_D_MAT_PATH -fsl2ras -oitk $EPI_REG_D_ANTS_PATH"
echo $C3D_CMD
eval $C3D_CMD

# ANTs register T1 to atlas
echo -------
echo ANTS syn registration
ANTS_OUT=$JOB_PATH/ANTS
# ANTS_CMD="antsRegistrationSyNQuick.sh -d 3 -f $T1_ATLAS_PATH -m $T1_PATH -o $ANTS_OUT"
ANTS_CMD="antsRegistrationSyN.sh -d 3 -f $T1_ATLAS_PATH -m $T1_PATH/T1.nii.gz -o $ANTS_OUT"
echo $ANTS_CMD
eval $ANTS_CMD

# Apply linear transform to normalized T1 to get it into atlas space
echo -------
echo Apply linear transform to T1 NORM
T1_NORM_LIN_ATLAS_PATH=$JOB_PATH/T1_norm_lin_atlas.nii.gz
APPLYTRANSFORM_CMD="antsApplyTransforms -d 3 -i $T1_PATH/T1_NORM.nii.gz -r $T1_ATLAS_PATH -n BSpline -t "$ANTS_OUT"0GenericAffine.mat -o $T1_NORM_LIN_ATLAS_PATH"
echo $APPLYTRANSFORM_CMD
eval $APPLYTRANSFORM_CMD
echo -------
echo Apply linear transform to T1 N3
T1_N3_LIN_ATLAS_PATH=$JOB_PATH/T1_N3_lin_atlas.nii.gz
APPLYTRANSFORM_CMD="antsApplyTransforms -d 3 -i $T1_PATH/T1_N3.nii.gz -r $T1_ATLAS_PATH -n BSpline -t "$ANTS_OUT"0GenericAffine.mat -o $T1_N3_LIN_ATLAS_PATH"
echo $APPLYTRANSFORM_CMD
eval $APPLYTRANSFORM_CMD
# fsleyes $T1_ATLAS_PATH $T1_NORM_LIN_ATLAS_PATH

# Apply linear transform to distorted b0 to get it into atlas space
echo -------
echo Apply linear transform to distorted b0
B0_D_LIN_ATLAS_PATH=$JOB_PATH/b0_lin_atlas.nii.gz
APPLYTRANSFORM_CMD="antsApplyTransforms -d 3 -i $B0_D_PATH -r $T1_ATLAS_PATH -n BSpline -t "$ANTS_OUT"0GenericAffine.mat -t $EPI_REG_D_ANTS_PATH -o $B0_D_LIN_ATLAS_PATH"
echo $APPLYTRANSFORM_CMD
eval $APPLYTRANSFORM_CMD
# fsleyes $T1_ATLAS_PATH $T1_NORM_LIN_ATLAS_PATH $B0_D_LIN_ATLAS_PATH

# Apply nonlinear transform to normalized T1 to get it into atlas space
echo -------
echo Apply nonlinear transform to T1 NORM
T1_NORM_NONLIN_ATLAS_PATH=$JOB_PATH/T1_norm_nonlin_atlas.nii.gz
APPLYTRANSFORM_CMD="antsApplyTransforms -d 3 -i $T1_PATH/T1_NORM.nii.gz -r $T1_ATLAS_PATH -n BSpline -t "$ANTS_OUT"1Warp.nii.gz -t "$ANTS_OUT"0GenericAffine.mat -o $T1_NORM_NONLIN_ATLAS_PATH"
echo $APPLYTRANSFORM_CMD
eval $APPLYTRANSFORM_CMD
echo -------
echo Apply nonlinear transform to T1 N3
T1_N3_NONLIN_ATLAS_PATH=$JOB_PATH/T1_N3_nonlin_atlas.nii.gz
APPLYTRANSFORM_CMD="antsApplyTransforms -d 3 -i $T1_PATH/T1_N3.nii.gz -r $T1_ATLAS_PATH -n BSpline -t "$ANTS_OUT"1Warp.nii.gz -t "$ANTS_OUT"0GenericAffine.mat -o $T1_N3_NONLIN_ATLAS_PATH"
echo $APPLYTRANSFORM_CMD
eval $APPLYTRANSFORM_CMD
# fsleyes $T1_ATLAS_PATH $T1_NORM_NONLIN_ATLAS_PATH

# Apply nonlinear transform to distorted b0 to get it into atlas space
echo -------
echo Apply nonlinear transform to distorted b0
B0_D_NONLIN_ATLAS_PATH=$JOB_PATH/b0_nonlin_atlas.nii.gz
APPLYTRANSFORM_CMD="antsApplyTransforms -d 3 -i $B0_D_PATH -r $T1_ATLAS_PATH -n BSpline -t "$ANTS_OUT"1Warp.nii.gz -t "$ANTS_OUT"0GenericAffine.mat -t $EPI_REG_D_ANTS_PATH -o $B0_D_NONLIN_ATLAS_PATH"
echo $APPLYTRANSFORM_CMD
eval $APPLYTRANSFORM_CMD
# fsleyes $T1_ATLAS_PATH $T1_NORM_NONLIN_ATLAS_PATH $B0_D_NONLIN_ATLAS_PATH

# Copy what you want to results path
echo -------
echo Copying results to results path...
cp $T1_PATH/T1_NORM.nii.gz $RESULTS_PATH
cp $T1_MASK_PATH $RESULTS_PATH
cp $EPI_REG_D_MAT_PATH $RESULTS_PATH
cp $EPI_REG_D_ANTS_PATH $RESULTS_PATH
cp "$ANTS_OUT"0GenericAffine.mat $RESULTS_PATH
cp "$ANTS_OUT"1Warp.nii.gz $RESULTS_PATH
cp "$ANTS_OUT"1InverseWarp.nii.gz $RESULTS_PATH
cp $T1_NORM_LIN_ATLAS_PATH $RESULTS_PATH
cp $T1_NORM_NONLIN_ATLAS_PATH $RESULTS_PATH
cp $T1_N3_LIN_ATLAS_PATH $RESULTS_PATH
cp $T1_N3_NONLIN_ATLAS_PATH $RESULTS_PATH
cp $B0_D_LIN_ATLAS_PATH $RESULTS_PATH
cp $B0_D_NONLIN_ATLAS_PATH $RESULTS_PATH

# Delete job directory
echo -------
echo Removing job directory...
rm -rf $JOB_PATH
