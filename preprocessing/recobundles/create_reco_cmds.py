import os

projs = ['/nfs/masi/hansencb/t1_tract_data/raw_data/HCP',
         '/nfs/masi/hansencb/t1_tract_data/raw_data/NORMAL',
         '/nfs/masi/hansencb/t1_tract_data/raw_data/BLSA']
#projs = ['/nfs/masi/hansencb/t1_tract_data/sample']

cmd = 'tmp_dir=$(mktemp -d -t reco-XXXXXXXXX) && '\
      'mkdir -p $tmp_dir/{} && ' \
      'mkdir -p $tmp_dir/{} && ' \
      'scp -r hickory:{} $tmp_dir/{} && ' \
      'scp -r hickory:{} $tmp_dir/{} && ' \
      'scp -r hickory:{} $tmp_dir/{} && ' \
      'python /scratch/hansencb/tract_preprocessing/recobundles/WMLearning_CreateStreamlines.py $tmp_dir/{} $tmp_dir/{}  /scratch/hansencb/tract_preprocessing/recobundles/Atlas_80_Bundles && ' \
      'mv $tmp_dir/{} $tmp_dir/recobundles_v2 && ' \
      'scp -r $tmp_dir/recobundles_v2 hickory:{} && ' \
      'rm -rf $tmp_dir \n'

out_file = 'reco_cmds.txt'

with open(out_file, 'w') as f:
    for d in projs:
        for subj in os.listdir(d):
            subj_dir = os.path.join(d, subj)
            if os.path.isdir(subj_dir):
                for sess in os.listdir(subj_dir):
                    sess_dir = os.path.join(subj_dir, sess)
                    if os.path.isdir(sess_dir):
                        bval_path = os.path.join(sess_dir, 'dwi', 'Diffusion.bvals')
                        bvec_path = os.path.join(sess_dir, 'dwi', 'Diffusion.bvecs')
                        dwmri_path = os.path.join(sess_dir, 'dwi', 'Diffusion.nii.gz')

                        input_dir = 'INPUTS'
                        output_dir = 'OUTPUTS'

                        bval_work = os.path.join(input_dir, 'dwmri.bval')
                        bvec_work = os.path.join(input_dir, 'dwmri.bvec')
                        dwmri_work = os.path.join(input_dir, 'dwmri.nii.gz')

                        output_target = os.path.join(sess_dir, 'derivatives')
                        if os.path.isfile(bval_path) and os.path.isfile(bvec_path) and os.path.isfile(dwmri_path) and not os.path.isdir(os.path.join(output_target, 'recobundles_v2')):
                            f.write(cmd.format(input_dir, output_dir, bval_path, bval_work, bvec_path, bvec_work,
                                               dwmri_path, dwmri_work, output_dir, input_dir, output_dir, output_target))


