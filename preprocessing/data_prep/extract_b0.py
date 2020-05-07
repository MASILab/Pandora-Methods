import os
import multiprocessing

def extract(sess_dir):
    if os.path.isdir(sess_dir):
        dwi_path = os.path.join(sess_dir, 'dwi', 'Diffusion.nii.gz')
        bval_path = os.path.join(sess_dir, 'dwi', 'Diffusion.bvals')
        out_path = os.path.join(sess_dir, 'dwi', 'b0.nii.gz')
        if os.path.isfile(dwi_path) and os.path.isfile(bval_path):
            with open(bval_path, 'r') as f:
                bvals = f.readline().strip().split(' ')
                bvals = [int(i) for i in bvals]

                idx = next(x[0] for x in enumerate(bvals) if x[1] < 10)

            os.system('/home-nfs2/local/VANDERBILT/blaberj/fsl_601/bin/fslroi {} {} {} 1'.format(dwi_path, out_path, idx))

root_dir = '/nfs/masi/hansencb/t1_tract_data/raw_data'
proj_names = ['HCP', 'NORMAL', 'BLSA']

threads = []
for proj in proj_names:
    proj_path = os.path.join(root_dir, proj)
    for subj in os.listdir(proj_path):
        subj_dir = os.path.join(proj_path, subj)
        if os.path.isdir(subj_dir):
            for sess in os.listdir(subj_dir):
                sess_dir = os.path.join(subj_dir, sess)
                t = multiprocessing.Process(target=extract, args=(sess_dir,))
                threads.append(t)
                t.start()

                if len(threads)>=5:
                    for thread in threads:
                        thread.join()
                    threads = []