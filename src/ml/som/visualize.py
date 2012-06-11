# released under bsd licence
# see LICENSE file or http://www.opensource.org/licenses/bsd-license.php for details
# Institute of Applied Simulation (ZHAW)
# Author Timo Jeranko

from classes import *
from flatten import *
import scipy as scipy
import functions as fn
import re
from collections import Counter

def word_plot(matrix):
    matrix = scipy.transpose(matrix)
    nrows = len(matrix)
    for i in range(nrows):
        i = nrows - 1 - i
        row = matrix[i]
        for m in row:
            print str(m) + "\t",
        print "\n"

def draw_basis_activation(map):             # This mapping finds the closest neuron for each basis vector and prints the "name" of the basis vector on the neuron position 
    words = empty_list(map.size, 1)

    basis_vectors = []
    d = map.space.dimension
    for i in range(d):
        b = scipy.zeros(d, int)
        b[i] = 1
        basis_vectors.append(b)

    for i, bv in enumerate(basis_vectors):
        bmu = map.find_bmu0(bv)
        x = map.positions[bmu]
        x = fn.to_int(x)
        words[x[0]][x[1]] = map.space.words[i]

    word_plot(words)
    return words

def draw_item_activation(mymap, named=True, overwrite=False, symbols=False):
    words = empty_list(mymap.size, 1)
    mymap.renormalize()             

    if named:
        vectors = mymap.vectors
        keys = mymap.keys
    else:
        vectors = []
        keys = []
        idea_names = mymap.space.idea_names
        for item in mymap.space.table:
            keys.append(idea_names[item])
            vectors.append(mymap.space.table[item])   

    if symbols:
        s = mymap.space.symbol_vectors
        keys = []
        vectors = []
        for item in s:
            keys.append(item)
            vectors.append(s[item])

    for i, vector in enumerate(vectors):
        match = fn.find_best_match(vector, mymap.weights)
        x = mymap.positions[match]     
        x = fn.to_int(x)
        w = words[x[0]][x[1]]
        if w == "" or overwrite:
            if overwrite:
                winner = fn.find_best_match(mymap.weights[match], mymap.vectors)
                w = keys[winner]
            else:
                w = keys[i]
        else:
            w = w + "," + keys[i]
        words[x[0]][x[1]] = w 
    word_plot(words)
    return words

def draw_neuron_activation(mymap, named=True, symbols=False):     # iterates through EACH neuron and finds closest vector
    words = distances = empty_list(mymap.size, 1)

    if named:
        vectors = mymap.vectors
        keys = mymap.keys
    else:
        vectors = []
        keys = []
        idea_names = mymap.space.idea_names
        for item in mymap.space.table:
            keys.append(idea_names[item])
            vectors.append(mymap.space.table[item])   

    if symbols:
        s = mymap.space.symbol_vectors
        keys = []
        vectors = []
        for item in s:
            keys.append(mymap.space.idea_names[item])
            vectors.append(s[item])

    for neuron in flatten(mymap.neurons):
        weight = neuron.weight
        match = fn.find_best_match(weight, vectors)
        distance = fn.distance(weight, vectors[match])
        x = neuron.position
        x = fn.to_int(x)
        words[x[0]][x[1]] = keys[match]
        #       distances[x[0]][x[1]] = distance
    word_plot(words)
    return words

def draw_clusters(mymap, clusters):
    cluster_map = empty_list(mymap.size, 1) 

    vectors = mymap.vectors
    keys = mymap.keys

    for neuron in flatten(mymap.neurons):
        weight = neuron.weight
        match = fn.find_best_match(weight, vectors)
        key = keys[match]
        cluster = clusters[key]
        x = neuron.position
        x = fn.to_int(x)
#        cluster_map[x[0]][x[1]] = key
        cluster_map[x[0]][x[1]] = cluster
    return cluster_map

def draw_clusters_per_item(mymap, clusters):
    cluster_map = empty_list(mymap.size, 1) 

    vectors = mymap.vectors
    keys = mymap.keys

    for neuron in flatten(mymap.neurons):
        weight = neuron.weight
        match = fn.find_best_match(weight, vectors)
        key = keys[match]
        cluster = clusters[key]
        x = neuron.position
        x = fn.to_int(x)
        cluster_map[x[0]][x[1]] = key
#        cluster_map[x[0]][x[1]] = cluster
    return cluster_map

def get_distances_to_nearest(mymap):
    distances = empty_list(mymap.size, 1)
    vectors = mymap.vectors
    matches = []
    for neuron in flatten(mymap.neurons):
        weight = neuron.weight
        match = fn.find_best_match(weight, vectors)
        matches.append(match)
        distance = fn.distance(weight, vectors[match])
        x = neuron.position
        x = fn.to_int(x)
        distances[x[0]][x[1]] = distance
    c = Counter(matches)
    print c 
    print 'items mapped : ' + str(len(sorted(c)))
    return distances

def get_umatrix(mymap, radius=1):
    umatrix = empty_list(mymap.size, 1)

    xmax = mymap.size[1]
    ymax = mymap.size[0]    

    rad = range(-radius, radius + 1)
#    print rad

    for neuron in flatten(mymap.neurons):
        weight = neuron.weight
        position = neuron.position
        x = position[0]
        y = position[1]
        xrange = []
        yrange = []
  
        for i in rad:
            xrange.append(int((x + i) % xmax))
            yrange.append(int((y + i) % ymax))

        average_dist = 0
        for x in xrange:
            for y in yrange:
                neighbour_weight = mymap.neurons[x][y].weight                
                d = fn.distance(neighbour_weight, weight)   
                average_dist += d
        
        umatrix[x][y] = average_dist 
    return umatrix
    
def create_idea_names(space):
    idea_names = {}
    for item in space.table:
        name = ""
        for i, element in enumerate(space.table[item]):     
            word = space.words[i]         
            word = re.sub("\"", "", str(word))
            if element > 0 : 
                if len(name) == 0: 
                    name = name + word  
                else: 
                    name = name + "+" + word
        idea_names[item] = name
    return idea_names 

def empty_list(shape, i):
    x = []
    for n in range(shape[i]):
        if i == 0:
            x.append("")
        else:
            x.append(empty_list(shape, i - 1))
    return x