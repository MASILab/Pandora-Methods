import os
import shutil

proj_dirs = ['/nfs/masi/hansencb/t1_tract_data/raw_data/BLSA',
             '/nfs/masi/hansencb/t1_tract_data/raw_data/NORMAL',
             '/nfs/masi/hansencb/t1_tract_data/raw_data/HCP']


for proj_dir in proj_dirs:
    for subj in os.listdir(proj_dir):
        subj_dir = os.path.join(proj_dir, subj)
        for sess in os.listdir(subj_dir):
            sess_dir = os.path.join(subj_dir, sess)

            reg_priority = ['reg',
                            'reg/reg',
                            'reg_redo',
                            'reg_redo/reg']
            
            final_reg = None
            remove_reg = []
            num_dirs = 0
            for reg_dir in reg_priority:
                if os.path.isdir(os.path.join(sess_dir, reg_dir)):
                    num_dirs += 1
                    if final_reg:
                        remove_reg.append(final_reg)
                    final_reg = os.path.join(sess_dir, reg_dir)

            out_reg = os.path.join(sess_dir, 'reg')
            if num_dirs > 1:
                tmp_reg = os.path.join(sess_dir, 'tmp_reg')
                print('Move {} to {}'.format(final_reg, tmp_reg))
                shutil.move(final_reg, tmp_reg)
                for reg_dir in remove_reg:
                    if os.path.isdir(reg_dir):
                        print('Deleting {}'.format(reg_dir))
                        shutil.rmtree(reg_dir)
                print('Move {} to {}'.format(tmp_reg, out_reg))
                shutil.move(tmp_reg, out_reg)
            elif num_dirs == 1 and final_reg != out_reg:
                print('Move {} to {}'.format(final_reg, out_reg))
                shutil.move(final_reg, out_reg)
