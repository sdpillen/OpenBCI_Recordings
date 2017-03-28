"""
Wrapper methods for assertions.
"""

def assert_equal(val1, val2, message=''):
    assert val1 == val2, '%s -- %s, %s' % (str(message), str(val1), str(val2))

def assert_not_equal(val1, val2):
    assert val1 != val2, '%s, %s' % (str(val1), str(val2))

def assert_less(val_less, val_greater):
    assert val_less < val_greater, '%s, %s' % (str(val_less), str(val_greater))

def assert_less_or_equal(val_less, val_greater):
    assert val_less <= val_greater, '%s, %s' % (str(val_less), str(val_greater))

def assert_greater(val_greater, val_less):
    assert val_greater > val_less, '%s, %s' % (str(val_greater), str(val_less))

def assert_greater_or_equal(val_greater, val_less):
    assert val_greater >= val_less, '%s, %s' % (str(val_greater), str(val_less))

def assert_epoch_label_shape(epoched_values, labels, message="The number of epochs between the density and labels do not match"):
    """
    Asserts that the number of epochs in the density has the same length as the labels
    :param epoched_values: numpy array - epoched values where the first dimension is the number of epoch (such as density)
    :param labels: labels - list or 1D np array
    :param message: Message to show if assertion fails.
    """
    assert epoched_values.shape[0] == len(labels), str(message) + '-- Density: %d, Labels: %d' % (epoched_values.shape[0], len(labels))
