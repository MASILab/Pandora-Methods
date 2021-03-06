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

OUTPUTDIR="$MAIN"/Atlases/TractSegLinear/"$DATA"_"$SUB"_"$SCAN"
REFERENCE=/nfs/masi/schilkg1/LearningWM/data/atlases/mni_icbm152_t1_tal_nlin_asym_09c.nii.gz

# make INPUT/OUTPUT Directories
mkdir $OUTPUTDIR

# Copying T1_N3_lin_atlas to INPUTDIR
T1_CURRENT="$MAIN"/raw_data/"$DATA"/"$SUB"/"$SCAN"/reg/T1_N3_lin_atlas.nii.gz
T1_NEW="$OUTPUTDIR"/T1_N3_lin_atlas.nii.gz
COPY_CMD="cp $T1_CURRENT $T1_NEW"
echo $COPY_CMD
eval $COPY_CMD

# into OUTPUTDIR move each streamline from b0 to T1 and T1 to atlas linearly
ANTS_T12Atlas="$MAIN"/raw_data/"$DATA"/"$SUB"/"$SCAN"/reg/ANTS0GenericAffine.mat
ANTS_b02T1="$MAIN"/raw_data/"$DATA"/"$SUB"/"$SCAN"/reg/epi_reg_d_ANTS.txt
STREAM_PATH="$MAIN"/raw_data/"$DATA"/"$SUB"/"$SCAN"/derivatives/tractseg/bundle_segmentations

for i in "$STREAM_PATH"/*.nii.gz
do
	echo $i
	INPUT_STREAMLINES="$i"
	filename=$(basename "$INPUT_STREAMLINES" ".nii.gz")
	echo $filename
	OUTPUT_STREAMLINES_NAME="$OUTPUTDIR"/"$filename".nii.gz
	echo $OUTPUT_STREAMLINES_NAME

	# Apply linear transform to distorted b0 to get it into atlas space
	echo -------
	
	APPLYTRANSFORM_CMD="antsApplyTransforms -d 3 -i $INPUT_STREAMLINES -r $REFERENCE -n Linear -t $ANTS_T12Atlas -t $ANTS_b02T1 -o $OUTPUT_STREAMLINES_NAME"
	
	echo $APPLYTRANSFORM_CMD
	eval $APPLYTRANSFORM_CMD

done



###########################################
################# NONLINEAR ##################
###########################################

OUTPUTDIR="$MAIN"/Atlases/TractSegNonlinear/"$DATA"_"$SUB"_"$SCAN"
REFERENCE=/nfs/masi/schilkg1/LearningWM/data/atlases/mni_icbm152_t1_tal_nlin_asym_09c.nii.gz

# make INPUT/OUTPUT Directories
mkdir $OUTPUTDIR

# Copying T1_N3_lin_atlas to INPUTDIR
T1_CURRENT="$MAIN"/raw_data/"$DATA"/"$SUB"/"$SCAN"/reg/T1_N3_nonlin_atlas.nii.gz
T1_NEW="$OUTPUTDIR"/T1_N3_nonlin_atlas.nii.gz
COPY_CMD="cp $T1_CURRENT $T1_NEW"
echo $COPY_CMD
eval $COPY_CMD

# into OUTPUTDIR move each streamline from b0 to T1 and T1 to atlas linearly
ANTS_T12Atlas="$MAIN"/raw_data/"$DATA"/"$SUB"/"$SCAN"/reg/ANTS0GenericAffine.mat
ANTS_b02T1="$MAIN"/raw_data/"$DATA"/"$SUB"/"$SCAN"/reg/epi_reg_d_ANTS.txt
ANTS_warp="$MAIN"/raw_data/"$DATA"/"$SUB"/"$SCAN"/reg/ANTS1Warp.nii.gz
STREAM_PATH="$MAIN"/raw_data/"$DATA"/"$SUB"/"$SCAN"/derivatives/tractseg/bundle_segmentations

for i in "$STREAM_PATH"/*.nii.gz
do
	echo $i
	INPUT_STREAMLINES="$i"
	filename=$(basename "$INPUT_STREAMLINES" ".nii.gz")
	echo $filename
	OUTPUT_STREAMLINES_NAME="$OUTPUTDIR"/"$filename".nii.gz
	echo $OUTPUT_STREAMLINES_NAME

	# Apply linear transform to distorted b0 to get it into atlas space
	echo -------
	
	APPLYTRANSFORM_CMD="antsApplyTransforms -d 3 -i $INPUT_STREAMLINES -r $REFERENCE -n Linear -t $ANTS_warp -t $ANTS_T12Atlas -t $ANTS_b02T1 -o $OUTPUT_STREAMLINES_NAME"
	echo $APPLYTRANSFORM_CMD
	eval $APPLYTRANSFORM_CMD

done



