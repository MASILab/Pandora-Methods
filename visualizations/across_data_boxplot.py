import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

dice_dir = 'across_data_correlation'

scores = {}
for fname in os.listdir(dice_dir):
    path = os.path.join(dice_dir, fname)
    compare = '_'.join(fname.split('_')[1:4])

    with open(path, 'r') as f:
        score = float(f.readline().strip())

    if compare not in scores:
        scores[compare] = []

    if not np.isnan(score):
        scores[compare].append(score)

groups = ['HCP_BLSA', 'HCP_NORMAL', 'BLSA_NORMAL']
xticks = ['HCP-BLSA', 'HCP-VU', 'BLSA-VU']
methods = ['AFQcleanNonlinear', 'AFQclippedNonlinear', 'XtractNonlinear',
           'TractSegNonlinear', 'RecobundlesNonlinear', 'TraculaNonlinear']


data = [[], []]
f, ax = plt.subplots(2,3)
for i,m in enumerate(methods):
    mname = m.replace('Nonlinear', '')
    mname = mname.replace('clean', '')
    for j,g in enumerate(groups):
        k = '_'.join([g,m])
        gname = xticks[j]


        dice = scores[k]

        for d in dice:
            data[0].append(d)
            data[1].append(gname)

    df = pd.DataFrame(list(zip(data[1], data[0])), columns=['Compare', 'Correlation'])

    k = i%3
    j = int(np.floor(i/3))
    sns.boxplot(y='Correlation', x='Compare', data=df, ax=ax[j,k])
    sns.swarmplot(y='Correlation', x='Compare', data=df, ax=ax[j,k], color="0.25", size=2)
    ax[j,k].set_xlabel('')
    ax[j,k].set_xticklabels(xticks, rotation=45)
    ax[j,k].grid(True, axis='y')
    ax[j,k].set_title(mname)
    ax[j, k].set_ylim([0.4, 1])
    if k != 0:
        ax[j,k].set_ylabel('')
    if j != 1:
        ax[j,k].set_xticklabels([])

plt.show()
