#!/usr/local/bin/python
# coding: UTF-8

from matplotlib.pyplot import *
import random
import csv
from mlscripts.ml.util import *
from mlscripts.ml.hebbian_clustering import *
import colorsys

def iterate(data, n_clusters, n_visual_dimensions):
    data_no_mean = data - np.mean(data, 0)
    
    fig = figure(1, figsize=(14, 8))
    subplot = fig.add_subplot(111)
    
    ion()
    color_values = np.random.rand(n_clusters)
    colors = np.zeros((n_clusters, 3))

    for i in range(n_clusters):
        colors[i] = colorsys.hsv_to_rgb(color_values[i], 1.0, 1.0)

    (W, W_subgroups) = one_time_learning(data, n_clusters, n_visual_dimensions)
    (x, y, cluster_mapping) = project_items(data_no_mean, W, W_subgroups)
    #rescale "circle" visualization
    visual_location = np.zeros((data.shape[0], n_visual_dimensions))
    visual_location[:, 0] = 500 + 300 * x
    visual_location[:, 1] = 700 + 300 * y
    
    title('PCA')
    #plot(range(len(singular_values)), np.sqrt(singular_values))
    fig.delaxes(subplot)
    subplot = fig.add_subplot(111)
    scatter(np.array(np.real(visual_location[:, 0])), np.array(np.real(visual_location[:, 1])), c=colors[cluster_mapping, :])
    subplot.axis([0, 1200, 0, 1200])
    draw()
    
def process_project(tfidf_file):
    tf_matrix = np.genfromtxt(tfidf_file, delimiter=' ')
    print tf_matrix.shape
    n_clusters = 10
    n_visual_dimensions = 2
    
    indices = range(tf_matrix.shape[0])
    random.shuffle(indices)
    rand_data = tf_matrix[indices, :]
    
    iterate(tf_matrix, n_clusters, n_visual_dimensions)

if __name__ == "__main__":
    process_project("C:/Daten/atizo/data-repo/tf/out-tf-project-50.csv")