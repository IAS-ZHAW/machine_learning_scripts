# released under bsd licence
# see LICENSE file or http://www.opensource.org/licenses/bsd-license.php for details
# Institute of Applied Simulation (ZHAW)
# Author Thomas Niederberger

from scipy import *
from scipy.sparse import *
import scipy.linalg as linalg

def pca(data, dimensions = 2):
    """calculates a PCA of the specified dataset. 
    
    Parameters
    ----------
    data : array_like
        sparse data matrix which is supposed to have dataitems in the rows and features in the columns.
    dimensions : int, optional
        number of dimensions (default = 2) to consider in the PCA 
        
    Returns
    -------
    loc : ndarray
        PCA matrix of shape (# of dataitems, dimensions)
    """
    covariance = cov(transpose(data.todense()))
    u_matrix, lambda_matrix, v_matrix = linalg.svd(covariance)
    
    # remove means from original data
    noMeansData = data - mean(data.todense(), 0)

    loc = transpose(dot(transpose(u_matrix[:, 0:dimensions]), transpose(noMeansData)))
    return loc
