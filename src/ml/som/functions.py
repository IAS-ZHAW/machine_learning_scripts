# released under bsd licence
# see LICENSE file or http://www.opensource.org/licenses/bsd-license.php for details
# Institute of Applied Simulation (ZHAW)
# Author Timo Jeranko

import numpy as np
from random import random

def gaussian(x, sigma):
    return  np.exp(-np.dot(x, x) * (1.0 / (2.0 * (sigma ** 2))))

def gaussian0(x, a):
    return  np.exp(-np.dot(x, x) * a)

def decay(t, tau, x0):
    return x0 * np.exp(-float(t) / tau)

def length(x):
    return np.sqrt(np.dot(x, x))

def distance(x, y):
    x = np.array(to_float(x))
    y = np.array(to_float(y))
    a = x - y
    return np.sqrt(np.dot(a, a))

def normalize(x):
    if length(x) == 0:
        return np.array(x)
    else:
        return np.array(x) * (1 / float(length(x)))

def normalize0(x):
    return x * (1.0 / length(x))

def torus_subtract(x, y, size):      # x and y are scipy arrays
    d = y - x
    for i, length in enumerate(size):
        threshold = length * 0.5
        if d[i] > threshold:
            d[i] = length - d[i]
    return d

def mod_range(a, b, mod):
    a = a % mod
    b = b % mod
    if a < b:
        return range(a, b)
    else:
        return range(a, mod) + range(0, b)

# array methods
def makezerovector(n):
    vector = []
    for i in range(n):
        vector.append(0)
    return vector

def to_float(array):
    out = []
    for x in array:
        if x == "": x = 0.0
        x = float(x)
        if np.isnan(x): x = 0.0
        out.append(x)
    return out

def to_int(array):
    out = []  
    for x in array:
        x = int(x)
        out.append(x)
    return out

def pick_random(dictionary):
    keys = []
    for key in dictionary:
        keys.append(key)
    i = int(random()*len(dictionary))
    return keys[i] 

def pick_random0(vector):
    i = int(random()*len(vector))
    return vector[i]

def random_int(n):
    return int(random() * n)

def mean_length(matrix):
    l = []
    for x in matrix:
        l.append(length(x))
    return np.mean(l)

def iszero(x):
    for a in x:
        if a != 0:
            return False
            break
    return True

def find_best_match(vector, matrix):
    max = 0
    i = -1 
    imax = 0
    for weight in matrix:
        i += 1
        d = np.dot(weight, vector)  
        if d > max:
            max = d
            imax = i
    return imax

def combinations(vectors):
    if len(vectors) == 1:
        out = []
        for i in vectors[0]:
            out.append([i])
        return out
    else:
        comb = combinations(vectors[1:])
        out = []
        for xx in comb:
            for i in vectors[0]:
                out.append(xx + [i])
        return out
