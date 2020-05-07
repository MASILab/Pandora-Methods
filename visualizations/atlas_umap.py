import nibabel as nib
import numpy as np
import os
import glob
import numpy as np
from sklearn.datasets import load_iris, load_digits
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import seaborn as sns
import pandas as pd
import umap
import os


proj_dir = '/nfs/masi/hansencb/t1_tract_data/Atlases'
atlas_dirs = ['AFQAtlases', 'AFQclippedAtlases', 'RecobundlesAtlases',
              'TractSegAtlases', 'TraculaAtlases', 'XtractAtlases']

# mask_path = '/nfs/masi/schilkg1/LearningWM/data/atlases/mni_icbm152_t1_tal_nlin_asym_09c_mask.nii'
# mask = nib.load(mask_path).get_fdata()
# mask = mask>0
#
# data = 0
# init = True
# for atlas_dir in atlas_dirs:
#     name = glob.glob(os.path.join(proj_dir, atlas_dir, '*Nonlinear_ALL.nii.gz'))[0]
#     path = os.path.join(proj_dir, atlas_dir, name)
#     img = nib.load(path).get_fdata()
#     if init:
#         # data = np.reshape(img, [img.shape[0]*img.shape[1]*img.shape[2], img.shape[3]])
#         data = img[mask]
#         init = False
#     else:
#         data = np.concatenate((data, img[mask]), axis=1)
#
#     if data.shape[1] == 4:
#         break
#
#
#
# reducer = umap.UMAP()
# embedding = reducer.fit_transform(np.transpose(data))
#
# out_path = 'nonlin_embedded.npy'
# np.save(out_path, embedding)

out_path = 'nonlin_embedded.npy'
embedding = np.load(out_path)

labels = []
methods = []
with open('umap_info_labels.csv', 'r') as f:
    for i, line in reversed(list(enumerate(f.readlines()))):
        method, name, label = line.strip().split(',')
        if label == '':
            # embedding = np.delete(embedding, i, axis=0)
            labels.append(0)
        else:
            label = int(label)
            labels.append(label)
        methods.append(method)

labels.reverse()
methods.reverse()

label_names = []
with open('umap_info_labels_names.csv', 'r') as f:
    for line in f.readlines():
        label_names.append(line.strip().split(',')[-1])


# custom = np.array(sns.color_palette('tab20', 20))
# colors = [custom[x-1] for x in labels]

cmap = []
with open('colors.txt', 'r') as f:
    for line in f.readlines():
        cmap.append([float(x) for x in line.strip().split(',')])

colors = [cmap[x-2] for x in labels]
markers = ['o', '^', 's', '*', 'D', 'p']

legend_elems = []
for c in np.unique(labels):
    color = cmap[c-2]
    legend_elems.append(
        Line2D([0], [0], marker='o', color='w', alpha=0.5, label=label_names[c], markerfacecolor=color, markersize=15))

legend_elems2 = []
for i,c in enumerate(np.unique(methods)):
    marker = markers[i]
    legend_elems2.append(
        Line2D([0], [0], marker=marker, color='w', alpha=0.5, label=c, markerfacecolor=cmap[-2], markersize=15))


colors = np.array(colors)

alpha_masks = [np.array(labels) == 0, np.array(labels) != 0]
alphas = [0.5, 0.5]

fig, ax = plt.subplots()
leg = plt.legend(handles=legend_elems, loc='upper right')
ax.add_artist(leg)
for i,method in enumerate(list(np.unique(methods))):
    method_mask = np.array(methods) == method
    for j,alph_mask in enumerate(alpha_masks):
        mask = method_mask * alph_mask
        plt.scatter(embedding[mask, 0], embedding[mask, 1], s=40, marker=markers[i], alpha=alphas[j], c=colors[mask,:])

plt.legend(handles=legend_elems2, loc='lower right')
plt.xticks([])
plt.yticks([])
# plt.title('{} {} Labeled Data {}'.format(method, num_labeled, layer))
# save_path = 'plots/{}_{}_labeled_{}.png'.format(method, num_labeled, '_'.join(layer.split(' ')))

# plt.savefig(save_path)
# plt.close()

plt.show()