#!/usr/local/bin/python
# coding: UTF-8

# released under bsd licence
# see LICENCE file or http://www.opensource.org/licenses/bsd-license.php for details
# Institute of Applied Simulation (ZHAW)
# Author Thomas Niederberger

import numpy as np
from util import *

def project_items(data, W, W_subgroups):
    """
    
    Args:

        
    Returns:
        a three element tuple containing x, y coordinates and a cluster id for each element.
    """
    n_clusters = W.shape[0]
    n_records = data.shape[0]
    sub_locations = np.zeros((n_records, 2))
    a_side = np.sqrt(2-2*np.cos(2*np.pi/n_clusters))
    
    #cluster
    location = np.dot(data, W.T)    
    value = np.max(abs(location), 1)
    cluster_mapping = np.argmax(abs(location), 1)
    print [np.sum(cluster_mapping == i) for i in range(n_clusters)]
    
    for i in range(n_clusters):
        if sum(cluster_mapping == i) > 2:
            #(singular_values_dontcare, sub_cluster_location, eigenvec_dontcare) = pca(data[cluster_mapping == i, :], 2)
            sub_cluster_location = np.dot(data[cluster_mapping == i, :], W_subgroups[i].T)
            sub_locations[cluster_mapping == i, :] = a_side * sub_cluster_location / (np.max(sub_cluster_location) - np.min(sub_cluster_location))
        elif sum(cluster_mapping == i) > 0:
            sub_locations[cluster_mapping == i, :] = 0
    x = (np.cos(cluster_mapping * 2 * np.pi / (n_clusters)) + sub_locations[:, 0])
    y = (np.sin(cluster_mapping * 2 * np.pi / (n_clusters)) + sub_locations[:, 1])
    return (x, y, cluster_mapping)

def learn_weights(data, W, W_subgroups, n_clusters, iterations, learning_rate, visual_learning_rate, n_visual_dimensions=2, gamma=3.0):
    W = hebbian_learning(data, W, n_clusters, iterations, learning_rate, gamma)
    #print np.sum(W.T * reference_vectors, 0) / np.power(np.sum(np.power(W, 2), 1), 0.5)

    #cluster
    location = np.dot(data, W.T)    
    value = np.max(abs(location), 1)
    cluster_mapping = np.argmax(abs(location), 1)
    
    for i in range(n_clusters):
        indeces = (cluster_mapping == i)
        if sum(indeces) > 2:
            W_subgroups[i] = hebbian_learning(data[indeces, :], W_subgroups[i], n_visual_dimensions, 4, visual_learning_rate)
    return (W, W_subgroups)

def hebbian_learning(data, W = None, dimensions = 2, iterations = 100, learning_rate=decay_learning_rate(), gamma=1.0):
    """Executes hebbian learning for the dataset data.
    
    Args:
        W = weight matrix (default=random initialization)
        learning_rate: generator function returning a learning_rate
        gamma: float to increase convergence speed (default=1.0)
        
    Returns:
        adapted weight matrix
    """
    features = data.shape[1]
    examples = data.shape[0]
    if W == None:
        W = np.random.randn(dimensions, features) #random weight matrix
        #normalize to length = 1 --> divide by length
        W = (W.T * (1 / np.power(np.sum(np.power(W, 2), 1), 0.5))).T
    
    for iter in range(iterations):
        x = data[np.random.randint(0, examples), :] #select random example
        y = np.dot(W, x) #calculate output 
        lower = np.tril(np.outer(y, y))
        lower = lower + gamma * (lower - np.diag(np.diag(lower)))
        adjust = (np.outer(y, x) - np.dot(lower, W))
        delta_w = learning_rate.next() * adjust 
        W = W + delta_w
    return W