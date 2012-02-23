#!/usr/local/bin/python
# coding: UTF-8

# released under bsd licence
# see LICENCE file or http://www.opensource.org/licenses/bsd-license.php for details
# Institute of Applied Simulation (ZHAW)
# Author Thomas Niederberger

import numpy as np

def get_neighbourhood_matrix(distance_matrix):
    """generate neighbourhood matrix for distanceMatrix"""
    return threshold_matrix(distance_matrix, 0)

def threshold_matrix(matrix, threshold):
    """set all entries in matrix with a value bigger than threshold to 1 and the rest to 0. """
    threshold_matrix = np.zeros_like(matrix)
    threshold_matrix[np.where(matrix > threshold)] = 1
    return threshold_matrix

def get_symmetric_random_matrix(len, random_generator):
    """Generate a symmetric matrix with dimension len x len.
    Parameters
    ----------
    len : integer
        size of generated matrix
    random_generator : generator function
        random_generator to use for random numbers 
    """
    values = np.zeros((len, len))
    for i in range(len-1):
        for j in range(i+1, len):
            value = random_generator()
            values[i][j] = value
            values[j][i] = value
    return values

def get_random_vector(len, max, random_generator):
    """values = np.zeros(len)
    for i in range(len):
        values[i] = int(random_generator() * (max + 1))
    return values"""
    return np.random.randint(max+1, size=len)