# released under bsd licence
# see LICENSE file or http://www.opensource.org/licenses/bsd-license.php for details
# Institute of Applied Simulation (ZHAW)
# Author Timo Jeranko

import functions as fn
from flatten import *
import scipy as scipy
import random as rd
import copy as copy
import numpy as np
import scipy.sparse as sparse
import ml.feature.pca as pca
import re
rnd = rd.random()

class Space:
    def __init__(self, table={'idea':[0, 0, 1]}, words=['word1', 'word2', 'word3'], named=True):
        self.table = table
        self.words = words    
        self.dimension = len(self.words)
        for item in self.table:
            assert len(self.table[item]) == self.dimension, 'size of vector \"' + item + '\" does not equal dimension'
        if not named:
            self.create_idea_names()

    def normalize(self):
        for item in self.table:
            self.table[item] = fn.normalize(self.table[item])

    def display(self):
        print self.words
        for item in self.table:
            print(self.table[item])

    def n_zero_vectors(self):
        n = 0
        for item in self.table:
            if fn.iszero(self.table[item]):
                n += 1
        return n

    def remove_zero_vectors(self):
        table = copy.copy(self.table)
        for item in table:
            if fn.iszero(table[item]):
                self.table.pop(item)
        
    def getmatrix(self):
        matrix = []
        for item in self.table:
            matrix.append(self.table[item])
        return matrix

    def create_idea_names(self):
        self.idea_names = {}
        for item in self.table:
            name = ""
            for i, element in enumerate(self.table[item]):
                word = self.words[i]
                word = re.sub("\"", "", str(word))
                if element > 0 :
                    if len(name) == 0:
                        name = name + word
                    else:
                        name = name + "+" + word
            self.idea_names[item] = name
      
    def pca_reduce(self, dimensions):
        matrix = []
        keys = []
        for item in self.table:
            matrix.append(self.table[item])
            keys.append(item)
        matrix = sparse.csc_matrix(matrix)
        reduced = pca.pca(matrix, dimensions)
        reduced = scipy.array(reduced)
        for i, row in enumerate(reduced):
            self.table[keys[i]] = row
        self.words = range(dimensions)
        self.dimension = len(self.words)   
    
    def add_symbol_vectors(self, coeff):
        self.symbol_vectors = {}
        size = len(self.table)
        vector = scipy.zeros(size)
        symb = scipy.zeros(self.dimension)
        self.symbol_vectors = {}
        for i, item in enumerate(self.table):
            self.words.append("S:" + item)     
            v = copy.copy(vector)
            s = copy.copy(symb)
            v[i] = coeff
            self.symbol_vectors[item] = scipy.concatenate((s, v), 0)
            self.table[item] = scipy.concatenate((self.table[item], v), 0)   
        self.dimension = len(self.words)

class Map:
    def __init__(self , size=[10, 10, 10] , space=Space(), params={"tau1":2000, "nu0":0.1, "tau2":5000, "renormalize":0.999}):   
        self.dimension = len(size)
        self.size = size
        self.size.reverse()
        print self.size
        self.space = space
        #self.space.normalize()
        self.neurons = self.populate(self.size)
        self.time = 0
        
        self.tau1 = params["tau1"]                                                # neighbourhood shrinkage time constant
        self.nu0 = params["nu0"]                                                 # initial learning rate  
        self.tau2 = params["tau2"]                                                # learning rate time constant
        self.sigma0 = 0.5 * scipy.sqrt(scipy.dot(size, size))                      # parameter for gaussian neighbourhood function
        
        self.renormalization_threshold = params["renormalize"]
        self.gaussian_threshold = 1e-5
    
    def setsize(self, x):
        self.dimension = len(x)
        self.size = x 
        self.neurons = self.populate(x)
    
    def getsize(self):
        return self.size
    
    def getneurons(self):
        return self.neurons
    
    def populate(self, size):                                          #populate  n * m * ... * k  map with neurons (square geometry)
        dimension = len(size)
        self.position = scipy.zeros(dimension, int)
        return self.__populate(size, dimension)
    
    def __populate(self, size, dimension):
        if dimension == 1:
            matrix = []
            for i in range(size[0]):
                self.position[0] = i                                                 # counter
                position = self.position[:]
                position = fn.to_float(position)
                position.reverse()
                neuron = Neuron(position , self.space.dimension)      # position of neuron in map is same as object  postion in matrix
                matrix.append(neuron)                                                # dimension of neuron is same as dimension of space
            return matrix
        else:
            matrix = []
            for i in range(size[dimension - 1]):
                self.position[dimension - 1] = i
                matrix.append(self.__populate(size, dimension - 1))      #recursion
            return matrix
    
    def average_distance_to_bmu(self):
        dd = 0.0
        for item in self.space.table:
            bmu = self.find_bmu(item)
            dd += fn.distance(bmu.weight , self.space.table[item])
        return dd / len(self.space.table)        
    
    def get_weight_indexes(self, xx, neighborhood):
        ranges = []
        for i, x in enumerate(xx):
            lower = (x - neighborhood) % self.size[i]
            upper = (x + neighborhood) % self.size[i]
            r = fn.mod_range(lower, upper + 1, self.size[i]) 
            ranges.append(r)
         
        reduced_positions = fn.combinations(ranges)     
        for i, position in self.positions:
            if position in reduced_positions:
                print i
        return 0
    
    def average_distance_to_bmu0(self):
        dd = 0.0
        for vector in self.vectors: 
            bmu = self.find_bmu0(vector)
            dd += fn.distance(self.weights[bmu], vector)
        return dd / len(self.vectors)
    
    def setweights(self):
        x = []
        list = flatten(self.neurons)
        for neuron in list:
            #x.append(fn.normalize(neuron.weight))
            x.append(neuron.weight)
        self.weights = scipy.array(x)   
    
    def setpositions(self):
        x = []
        list = flatten(self.neurons)
        for neuron in list:
            x.append(fn.to_int(neuron.position))
        self.positions = scipy.array(x)
    
    def setvectors(self):
        self.vectors = []
        self.keys = []
        for item in self.space.table:
            self.vectors.append(fn.normalize(self.space.table[item]))
            #self.vectors.append(self.space.table[item])
            self.keys.append(item)
        #self.vectors = (self.vectors - np.min(self.vectors, 0)) / (np.max(self.vectors, 0) - np.min(self.vectors, 0))
        pass
    
    def init_optimization(self):
        self.cutoff = 1e-4
        self.setweights()
        self.setpositions()
        self.setvectors()
      
    def renormalize(self): 
        for i, weight in enumerate(self.weights):
            self.weights[i] = fn.normalize0(weight)
        pass
    
    def find_bmu0(self, vector):
        m = 0
        i = -1 
        imax = 0
        for weight in self.weights:
            i += 1
            d = scipy.dot(weight, vector)  
            if d > m:
                m = d
                imax = i
        #distances = scipy.dot(self.weights, vector)
        #imax = np.argmax(distances)
        return imax
    
    def find_bmu1(self, vector):
        m = 1e8
        i = -1 
        imin = 0
        for weight in self.weights:
            i += 1
            #d = fn.distance(weight,vector)
            delta = weight - vector
            d = np.dot(delta, delta)
            if d < m:
                m = d
                imin = i
        #dist = np.power(self.weights - vector, 2)
        #imin = np.argmin(np.sum(dist, 1))
        return imin
    
    def distort0(self, vector, time):
        sigma = fn.decay(time, self.tau1, self.sigma0)
        a = 1.0 / (2.0 * sigma ** 2)
        bmu = self.find_bmu1(vector)
        w = self.weights[bmu]
        
        #     normal = scipy.dot(w, w)
        #     if normal < self.renormalization_threshold:
        #       self.renormalize()       
        #print fn.distance(w,vector)  
        
        learning = fn.decay(time, self.tau2, self.nu0)
        adaption = 0
        #could probably written in a vectorized way
        for i, weight in enumerate(self.weights):
        #       x = fn.torus_subtract( self.positions[i] , self.positions[bmu] , self.size)        # torus geometry
            x = self.positions[i] - self.positions[bmu]                                      # rectangular geometry
            gauss = fn.gaussian0(x, a)
            if gauss > self.gaussian_threshold:
                delta_w = (vector - weight)
                self.weights[i] = weight + gauss * learning * delta_w  
                #self.weights[i] = weight + gauss * delta_w #without learning rate
                adaption = adaption + np.dot(delta_w, delta_w)
        return adaption
    
    def iterate0(self, time):
        t = 0
        d = len(self.vectors) 
        while t <= time:
            vector = self.vectors[fn.random_int(d)]
            adaption = self.distort0(vector, t)
            print str(t) + ': ' + str(adaption) #, self.average_distance_to_bmu0()
            t += 1
            self.time += 1
        self.flush_map()     
    
    def flush_map(self):
        list = flatten(self.neurons)
        for n, neuron in enumerate(list):
            neuron.weight = self.weights[n] 

class Neuron:
    def __init__(self, position=[0.0, 0.0], dimension=3):
        self.position = position
        self.dimension = dimension
        self.weight = []
        for i in range(self.dimension):
            r = rd.random()*0.1
            self.weight.append(r)              # initialize weights 
    
    def setposition(self, x):
        self.position = x    
    
    def getposition(self):
        return self.position
    
    def setweight(self, w):
        self.dimension = len(w)
        self.weight = w
    
    def getweight(self):
        return self.weight