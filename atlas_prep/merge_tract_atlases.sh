#!/bin/bash

ATLAS_DIR=$1
PRE=$2
PROJS=("HCP" "BLSA" "NORMAL" "ALL")

for proj in ${PROJS[*]}; do
    fslmerge -t "$ATLAS_DIR"/"$PRE"Linear_"$proj".nii.gz "$ATLAS_DIR"/"$proj"/*Linear*.nii.gz
    fslmerge -t "$ATLAS_DIR"/"$PRE"Nonlinear_"$proj".nii.gz "$ATLAS_DIR"/"$proj"/*Nonlinear*.nii.gz
done
