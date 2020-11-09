import shutil
from pathlib import Path

in_dir = Path('/nfs/masi/hansencb/t1_tract_data/AtlasesQA/RecoBundles')
out_dir = Path('/nfs/masi/hansencb/t1_tract_data/AtlasesQA/RecoBundles/.unused')
dirs = ['BLSA', 'ALL', 'HCP', 'NORMAL']
filter_file = '/nfs/masi/hansencb/t1_tract_data/AtlasesQA/RecoBundles/order.txt'
fnames = []

with open(filter_file, 'r') as f:
    fnames = f.readlines()
    fnames = [x.strip() for x in fnames]

for d in dirs:
    data_dir = in_dir.joinpath(d)
    for fname in data_dir.iterdir():
        if fname.name not in fnames:
            print('Moving {}'.format(fname.name))
            shutil.move(str(fname), str(out_dir.joinpath(d, fname.name)))