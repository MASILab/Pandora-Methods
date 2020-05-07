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
################# NONLINEAR ##################
###########################################

OUTPUTDIR="$MAIN"/registered_data/RecobundlesNonlinear/"$DATA"_"$SUB"_"$SCAN"
REFERENCE=/nfs/masi/schilkg1/LearningWM/data/atlases/mni_icbm152_t1_tal_nlin_asym_09c.nii.gz

# make INPUT/OUTPUT Directories
mkdir $OUTPUTDIR

# into OUTPUTDIR move each streamline from b0 to T1 and T1 to atlas linearly
ANTS_T12Atlas="$MAIN"/raw_data/"$DATA"/"$SUB"/"$SCAN"/reg/ANTS0GenericAffine.mat
ANTS_b02T1="$MAIN"/raw_data/"$DATA"/"$SUB"/"$SCAN"/reg/epi_reg_d_ANTS.txt
ANTS_warp="$MAIN"/raw_data/"$DATA"/"$SUB"/"$SCAN"/reg/ANTS1Warp.nii.gz
STREAM_PATH="$MAIN"/raw_data/"$DATA"/"$SUB"/"$SCAN"/derivatives/recobundles/TRACTOGRAPHY-recobundles

source activate python36

for i in "$STREAM_PATH"/streamlines*orig.nii.gz
do
	echo $i
	INPUT_STREAMLINES="$i"
	filename=$(basename "$INPUT_STREAMLINES" ".nii.gz")
	echo $filename
	OUTPUT_STREAMLINES_NAME="$OUTPUTDIR"/"$filename".nii.gz
	echo $OUTPUT_STREAMLINES_NAME

	# Apply linear transform to distorted b0 to get it into atlas space
	echo -------

	tmp_path="$INPUT_STREAMLINES"_fix.nii.gz

	FIX_CMD="python /nfs/masi/hansencb/t1_tract_data/preprocessing/recobundles/fix_data_type.py --input $INPUT_STREAMLINES --output $tmp_path"
	APPLYTRANSFORM_CMD="antsApplyTransforms -d 3 -i $tmp_path -r $REFERENCE -n Linear -t $ANTS_warp -t $ANTS_T12Atlas -t $ANTS_b02T1 -o $OUTPUT_STREAMLINES_NAME"

  if [ ! -f $OUTPUT_STREAMLINES_NAME ]; then
    echo $FIX_CMD
    eval $FIX_CMD
    echo $APPLYTRANSFORM_CMD
    eval $APPLYTRANSFORM_CMD
	fi

done


