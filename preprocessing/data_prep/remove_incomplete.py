import os

d = '/nfs/masi/hansencb/t1_tract_data/raw_data/BLSA'
for scan in os.listdir(d):
    scan_dir = os.path.join(d,scan)
    if os.path.isdir(scan_dir):
        for sess in os.listdir(scan_dir):
            sess_dir = os.path.join(scan_dir, sess)
            if os.path.isdir(sess_dir):
                dwi_dir = os.path.join(sess_dir, 'dwi')
                t1_dir = os.path.join(sess_dir, 'anat')

                if os.path.isdir(dwi_dir):
                    if len(os.listdir(dwi_dir)) == 0:
                        os.rmdir(dwi_dir)
                if os.path.isdir(t1_dir):
                    if len(os.listdir(t1_dir)) == 0:
                        os.rmdir(t1_dir)

                if len(os.listdir(sess_dir)) == 0:
                    os.rmdir(sess_dir)
        if len(os.listdir(scan_dir)) == 0:
            os.rmdir(scan_dir)