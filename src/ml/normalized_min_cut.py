#!/usr/local/bin/python
# coding: UTF-8

# released under bsd licence
# see LICENCE file or http://www.opensource.org/licenses/bsd-license.php for details
# Institute of Applied Simulation (ZHAW)
# Author Thomas Niederberger

import networkx as nx
import numpy as np

def normalized_min_cut(graph):
    """Clusters graph nodes according to normalized minimum cut algorithm.
    All nodes must have at least 1 edge. Uses zero as decision boundary. 
    
    Parameters
    -----------
        graph: a networkx graph to cluster
        
    Returns
    -----------
        vector containing -1 or 1 for every node
    References
    ----------
        J. Shi and J. Malik, *Normalized Cuts and Image Segmentation*, 
        IEEE Transactions on Pattern Analysis and Machine Learning, vol. 22, pp. 888-905
    """
    m_adjacency = np.array(nx.to_numpy_matrix(graph))

    D = np.diag(np.sum(m_adjacency, 0))
    D_half_inv = np.diag(1.0/np.sqrt(np.sum(m_adjacency, 0)))
    M = np.dot(D_half_inv, np.dot((D - m_adjacency), D_half_inv))

    (w, v) = np.linalg.eig(M)
    #find index of second smallest eigenvalue
    index = np.argsort(w)[1]
    
    v_partition = v[:, index]
    v_partition = np.sign(v_partition)
    return v_partition
    
    
if __name__ == "__main__":
    #create graph
    #graph = nx.tutte_graph()
    graph = nx.barbell_graph(10, 0)
    #add some additional edges
    graph.add_edge(3, 13)
    graph.add_edge(4, 13)    
    #graph = nx.lollipop_graph(10, 10)
    
    v_partition = normalized_min_cut(graph)
    colors = np.zeros((len(v_partition), 3)) + 1.0
    colors[:, 2]=np.where(v_partition >= 0, 1.0, 0)
    
    nx.draw(graph, node_color=colors)