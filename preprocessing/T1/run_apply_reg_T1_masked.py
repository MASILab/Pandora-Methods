import os
from multiprocessing import Process


def run_atlas_script(data, subj, sess):
    script_path = '/nfs/masi/hansencb/WM_Atlas_Learning/preprocessing/T1/apply_reg_T1_masked.sh'
    os.system('bash {} {} {} {}'.format(script_path, data, subj, sess))

projs = ['/nfs/masi/hansencb/t1_tract_data/raw_data/NORMAL',
         '/nfs/masi/hansencb/t1_tract_data/raw_data/HCP',
         '/nfs/masi/hansencb/t1_tract_data/raw_data/BLSA']

threads = []
for d in projs:
    data = d.split('/')[-1]
    for subj in os.listdir(d):
        subj_dir = os.path.join(d, subj)
        if os.path.isdir(subj_dir):
            for sess in os.listdir(subj_dir):
                threads.append(Process(target=run_atlas_script, args=(data, subj, sess)))
                threads[-1].start()

                if len(threads) > 16:
                    for thread in threads:
                        thread.join()
                    threads = []

for thread in threads:
    thread.join()