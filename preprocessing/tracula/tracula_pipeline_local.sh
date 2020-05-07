#!/bin/bash

SESS_PATH=$1
T1_PATH=$SESS_PATH/anat/T1.nii.gz
DWI_PATH=$SESS_PATH/dwi/Diffusion.nii.gz
BVAL_PATH=$SESS_PATH/dwi/Diffusion.bvals
BVEC_PATH=$SESS_PATH/dwi/Diffusion.bvecs
BEDPOSTX_PATH=$SESS_PATH/derivatives/bedpostx
CONF_SCRIPT=/nfs/masi/hansencb/t1_tract_data/preprocessing/tracula/gen_conf.py

tmp_dir=$(mktemp -d -t tracula-XXXXXXXX)
mkdir $tmp_dir/INPUTS
mkdir $tmp_dir/OUTPUTS
mkdir $tmp_dir/OUTPUTS/freesurfer
mkdir $tmp_dir/OUTPUTS/tracula

#Need T1, Diffusion, Bedpostx 
cp $T1_PATH $tmp_dir/INPUTS
cp $DWI_PATH $tmp_dir/INPUTS
cp $BVAL_PATH $tmp_dir/INPUTS
cp $BVEC_PATH $tmp_dir/INPUTS
cp -r $BEDPOSTX_PATH $tmp_dir/INPUTS

#Run recon-all on T1
recon-all -i $tmp_dir/INPUTS/T1.nii.gz -subjid subj -sd $tmp_dir/OUTPUTS/freesurfer -all

#Generate tracula conf file
python $CONF_SCRIPT --work_dir $tmp_dir

#Run trac-all prep without correction & mv bedpostx
trac-all -c $tmp_dir/INPUTS/trac.conf -prep
mv $tmp_dir/INPUTS/bedpostx/ $tmp_dir/OUTPUTS/tracula/subj/dmri.bedpostX

#Run trac-all path
trac-all -c $tmp_dir/INPUTS/trac.conf -path 

#Copy output
mv $tmp_dir/OUTPUTS/freesurfer/subj $tmp_dir/freesurfer
mv $tmp_dir/OUTPUTS/tracula/subj $tmp_dir/tracula

cp -r $tmp_dir/freesurfer $SESS_PATH/derivatives
cp -r $tmp_dir/tracula $SESS_PATH/derivatives
#rm -rf $tmp_dir
