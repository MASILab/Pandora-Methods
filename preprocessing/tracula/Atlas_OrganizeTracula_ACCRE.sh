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

tmp_dir=$(mktemp -d -t tracula-XXXXXXXX)
mkdir $tmp_dir/reg
scp -r hickory:"$MAIN"/raw_data/"$DATA"/"$SUB"/"$SCAN"/tracula/dpath $tmp_dir/
scp hickory:"$MAIN"/raw_data/"$DATA"/"$SUB"/"$SCAN"/reg/ANTS0GenericAffine.mat $tmp_dir/reg/
scp hickory:"$MAIN"/raw_data/"$DATA"/"$SUB"/"$SCAN"/reg/epi_reg_d_ANTS.txt $tmp_dir/reg/
scp hickory:"$MAIN"/raw_data/"$DATA"/"$SUB"/"$SCAN"/reg/ANTS1Warp.nii.gz $tmp_dir/reg/

###########################################
################# LINEAR ##################
###########################################

OUTPUTDIR="$tmp_dir"/Linear/"$DATA"_"$SUB"_"$SCAN"
mkdir -p $OUTPUTDIR
REFERENCE=/scratch/hansencb/tract_preprocessing/mni_icbm152_t1_tal_nlin_asym_09c.nii.gz

# into OUTPUTDIR move each streamline from b0 to T1 and T1 to atlas linearly
ANTS_T12Atlas="$tmp_dir"/reg/ANTS0GenericAffine.mat
ANTS_b02T1="$tmp_dir"/reg/epi_reg_d_ANTS.txt
STREAM_PATH="$tmp_dir"/dpath

for i in "$STREAM_PATH"/*
do
	echo $i
	INPUT_STREAMLINES="$i"/path.pd.nii.gz

	if [[ -f $INPUT_STREAMLINES ]]
	then
    echo $INPUT_STREAMLINES
    filename=$(basename "$i" ".nii.gz")
    echo $filename
    OUTPUT_STREAMLINES_NAME="$OUTPUTDIR"/"$filename".nii.gz
    echo $OUTPUT_STREAMLINES_NAME

    # Apply linear transform to distorted b0 to get it into atlas space
    echo -------

    APPLYTRANSFORM_CMD="antsApplyTransforms -d 3 -i $INPUT_STREAMLINES -r $REFERENCE -n Linear -t $ANTS_T12Atlas -t $ANTS_b02T1 -o $OUTPUT_STREAMLINES_NAME"

    echo $APPLYTRANSFORM_CMD
    eval $APPLYTRANSFORM_CMD
	fi

done



###########################################
################# NONLINEAR ##################
###########################################

OUTPUTDIR="$tmp_dir"/Nonlinear/"$DATA"_"$SUB"_"$SCAN"
mkdir -p $OUTPUTDIR

# into OUTPUTDIR move each streamline from b0 to T1 and T1 to atlas linearly
ANTS_warp="$tmp_dir"/reg/ANTS1Warp.nii.gz



for i in "$STREAM_PATH"/*
do
	echo $i
  INPUT_STREAMLINES="$i"/path.pd.nii.gz

	if [[ -f $INPUT_STREAMLINES ]]
	then
    echo $INPUT_STREAMLINES
    filename=$(basename "$i" ".nii.gz")
    echo $filename
    OUTPUT_STREAMLINES_NAME="$OUTPUTDIR"/"$filename".nii.gz
    echo $OUTPUT_STREAMLINES_NAME

    # Apply linear transform to distorted b0 to get it into atlas space
    echo -------

    APPLYTRANSFORM_CMD="antsApplyTransforms -d 3 -i $INPUT_STREAMLINES -r $REFERENCE -n Linear -t $ANTS_warp -t $ANTS_T12Atlas -t $ANTS_b02T1 -o $OUTPUT_STREAMLINES_NAME"
    echo $APPLYTRANSFORM_CMD
    eval $APPLYTRANSFORM_CMD
	fi

done


scp -r "$tmp_dir"/Linear/"$DATA"_"$SUB"_"$SCAN" hickory:"$MAIN"/registered_data/TraculaLinear
scp -r "$tmp_dir"/Nonlinear/"$DATA"_"$SUB"_"$SCAN" hickory:"$MAIN"/registered_data/TraculaNonlinear
rm -rf $tmp_dir