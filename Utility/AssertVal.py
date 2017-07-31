"""
Wrapper methods for assertions.
"""


def assert_equal(val1, val2):
    """
    Runs assertion and displays values if assertion fails.
    """
    assert val1 == val2, 'Error: %s and %s should be EQUAL!' % (str(val1), str(val2))


def assert_not_equal(val1, val2):
    """
    Runs assertion and displays values if assertion fails.
    """
    assert val1 != val2, 'Error: %s and %s should NOT be equal!' % (str(val1), str(val2))


def assert_less(val_less, val_greater):
    """
    Runs assertion and displays values if assertion fails.
    """
    assert val_less < val_greater, 'Error: %s should be LESS than %s' % (str(val_less), str(val_greater))


def assert_less_or_equal(val_less, val_greater):
    """
    Runs assertion and displays values if assertion fails.
    """
    assert val_less <= val_greater, 'Error: %s should be LESS THAN OR EQUAL TO %s' % (str(val_less), str(val_greater))


def assert_greater(val_greater, val_less):
    """
    Runs assertion and displays values if assertion fails.
    """
    assert val_greater > val_less, 'Error: %s should be GREATER than %s' % (str(val_greater), str(val_less))


def assert_greater_or_equal(val_greater, val_less):
    """
    Runs assertion and displays values if assertion fails.
    """
    assert val_greater >= val_less, 'Error: %s should be GREATER THAN OR EQUAL TO %s' % (str(val_greater),
                                                                                         str(val_less))


def assert_epoch_label_shape(epoched_values, labels, message="The number of epochs between the density and labels don't match"):
    """
    Asserts that the number of epochs in the density has the same length as the labels
    :param epoched_values: numpy array - epoched values where the first dimension is the number of epoch (such as density)
    :param labels: labels - list or 1D np array
    :param message: Message to show if assertion fails.
    """
    assert epoched_values.shape[0] == len(labels), str(message) + '-- Density: %d, Labels: %d' % (epoched_values.shape[0], len(labels))


def assert_none(val1, message=''):
    """
    Runs assertion and displays value if assertion fails.
    """
    assert val1 is None , '%s -- %s' % (str(message), str(val1))


def assert_type(val1, type, message='Invalid types:'):
    assert type(val1) is type, message + '%s -- %s is type %s, not type %s' % (str(message), str(val1), type(val1), str(type))
