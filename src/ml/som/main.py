# released under bsd licence
# see LICENSE file or http://www.opensource.org/licenses/bsd-license.php for details
# Institute of Applied Simulation (ZHAW)
# Author Timo Jeranko

from file_operations import *
from functions import *
import pickle
from visualize import *
from plot_graphs import *

# read file
named = False
space,clusters = read_file("input.dat",named=False,clustered=True)

#space = read_file("input.dat",named=named)
space.remove_zero_vectors()

#space.pca_reduce(64)
#print space.getmatrix()

#space.add_symbol_vectors(0.1)

# initialize Map
mymap = Map([15,15],space)

# iterate
mymap.init_optimization()
#print mymap.get_weight_indexes(aa,2)
mymap.iterate0(10000)

#mymap = load_map("002")
#words = draw_basis_activation(mymap)
cluster_map =  draw_clusters(mymap,clusters)

#words = draw_item_activation(mymap,named=True,overwrite=False,symbols=False)
#words = draw_neuron_activation(mymap,named=named,symbols=True)
#print distances

distances = get_distances_to_nearest(mymap)
#umatrix = get_umatrix(mymap,radius=1)

#shade_map(umatrix)
#shade_map(distances)
#shade_map_clusters(umatrix,cluster_map)
shade_map_clusters(distances,cluster_map)

print "\n"
print "average distance to best matching unit:", mymap.average_distance_to_bmu0()
print "\n"

save_map(mymap,"002")