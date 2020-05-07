import os

dirs = ['/nfs/masi/hansencb/t1_tract_data/raw_data/NORMAL',
     '/nfs/masi/hansencb/t1_tract_data/raw_data/BLSA',
     '/nfs/masi/hansencb/t1_tract_data/raw_data/HCP']

singularity_path = '/scratch/hansencb/tract_preprocessing/bedpostx/justinblaber-bedpostx_app-master-1.0.0.simg'
conf_path = '/scratch/hansencb/tract_preprocessing/bedpostx/bedpostx.conf'
work_dir = '/scratch/hansencb/tract_preprocessing/bedpostx/data'
cmd = 'module load GCC/5.4.0-2.26 OpenMPI/1.10.3 FSL/5.0.10 && '\
      'tmp_dir=$(mktemp -d -t bedpostx-XXXXXXXXX) && '\
      'mkdir -p $tmp_dir/{} && '\
      'mkdir -p $tmp_dir/{} && '\
      'scp hickory:{} $tmp_dir/{} && '\
      'scp hickory:{} $tmp_dir/{} && '\
      'scp hickory:{} $tmp_dir/{} && '\
      'scp hickory:{} $tmp_dir/{} && '\
      'cp {} $tmp_dir/{} && '\
      'cd $tmp_dir/ && '\
      'bet $tmp_dir/{} $tmp_dir/{} && '\
      'singularity run -e -B $tmp_dir/INPUTS/:/INPUTS -B $tmp_dir/OUTPUTS/:/OUTPUTS {} && '\
      'scp -r $tmp_dir/{} hickory:{} && '\
      'scp $tmp_dir/{} hickory:{} && '\
      'rm -rf $tmp_dir/\n'

out_file = 'bedpostx_cmds.txt'

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

                        subj_work_dir = os.path.join(work_dir, subj)
                        sess_work_dir = os.path.join(work_dir, subj, sess)
                        input_dir = os.path.join('INPUTS')
                        output_dir = os.path.join('OUTPUTS')

                        bval_work = os.path.join(input_dir, 'dwmri.bval')
                        bvec_work = os.path.join(input_dir, 'dwmri.bvec')
                        dwmri_work = os.path.join(input_dir, 'dwmri.nii.gz')
                        b0_work = os.path.join('b0.nii.gz')
                        mask_work = os.path.join(input_dir, 'mask.nii.gz')
                        conf_work = os.path.join(input_dir, 'bedpostx.conf')

                        output_source = os.path.join(output_dir, 'BEDPOSTX_DATA.bedpostX')
                        output_target = os.path.join(sess_dir, 'derivatives/bedpostx')
                        mask_target = os.path.join(sess_dir, 'dwi/mask.nii.gz')
                        if os.path.isfile(bval_path) and os.path.isfile(bvec_path) and os.path.isfile(dwmri_path) and os.path.isfile(b0_path) and not os.path.isdir(output_target):
                            f.write(cmd.format(input_dir, output_dir, bval_path, bval_work, bvec_path, bvec_work,
                                               dwmri_path, dwmri_work, b0_path, b0_work, conf_path, conf_work,
                                               b0_work, mask_work, singularity_path, output_source,
                                               output_target, mask_work, mask_target))



