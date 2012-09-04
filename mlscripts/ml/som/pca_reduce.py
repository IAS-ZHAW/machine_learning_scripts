# released under bsd licence
# see LICENSE file or http://www.opensource.org/licenses/bsd-license.php for details
# Institute of Applied Simulation (ZHAW)
# Author Timo Jeranko

from mlscripts.ml.som.file_operations import *
from mlscripts.ml.som.functions import *
import pickle
import scipy
from mlscripts.ml.som.visualize import *
from mlscripts.ml.feature.pca import *
import scipy.sparse as sparse

# read file
matrix = read_file2("input.dat")
matrix = csc_matrix(matrix)

transform = pca(matrix,2)
transform= scipy.array(transform)
 
def printmatrix(matrix):
    for row in matrix:
        last = len(row) - 1
        for i,x in enumerate(row):
            print x,
            if i != last:
                print ";",
        print ""

printmatrix(transform)
