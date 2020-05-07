import os

data_dir = '/nfs/masi/hansencb/t1_tract_data/raw_data/'
# projs = ['NORMAL', 'HCP', 'BLSA']
projs = ['BLSA']
count = {'NORMAL':{'subjects':0, 'sessions':0},
         'HCP':{'subjects':0, 'sessions':0},
         'BLSA':{'subjects':0, 'sessions':0}}

out_file = 'QA_ventricle.csv'

with open(out_file, 'w') as f:
    for proj in projs:
        proj_dir = os.path.join(data_dir, proj)
        for subj in os.listdir(proj_dir):
            subj_dir = os.path.join(proj_dir, subj)
            if os.path.isdir(subj_dir):
                count[proj]['subjects'] += 1
                for sess in os.listdir(subj_dir):
                    sess_dir = os.path.join(subj_dir, sess)
                    
                    # if os.path.isdir(os.path.join(sess_dir, 'reg_redo')):
                    
                    QA_nonrig = os.path.join(sess_dir, 'QA', 'NONRigid_registration.tif')
                    QA_rig = os.path.join(sess_dir, 'QA', 'Rigid_registration.tif')

                    qa_complete = 0
                    if os.path.isfile(QA_rig) and os.path.isfile(QA_nonrig):
                        qa_complete = 1

                    f.write('{},{},{},{},{}\n'.format(proj, subj, sess, sess_dir, qa_complete))
                    count[proj]['sessions']+=1

print(count)
