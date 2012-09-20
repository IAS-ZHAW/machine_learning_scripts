import unittest

from feature_reduction import *
from numpy import *
from numpy.testing import *
    
class TestFeatureReduction(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_pca(self):
        data = array([[-1, -3, 1, 3], [-1, -3, 1, 3]])
        projected = pca(data.T, 1)
        correct = array([[np.sqrt(2.0)], [np.sqrt(18.0)], [-np.sqrt(2.0)], [-np.sqrt(18.0)]])
        assert_array_almost_equal(projected, correct, 4)
        
        projected = pca(data.T, 2)
        correct = array([[np.sqrt(2.0), 0.0], [np.sqrt(18.0), 0.0], [-np.sqrt(2.0), 0.0], [-np.sqrt(18.0), 0.0]])
        assert_array_almost_equal(projected, correct, 4)

        data = array([[-1, -3, 1, 3, 3], [-1, -3, 1, 3, 5]])
if __name__ == '__main__': unittest.main()