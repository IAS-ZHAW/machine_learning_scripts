# released under bsd licence
# see LICENSE file or http://www.opensource.org/licenses/bsd-license.php for details
# Institute of Applied Simulation (ZHAW)
# Author Timo Jeranko

from mlscripts.ml.som.file_operations import *
from mlscripts.ml.som.functions import *
import pickle
from mlscripts.ml.som.visualize import *
from mlscripts.ml.som.plot_graphs import *

# read file
named = False
#space,clusters = read_file("input.dat",named=False,clustered=True)
space, clusters = read_file(r"C:\Daten\atizo\data-repo\tf\out-tf-project-8881.csv",named=False,clustered=True, delimiter=' ')

#space = read_file("input.dat",named=named)
space.remove_zero_vectors()

#space.pca_reduce(64)
#print space.getmatrix()

#space.add_symbol_vectors(0.1)

# initialize Map
mymap = Map([20,20],space)

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
