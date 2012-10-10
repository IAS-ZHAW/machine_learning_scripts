import unittest

from mlscripts.ml.cluster_validation import *
from scipy.spatial.distance import pdist, squareform

from pylab import *
from numpy import *
from numpy.testing import *
import logging

class TestClusterValidation(unittest.TestCase):
    def setUp(self):
        pass

    def test_jaccard_index(self):
        index = jaccard_index([1, 3, 5, 6], [3, 2, 6, 1, 8])
        self.assertEquals(index, 3.0 / 6)
        index = jaccard_index([0, 1, 5], [5, 1, 5, 5, 5])
        self.assertEquals(index, 2.0 / 3)

    def test_confusion_matrix(self):
        conf_matrix = confusion_matrix([[1, 3, 5, 6], [8]], [[3, 2, 6, 1, 8]])
        correct = array([[3.0 / 6], [1.0 / 5]])
        self.assertTrue(array_equal(conf_matrix, correct))
        conf_matrix = confusion_matrix([[1, 3, 5, 6], [8]], [[3, 2, 6, 1, 8], [1, 3, 8]])
        correct = array([[3.0 / 6, 2.0 / 5], [1.0 / 5, 1.0 / 3]])
        self.assertTrue(array_equal(conf_matrix, correct))

if __name__ == '__main__':
    logging.basicConfig()
    unittest.main()
