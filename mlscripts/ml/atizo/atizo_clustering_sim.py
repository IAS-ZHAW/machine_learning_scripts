#!/usr/local/bin/python
# coding: UTF-8

from matplotlib.pyplot import *
import random
import csv
from mlscripts.ml.util import *
from mlscripts.ml.hebbian_clustering import *
import colorsys
import logging

def iterate(data, n_clusters, n_visual_dimensions):
    n_records = data.shape[0]
    data = data / 4
    data = data - np.mean(data, 0)

    fig = figure(1, figsize=(14, 8))
    subplot = fig.add_subplot(111)

    #learning_rate = decay_learning_rate(1.0, 500.0, 0.0010)
    learning_rate = decay_learning_rate(1.0, 500.0, 0.010)
    visual_learning_rate = const_learning_rate(0.0001)
    #W = np.random.randn(n_records, n_features)
    W = None
    W_subgroups = [None for i in range(n_clusters)]

    ion()
    color_values = np.random.rand(n_clusters)
    colors = np.zeros((n_clusters, 3))
    for i in range(n_clusters):
        colors[i] = colorsys.hsv_to_rgb(color_values[i], 1.0, 1.0)

    learn_iterations = 100
    iterations = 100
    for i in xrange(iterations):
        item_index = int((n_records - 20) / iterations * i) + 20
        #learn_data = data[0:item_index, :] #simulate a growing dataset
        learn_data = data

        (W, W_subgroups) = learn_weights(learn_data, W, W_subgroups, n_clusters, learn_iterations, learning_rate, visual_learning_rate)
        (x, y, cluster_mapping) = project_items(learn_data, W, W_subgroups)
        #rescale "circle" visualization
        visual_location = np.zeros((learn_data.shape[0], n_visual_dimensions))
        visual_location[:, 0] = 500 + 300 * x
        visual_location[:, 1] = 700 + 300 * y

        title('PCA')
        #plot(range(len(singular_values)), np.sqrt(singular_values))
        fig.delaxes(subplot)
        subplot = fig.add_subplot(111)
        scatter(np.array(np.real(visual_location[:, 0])), np.array(np.real(visual_location[:, 1])), c=colors[cluster_mapping, :])
        subplot.axis([0, 1200, 0, 1200])
        draw()
        canvas = gcf().canvas
        canvas.start_event_loop(timeout=0.010)

def process_project(tfidf_file):
    tf_matrix = np.genfromtxt(tfidf_file, delimiter=' ')
    print tf_matrix.shape
    n_clusters = 10
    n_visual_dimensions = 2

    indices = range(tf_matrix.shape[0])
    random.shuffle(indices)
    rand_data = tf_matrix[indices, :]

    iterate(rand_data, n_clusters, n_visual_dimensions)

if __name__ == "__main__":
    logging.basicConfig()
    process_project("C:/Daten/atizo/data-repo/tf/out-tf-project-50.csv")
