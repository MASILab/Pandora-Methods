import os

data_dir = '/nfs/masi/hansencb/t1_tract_data/raw_data/'
projs = ['NORMAL', 'HCP', 'BLSA']

count = {'NORMAL':{'subjects':0, 'sessions':0},
         'HCP':{'subjects':0, 'sessions':0},
         'BLSA':{'subjects':0, 'sessions':0}}

out_file = 'QA_tracula_list.csv'

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
                    
                    QA = os.path.join(sess_dir, 'QA', 'TraculaQA.tif')
                    deriv = os.path.join(sess_dir, 'derivatives', 'tracula')

                    qa_complete = 0
                    if os.path.isfile(QA) and os.path.isdir(deriv):
                        qa_complete = 1

                    f.write('{},{},{},{},{}\n'.format(proj, subj, sess, sess_dir, qa_complete))
                    count[proj]['sessions']+=1

print(count)
