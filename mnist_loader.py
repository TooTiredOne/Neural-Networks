"""
mnist_loader
~~~~~~~~~~~~

A library to load the MNIST image data.  For details of the data
structures that are returned, see the doc strings for ``load_data``
and ``load_data_wrapper``.  In practice, ``load_data_wrapper`` is the
function usually called by our neural network code.
"""

#### Libraries
# Standard library
#import pickle as cPickle
#import gzip
from keras.datasets import mnist
#import mnist_loader
from sklearn.preprocessing import StandardScaler

# Third-party libraries
import numpy as np
def load_data():
    """Return the MNIST data as a tuple containing the training data
    and the test data.

    The ``training_data`` is returned as a tuple with two entries.
    * The 1st entry contains the actual training images. 
        - It's a numpy array with shape (60000, 28, 28)
        - Each entry is, in turn, a numpy ndarray with 784 values, 
          representing the 28 * 28 = 784 pixels in a single MNIST image.

    * The 2nd entry in the ``training_data`` containts labels 
        - It's a numpy ndarray with shape (60000,).  
        - Those entries are just the digit values (0...9) for the corresponding 
          images contained in the first entry of the tuple.

    The ``test_data`` is similar, except it contains only 10,000 images and labels.

    This is a nice data format, but for use in neural networks it's
    helpful to modify the format of the ``training_data`` a little.
    That's done in the wrapper function ``load_data_wrapper()``, see
    below.
    """
    training_data, test_data = mnist.load_data()
    return (training_data, test_data)

def load_data_wrapper():
    """Return a tuple containing ``(training_data, test_data)``. 
    Based on ``load_data``, but the format is more
    convenient for use in our implementation of neural networks.

    In particular, ``training_data`` is a list containing 50,000
    2-tuples ``(x, y)``.  ``x`` is a 784-dimensional numpy.ndarray
    containing the input image.  ``y`` is a 10-dimensional
    numpy.ndarray representing the unit vector corresponding to the
    correct digit for ``x``.

   ``test_data`` is a list containing 10,000
    2-tuples ``(x, y)``.  In each case, ``x`` is a 784-dimensional
    numpy.ndarry containing the input image, and ``y`` is the
    corresponding classification, i.e., the digit values (integers)
    corresponding to ``x``.

    Obviously, this means we're using slightly different formats for
    the training data and the test data.  These formats
    turn out to be the most convenient for use in our neural network
    code."""
    
    tr_d, te_d = load_data()
    training_inputs = [x.reshape(784, 1).astype(np.float32) for x in tr_d[0]]
    training_inputs = [StandardScaler().fit_transform(x) for x in training_inputs]
    training_results = [vectorized_result(y) for y in tr_d[1]]
    training_data = list(zip(training_inputs, training_results))
    test_inputs = [np.reshape(x, (784, 1)) for x in te_d[0]]
    test_data = list(zip(test_inputs, te_d[1]))
    return (training_data, test_data)

def vectorized_result(j):
    """Return a 10-dimensional unit vector with a 1.0 in the jth
    position and zeroes elsewhere.  
    
    This is used to convert a digit(0...9) into a corresponding 
    desired output from the neural network."""
    
    e = np.zeros((10, 1))
    e[j] = 1.0
    return e