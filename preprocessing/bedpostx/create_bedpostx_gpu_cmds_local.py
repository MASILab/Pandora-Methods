import os

dirs = ['/nfs/masi/hansencb/t1_tract_data/raw_data/NORMAL',
     '/nfs/masi/hansencb/t1_tract_data/raw_data/BLSA',
     '/nfs/masi/hansencb/t1_tract_data/raw_data/HCP']

singularity_path = '/nfs/masi/hansencb/t1_tract_data/preprocessing/fsl_601.simg'
conf_path = '/nfs/masi/hansencb/t1_tract_data/preprocessing/bedpostx/bedpostx.conf'
cmd = 'tmp_dir=$(mktemp -d -t bedpostx-XXXXXXXXX) && '\
      'mkdir -p $tmp_dir/{} && '\
      'mkdir -p $tmp_dir/{} && '\
      'cp {} $tmp_dir/{} && '\
      'cp {} $tmp_dir/{} && '\
      'cp {} $tmp_dir/{} && '\
      'cp {} $tmp_dir/{} && '\
      'cp {} $tmp_dir/{} && '\
      'cd $tmp_dir/ && '\
      'bet $tmp_dir/{} $tmp_dir/{} && '\
      'singularity exec -e --nv -B $tmp_dir/INPUTS/:/INPUTS -B $tmp_dir/OUTPUTS/:/OUTPUTS {} /extra/bedpostx_gpu_run.sh && '\
      'cp -r $tmp_dir/{} {} && '\
      'cp $tmp_dir/{} {} && '\
      'rm -rf $tmp_dir/\n'

out_file = 'bedpostx_cmds_local.txt'

with open(out_file, 'w') as f:
    for d in dirs:
        for subj in os.listdir(d):
            subj_dir = os.path.join(d, subj)
            if os.path.isdir(subj_dir):
                for sess in os.listdir(subj_dir):
                    sess_dir = os.path.join(subj_dir, sess)
                    if os.path.isdir(sess_dir):
                        bval_path = os.path.join(sess_dir, 'dwi', 'Diffusion.bvals')
                        bvec_path = os.path.join(sess_dir, 'dwi', 'Diffusion.bvecs')
                        dwmri_path = os.path.join(sess_dir, 'dwi', 'Diffusion.nii.gz')
                        b0_path = os.path.join(sess_dir, 'dwi', 'b0.nii.gz')

                        input_dir = os.path.join('INPUTS')
                        output_dir = os.path.join('OUTPUTS')

                        bval_work = os.path.join(input_dir, 'bvals')
                        bvec_work = os.path.join(input_dir, 'bvecs')
                        dwmri_work = os.path.join(input_dir, 'data.nii.gz')
                        b0_work = os.path.join('b0.nii.gz')
                        mask_work = os.path.join(input_dir, 'nodif_brain_mask.nii.gz')
                        conf_work = os.path.join(input_dir, 'bedpostx.conf')

                        output_source = os.path.join(output_dir, 'BEDPOSTX_DATA.bedpostX')
                        output_target = os.path.join(sess_dir, 'derivatives/bedpostx')
                        mask_target = os.path.join(sess_dir, 'dwi/mask.nii.gz')
                        if os.path.isfile(bval_path) and os.path.isfile(bvec_path) and os.path.isfile(dwmri_path) and os.path.isfile(b0_path) and not os.path.isdir(output_target):
                            f.write(cmd.format(input_dir, output_dir, bval_path, bval_work, bvec_path, bvec_work,
                                               dwmri_path, dwmri_work, b0_path, b0_work, conf_path, conf_work,
                                               b0_work, mask_work, singularity_path, output_source,
                                               output_target, mask_work, mask_target))



