import os
import shutil
import zipfile
import threading

def extract_move(zip_dir, zip_path, bedpostx_dir, bedpostx_rename, target_dir, unzip_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        print('Unzipping {}'.format(zip_path))
        zip_ref.extractall(zip_dir)

    shutil.move(bedpostx_dir, bedpostx_rename)
    print('Moving {} to {}'.format(bedpostx_rename, target_dir))
    shutil.move(bedpostx_rename, target_dir)
    print('Removing {}'.format(unzip_path))
    shutil.rmtree(unzip_path)


zip_dir = '/nfs/HCP/bedpostx_retest'
retest = '_retest'
out_dir = '/nfs/masi/hansencb/t1_tract_data/raw_data/HCP'


threads = []

for z in os.listdir(zip_dir):
    zip_path = os.path.join(zip_dir, z)

    subj_id = z.split('_')[0]
    sess_id = subj_id + retest

    unzip_path = os.path.join(zip_dir, subj_id)
    bedpostx_dir = os.path.join(unzip_path, 'T1w', 'Diffusion.bedpostX')
    bedpostx_rename = os.path.join(unzip_path, 'T1w', 'bedpostx')

    target_dir = os.path.join(out_dir, subj_id, sess_id, 'derivatives')
    target_sess = os.path.join(out_dir, subj_id, sess_id)

    if os.path.isdir(target_sess):
        if not os.path.isdir(target_dir):
            print('Making derivatives folder: {}'.format(target_dir))
            os.mkdir(target_dir)

        threads.append(threading.Thread(target=extract_move, args=(zip_dir, zip_path, bedpostx_dir, bedpostx_rename, target_dir, unzip_path,)))
        threads[-1].start()

        if len(threads) == 32:
            for thread in threads:
                thread.join()
            threads = []

for thread in threads:
    thread.join()



