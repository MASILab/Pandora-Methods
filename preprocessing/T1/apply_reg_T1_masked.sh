#!/bin/bash
# prepare TractSeg atlas 1mm iso
# within TractSeg atlas folder, there is linear and nonlinear
# for each subject, create folder, move to atlas space

DATA=$1
SUB=$2
SCAN=$3
#DATA=BLSA
#SUB=0359
#SCAN=BLSA_0359_25-0_08

# Directories
MAIN=/nfs/masi/hansencb/t1_tract_data

###########################################
################# LINEAR ##################
###########################################

OUTPUTDIR="$MAIN"/registered_data/T1_Linear/"$DATA"_"$SUB"_"$SCAN"
REFERENCE=/nfs/masi/schilkg1/LearningWM/data/atlases/mni_icbm152_t1_tal_nlin_asym_09c.nii.gz

# make INPUT/OUTPUT Directories
mkdir -p $OUTPUTDIR


# into OUTPUTDIR move each streamline from b0 to T1 and T1 to atlas linearly
ANTS_T12Atlas="$MAIN"/raw_data/"$DATA"/"$SUB"/"$SCAN"/reg/ANTS0GenericAffine.mat
ANTS_b02T1="$MAIN"/raw_data/"$DATA"/"$SUB"/"$SCAN"/reg/epi_reg_d_ANTS.txt
T1_PATH="$MAIN"/raw_data/"$DATA"/"$SUB"/"$SCAN"/reg/T1_mask.nii.gz

OUTPUT_NAME="$OUTPUTDIR"/T1_mask.nii.gz
echo $OUTPUT_STREAMLINES_NAME

# Apply linear transform to distorted b0 to get it into atlas space
echo -------

APPLYTRANSFORM_CMD="antsApplyTransforms -d 3 -i $T1_PATH -r $REFERENCE -n Linear -t $ANTS_T12Atlas -o $OUTPUT_NAME"

echo $APPLYTRANSFORM_CMD
eval $APPLYTRANSFORM_CMD