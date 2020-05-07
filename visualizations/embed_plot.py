import numpy as np
from sklearn.datasets import load_iris, load_digits
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import seaborn as sns
import pandas as pd
import umap
import os

feature_dir = 'features'

op_to_layer = {'classify_9_LeakyRelu_18:0_embedded.npy':'Residual Layer 21',
               'classify_9_LeakyRelu_12:0_embedded.npy':'Residual Layer 14',
               'classify_9_LeakyRelu_6:0_embedded.npy':'Residual Layer 7',
               'Softmax_4:0_embedded.npy': 'Softmax Activation'}

for d in os.listdir(feature_dir):
    exp_feature_dir = os.path.join(feature_dir, d)

    parts = d.split('_')
    alpha, wmatch, beta = parts[2], parts[4], parts[6]
    num_labeled = parts[0].split('@')[-1].split('-')[0]
    if alpha == '1.0':
        method = 'MixMatchNST'
    else:
        method = 'MixMatch'

    for op in os.listdir(exp_feature_dir):
        path = os.path.join(exp_feature_dir, op)
        # if 'labels' not in layer and layer.endswith('.npy'):
        #     data = np.load(path)
        #     data = np.reshape(data, (data.shape[0], -1))
        #     reducer = umap.UMAP()
        #     embedding = reducer.fit_transform(data)
        #
        #     out_path = '{}_embedded.npy'.format(path[0:-4])
        #     np.save(out_path, embedding)
        if 'embedded' in op:
            layer = op_to_layer[op]
            cifar_10_classes = ['Airplane', 'Automobile', 'Bird', 'Cat', 'Deer', 'Dog', 'Frog', 'Horse', 'Ship', 'Truck']
            embedding = np.load(path)
            labels = np.load(path.replace('embedded', 'labels'))
            colors = [sns.color_palette('Paired')[x] for x in labels]
            class_to_color = {}
            for i in range(len(labels)):
                class_to_color[labels[i]] = colors[i]

            legend_elems = []
            for c in range(len(class_to_color)):
                color = class_to_color[c]
                legend_elems.append(Line2D([0], [0], marker='o', color='w', label=cifar_10_classes[c], markerfacecolor=color, markersize=15))

            plt.figure(figsize=(10, 8))
            plt.scatter(embedding[:,0], embedding[:, 1], s=40, marker='o', alpha=0.5, c=colors)
            # plt.legend(handles=legend_elems, loc='best')
            plt.title('{} {} Labeled Data {}'.format(method, num_labeled, layer))
            save_path = 'plots/{}_{}_labeled_{}.png'.format(method, num_labeled, '_'.join(layer.split(' ')))

            plt.savefig(save_path)
            plt.close()

# data = np.load('test/classify_9_LeakyRelu_15:0.npy')
# labels = np.load('test/classify_9_LeakyRelu_15:0_labels.npy')
# data = np.load('test/Softmax_4:0.npy')
# labels = np.load('test/Softmax_4:0_labels.npy')
#
# data = np.reshape(data, (data.shape[0], -1))
# reducer = umap.UMAP()
#
# embedding = reducer.fit_transform(data)
# colors = [sns.color_palette('Paired')[x] for x in labels]
# class_to_color = {}
# for i in range(len(labels)):
#     class_to_color[labels[i]] = colors[i]
#
# legend_elems = []
# for c in range(len(class_to_color)):
#     color = class_to_color[c]
#     legend_elems.append(Line2D([0], [0], marker='o', color='w', label=cifar_10_classes[c], markerfacecolor=color, markersize=15))
#
#
# plt.scatter(embedding[:,0], embedding[:, 1], s=40, marker='o', alpha=0.5, c=colors)
# plt.legend(handles=legend_elems, loc='best')
# plt.show()
