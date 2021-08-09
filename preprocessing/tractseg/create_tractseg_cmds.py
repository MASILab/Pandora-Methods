import os
import shutil

projs = ['/nfs/masi/hansencb/t1_tract_data/raw_data/HCP',
         '/nfs/masi/hansencb/t1_tract_data/raw_data/NORMAL',
         '/nfs/masi/hansencb/t1_tract_data/raw_data/BLSA']

work_dir = '/scratch/hansencb/tract_preprocessing/tractseg'
cmd = 'bash /scratch/hansencb/tract_preprocessing/tractseg/run_tractseg.sh {} {}\n'
      
out_file = 'tractseg_cmds.txt'
output_folders = ['bundle_segmentations', 'TOM_trackings', 'TOM', 'endings_segmentations']
output_files = ['nodif_brain_mask.nii.gz', 'peaks.nii.gz']

with open(out_file, 'w') as f:
    for proj in projs:
        for subj in os.listdir(proj):
            subj_dir = os.path.join(proj, subj)
            if os.path.isdir(subj_dir):
                for sess in os.listdir(subj_dir):
                    sess_dir = os.path.join(subj_dir, sess)
                    if os.path.isdir(sess_dir):
                        work_subj_dir = os.path.join(work_dir, subj)
                        work_sess_dir = os.path.join(work_dir, subj, sess)
                        dwi_path = os.path.join(sess_dir, 'dwi')
                        out_path = os.path.join(sess_dir, 'derivatives', 'tractseg_v2')
                        exists = True
                        for folder in output_folders:
                            if not os.path.isdir(os.path.join(out_path, folder)):
                                exists = False
                        if os.path.isdir(out_path) and not exists:
                            shutil.rmtree(out_path)
                        if os.path.isdir(dwi_path) and not exists:
                            f.write(cmd.format(dwi_path, out_path))
