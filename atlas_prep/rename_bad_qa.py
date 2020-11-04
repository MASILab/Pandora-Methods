from pathlib import Path
from shutil import move

# qa_file = '/nfs/masi/yangq6/WM_learning/AFQ/QA_tract_label/AFQ_data_QA.csv'
#
# data_dirs = ['/nfs/masi/hansencb/t1_tract_data/registered_data/AFQcleanNonlinear',
#              '/nfs/masi/hansencb/t1_tract_data/registered_data/AFQcleanLinear']

# qa_file = '/nfs/masi/yangq6/WM_learning/AFQ_clipped/QA_tract_label/AFQ_clipped_data_QA.csv'
#
# data_dirs = ['/nfs/masi/hansencb/t1_tract_data/registered_data/AFQclippedNonlinear',
#              '/nfs/masi/hansencb/t1_tract_data/registered_data/AFQclippedLinear']

qa_file = '/nfs/masi/yangq6/WM_learning/tracula/QA_tract_label/tracula_data_QA.csv'

data_dirs = ['/nfs/masi/hansencb/t1_tract_data/registered_data/TraculaNonlinear',
             '/nfs/masi/hansencb/t1_tract_data/registered_data/TraculaLinear']


with open(qa_file, 'r') as f:
    col_names = f.readline().strip().split(',')

    #for Tracula
    for i in range(len(col_names)):
        if col_names[i].startswith('lh') or col_names[i].startswith('rh'):
            col_names[i] = col_names[i][0:2] + '.' + col_names[i][3:]

    qa_data = {}
    for line in f.readlines():
        line = line.strip().split(',')
        qa_data[line[0]] = []
        for i in range(1, len(line)):
            if line[i] == '':
                qa_data[line[0]].append(col_names[i])

for data_dir in data_dirs:
    for sess in qa_data:
        sess_dir = Path(data_dir).joinpath(sess)
        if sess not in qa_data:
            if not sess.endswith('.bad'):
                move(str(sess_dir), str(sess_dir)+'.bad')
        else:
            for bundle in qa_data[sess]:
                bundle_path = sess_dir.joinpath(bundle+'.nii.gz')
                if bundle_path.is_file():
                    move(str(bundle_path), str(bundle_path)+'.bad')