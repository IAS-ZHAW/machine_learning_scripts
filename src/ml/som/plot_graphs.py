# released under bsd license
# see LICENSE file or http://www.opensource.org/licenses/bsd-license.php for details
# Institute of Applied Simulation (ZHAW)
# Author Timo Jeranko

import scipy.interpolate as interpolate
import matplotlib.pyplot as pyplot
import matplotlib.cm as cm
from scipy import *
import random
from visualize import *
from flatten import *

def shade_map(distances):
    im = pyplot.imshow(distances,interpolation="nearest",cmap=cm.gray,origin='lower')
    pyplot.show()

def shade_map_clusters(distances,cluster_map):
    im = pyplot.imshow(distances,interpolation='nearest',cmap=cm.gray,origin='lower')    
    pyplot.show()
    #pyplot.figure()
    print distances
    
    cluster_color_map = convert_cluster_map(cluster_map)
    
    pyplot.imshow(cluster_color_map,interpolation='nearest',alpha=0.5,origin='lower')

    pyplot.show()

def get_clusters(cluster_map):
    out = []
    for row in cluster_map:
        for name in row:
            if name not in out:
                out.append(name)
    return out 
    
def convert_cluster_map(cluster_map):
    clusters = get_clusters(cluster_map)
    x = len(clusters)
    delta = 1.0/x
    colors = []
    color = 0
    for i in range(x):
        color += delta    
        colors.append(color)
#    print "colors", colors
    out = []
    for row in cluster_map:
        outrow = []
        for name in row:
            i = clusters.index(name)
            outrow.append(colors[i]) 
        out.append(outrow)
    return out

def shade_map_structured(words,distances):
    im = pyplot.imshow(distances,interpolation='nearest',cmap=cm.gray,origin='lower')

    for i,row in enumerate(words):
        for j,word in enumerate(row):
            if word != "":
                pyplot.text(j,i,word,fontsize=8).set_color('red')
#               pyplot.annotate(word,xy=(j,i)).set_color('red')
    pyplot.show()

def get_spline():
    print 0
#    f = interpolate.LSQBivariateSpline(x,y,z,tx,ty)
    

