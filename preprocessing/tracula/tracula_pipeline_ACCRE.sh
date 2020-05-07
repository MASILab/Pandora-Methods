#!/bin/bash

module load FreeSurfer/6.0.0 GCC/6.4.0-2.28 OpenMPI/2.1.1 FSL/5.0.10
source $FREESURFER_HOME/FreeSurferEnv.sh
export FSL_DIR=/accre/arch/easybuild/software/MPI/GCC/6.4.0-2.28/OpenMPI/2.1.1/FSL/5.0.10/fsl
SESS_PATH=$1
T1_PATH=$SESS_PATH/anat/T1.nii.gz
DWI_PATH=$SESS_PATH/dwi/Diffusion.nii.gz
BVAL_PATH=$SESS_PATH/dwi/Diffusion.bvals
BVEC_PATH=$SESS_PATH/dwi/Diffusion.bvecs
BEDPOSTX_PATH=$SESS_PATH/derivatives/bedpostx
RECON_PATH=$SESS_PATH/derivatives/freesurfer
CONF_SCRIPT=/scratch/hansencb/tract_preprocessing/tracula/gen_conf_ACCRE.py

tmp_dir=$(mktemp -d -t tracula-XXXXXXXX)
mkdir $tmp_dir/INPUTS
mkdir $tmp_dir/OUTPUTS
mkdir $tmp_dir/OUTPUTS/freesurfer
mkdir $tmp_dir/OUTPUTS/tracula

#Need T1, Diffusion, Bedpostx 
scp hickory:$T1_PATH $tmp_dir/INPUTS
scp hickory:$DWI_PATH $tmp_dir/INPUTS
scp hickory:$BVAL_PATH $tmp_dir/INPUTS
scp hickory:$BVEC_PATH $tmp_dir/INPUTS
scp -r hickory:$BEDPOSTX_PATH $tmp_dir/INPUTS
scp -r hickory:$RECON_PATH $tmp_dir/INPUTS

if [ -d "$tmp_dir/INPUTS/freesurfer"  ]
then
    mv $tmp_dir/INPUTS/freesurfer $tmp_dir/OUTPUTS/freesurfer/subj
else
    #Run recon-all on T1
    recon-all -i $tmp_dir/INPUTS/T1.nii.gz -subjid subj -sd $tmp_dir/OUTPUTS/freesurfer -all
fi

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

scp -r $tmp_dir/freesurfer hickory:$SESS_PATH/derivatives
scp -r $tmp_dir/tracula hickory:$SESS_PATH/derivatives
rm -rf $tmp_dir
