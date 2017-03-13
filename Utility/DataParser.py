import numpy as np
import AssertVal as AV
import time
import bisect
import ast

def epoch_data(eeg_indexes, raw_data, trial_starts, trial_stops):
    """
    Takes raw data of shape [sample, channel] and returns epoched data of shape [epoch, sample channel].
    The epoches are taken according to the indexing of the start and stop values in the eeg indexes

    :param eeg_indexes: epoch index for each sample in raw data (eeg index or time)
    :param raw_data: data shape [sample, channel]
    :param trial_starts: lst of trial start values (eeg index or time)
    :param trial_stops: lst of trial start values (eeg index or time)
    :return:
    """
    AV.assert_equal(len(eeg_indexes), raw_data.shape[0])
    AV.assert_equal(len(trial_starts), len(trial_stops))
    epoched_data = None
    for start_stop_index in xrange(len(trial_starts)):
        start_packet_index = bisect.bisect_right(eeg_indexes, trial_starts[start_stop_index])
        end_packet_index = bisect.bisect_left(eeg_indexes, trial_stops[start_stop_index])
        AV.assert_less(start_packet_index, end_packet_index)
        trial_epoched_data = np.expand_dims(raw_data[start_packet_index:end_packet_index], axis=0)
        try:
            epoched_data = trial_epoched_data if epoched_data is None else np.concatenate((epoched_data, trial_epoched_data), axis=0)
        except ValueError:
            print 'Epoched data shape', epoched_data.shape, 'Trial Epoched data shape', trial_epoched_data.shape
            raise
    AV.assert_equal(len(trial_stops), epoched_data.shape[0])
    return epoched_data

def extract_min_difference_in_list(lst):
    """
    Takes a list and extracts the minimum difference between consecutive items.
    For example
        [3, 5, 125, 23543]
    Would return 2
    :param lst: List of numbers to be examined. List must be in nonmonitonic ascending order
    """
    min_val = float('inf')
    for index in xrange(len(lst) - 1):
        diff = lst[index + 1] - lst[index]
        min_val = min(diff, min_val)
    return min_val

def extract_min_difference_between_lists(lst_large, lst_small):
    """
    Takes a list and extracts the minimum difference between two lists.
    For example
        [3, 5, 125, 23543]
        [1, 4, 120, 2354]
    Would return 1
    """
    AV.assert_equal(len(lst_large), len(lst_small))
    return min([a_i - b_i for a_i, b_i in zip(lst_large, lst_small)])


def extract_value_from_list_of_dicts(dictionary_list, key):
    """
    Iterates through a given dictionary for key in key order and returns a list of values for that key order
    :param dictionary_list: Dictionary list to extract values for (in order)
    :param key: Key to access in the dictionary
    :return: List of values extracted from the dictionary of length len(key_order).
    """
    return [dictionary[key] for dictionary in dictionary_list]

def convert_ununiform_start_stop_lists_to_uniform_start_stop_lists(start_lst, stop_lst):
    """
    Takes a list of start indexes and a list of end indexes a returns a new end index list such that trial_dur = stop_lst[i] - start_lst[i] and trial dur is the same for
    each list (set to the minimum trial dur contained in the list)
    :param start_lst: list of floats denoting starts of trials
    :param stop_lst: list of floats denoting end of trials
    :return: new stop list
    """
    AV.assert_equal(len(start_lst), len(stop_lst))
    dur = extract_min_difference_between_lists(stop_lst, start_lst)
    return [start_lst_val + dur for start_lst_val in start_lst]


def stack_epochs(existing, new_trial):
    """
    Takes existing epoch epoched data (shape epoch, sample trial) and concats a new trial along the first axis.
    If existing is none, returns new trial.
    """
    return new_trial if existing is None else np.concatenate((existing, new_trial), axis=0)

def stack_lists(existing, new_list):
    """
    Takes existing epoch list and concats a new list to the end.
    If existing is none, returns new list.
    """
    return new_list if existing is None else existing + new_list


def average_density_over_epochs(density):
    """
    Takes our densioty of shape (epoch, sample, channel) and averages over all trials.

    :param density: Spectral density of the form (epoch, sample, channel)
    :return: New density of the form (1, sample, channel), where the sample dimension is averaged over epoch
    """

    # Assert density is of the form (epoch, sample, channel)
    assert len(density.shape) == 3

    num_samples = density.shape[1]
    num_channles = density.shape[2]
    averaged = np.average(density, axis=0)

    # restore our epoch dim.
    averaged = np.expand_dims(averaged, axis=0)

    # Ensure we didn't change any unwanted dims.  Only num_epochs (dim 0) should change.
    AV.assert_equal(num_samples, averaged.shape[1])
    AV.assert_equal(num_channles, averaged.shape[2])
    return averaged


def trim_freqs(freqs, density, high=None, low=None):
    """
    Takes freqs and density and trims them according to the high and low values.
    :param freqs: freqs
    :param density: density (shape epoch sample channel)
    :param high: removes all freqs above this val (inclusive). Cast to int if passed a float.
    :param low: removes all freqs below this val (inclusive).  Cast to int if passed a float.
    :return: freqs, density
            Both elements are modified. Lenght of freqs is equal to the size of the first axis of density (samples).
    """
    original_num_samples = density.shape[1]
    assert len(density.shape) == 3
    if high is None and low is None:
        raise ValueError('High or low must be an int')

    if high is not None:
        high = int(high)

        index_of_high = bisect.bisect_left(a=freqs, x=high)
        freqs = freqs[:index_of_high]
        density = density[:, :index_of_high, :]
    if low is not None:
        low = int(low)
        index_of_low = bisect.bisect_left(a=freqs, x=low)
        freqs = freqs[index_of_low:]
        density = density[:, index_of_low:, :]
    # Assure we trimmed something
    AV.assert_not_equal(original_num_samples, density.shape[1])
    # Ensure each density pos has a corresponding freq.
    AV.assert_equal(len(freqs), density.shape[1])
    return freqs, density








