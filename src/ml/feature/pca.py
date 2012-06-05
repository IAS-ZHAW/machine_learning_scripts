# released under bsd licence
# see LICENSE file or http://www.opensource.org/licenses/bsd-license.php for details
# Institute of Applied Simulation (ZHAW)
# Author Thomas Niederberger

import numpy as np
from scipy import *
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import svds 
import scipy.linalg as linalg

def pca(data, dimensions = 2):
    """calculates a PCA of the specified dataset. 
    
    Parameters
    ----------
    data : array_like
        dense data matrix which is supposed to have dataitems in the rows and features in the columns.
    dimensions : int, optional
        number of dimensions (default = 2) to consider in the PCA
        
    Returns
    -------
    loc : ndarray
        PCA matrix of shape (# of dataitems, dimensions)
    """
    indices = np.sum(data > 0, 0)
    data = data[:, indices > 1.0]
    covariance = np.cov(np.transpose(data))
    u_matrix, lambda_matrix, v_matrix = svds(csr_matrix(covariance), k=dimensions)
    #u_matrix, lambda_matrix, v_matrix = np.linalg.svd(covariance)
    
    # remove means from original data
    no_means_data = data - np.mean(data, 0)

    #loc = np.dot(u_matrix[:, 0:dimensions].T, no_means_data.T).T
    loc = np.transpose(np.dot(np.transpose(u_matrix[:, 0:dimensions]), np.transpose(no_means_data)))
    
    return (lambda_matrix, loc, u_matrix[:, 0:dimensions])

def retained_variance(singular_values, dim):
    """Calculate how much variance (in percent) is retained when reducing the number of dimensions to dim"""
    return np.sum(singular_values[0:dim]) / np.sum(singular_values)

def mds(dist, dimensions = 2):
    n = len(dist[:,1])
    squared = dist ** 2
    
    J = np.eye(n) - np.ones(n, 'float')/n
    B = -1.0/2.0 * np.dot(np.dot(J, squared), J)
    
    u_matrix, val, v_matrix = np.linalg.svd(B)
    
    val = np.abs(val) #taking absolute values in case of negative eigenvalues occur. Not sure whether this is allowed
    principal_component_indices = np.flipud(np.argsort(val)[(n-dimensions):n])
    loc = np.dot(u_matrix[:, principal_component_indices], np.sqrt(np.diag(val[principal_component_indices])))
    return (val, loc, u_matrix[:, principal_component_indices])