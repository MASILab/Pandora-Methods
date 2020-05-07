import numpy as np
import os
import matplotlib.pyplot as plt

dice_dir = 'tract_correlation'

with open('wm_atlas_tract_paths.txt', 'r') as f:
    paths = [x.strip() for x in f.readlines()]

seperate = [0]
label_pos = []
init = True
prev_method = ''
for i, path in enumerate(paths):
    parts = path.split('/')
    method = parts[-3]
    if not init and method != prev_method:
        seperate.append(i)
        label_pos.append(seperate[-2] + int((seperate[-1] - seperate[-2])/2))
    elif init:
        init = False
    prev_method = method

seperate = seperate[1:]
label_pos.append(seperate[-1] + int ((len(paths) - 1 - seperate[-1])/2))

scores = np.zeros([len(paths), len(paths)])

for fname in os.listdir(dice_dir):
    path = os.path.join(dice_dir, fname)
    x = int(fname.split('_')[1])
    y = int(fname.split('_')[-1].strip('.txt'))
    with open(path, 'r') as f:
        dice = float(f.readline().strip())
        scores[x,y] = dice
        scores[y,x] = dice

        if x == y:
            scores[x,y] = 0

fig, ax = plt.subplots()
plt.imshow(scores)
for sep in seperate:
    plt.plot([sep]*216, np.arange(0, 216), 'w')
    plt.plot(np.arange(0, 216), [sep] * 216, 'w')

methods = ['AFQ', 'AFQ clipped', 'Recobundles', 'TractSeg', 'Tracula', 'Xtract']
plt.xticks(label_pos, methods, rotation=45, fontsize=10)
plt.yticks(label_pos, methods)
plt.margins(0.5)
plt.colorbar()
fig.subplots_adjust(bottom=0.2)
plt.show()
