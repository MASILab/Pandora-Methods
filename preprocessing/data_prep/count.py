import os

d = '/nfs/masi/hansencb/t1_tract_data/raw_data/BLSA'
count = 0

for scan in os.listdir(d):
    for sess in os.listdir(os.path.join(d,scan)):
        count += 1

print(count)