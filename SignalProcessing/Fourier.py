"""
Functions related to the fourier transform.
"""

import scipy.signal as scisig
import bisect
import matplotlib.pyplot as plt
import numpy as np


def get_channel_fft(single_channel_signal, fs, nperseg, noverlap, filter_sig=False, filter_above=40, filter_below=1):
    """ Returns frequencies and densities from the welch algorithm filtered as appropriate
    """
    freqs, density = scisig.welch(single_channel_signal, fs=fs, nperseg=nperseg, noverlap=noverlap)
    if filter_sig:
        low_index = bisect.bisect_left(freqs, filter_below)
        high_index = bisect.bisect_right(freqs, filter_above)
        freqs = freqs[low_index:high_index]
        density = density[low_index:high_index]
    return freqs, density


def get_fft_all_channels(data, fs, nperseg, noverlap):
    """
    Returns a np array of densities - shape(epoch, density, channel) and the frequency list
    :param data: Must be of the form (epoch, sample, channel)
    :param fs: sampling rate
    :param nperseg: nperseg for welch
    :param noverlap: noverlap for welch
    :return: freqs, np array of densities - shape(epoch, density, channel)
    """
    num_channels = data.shape[2]
    dens, freqs = [], None
    for chan in range(num_channels):
        freqs, density = scisig.welch(data[:, :, chan], fs=fs, nperseg=nperseg, noverlap=noverlap, axis=1)
        dens.append(density)
    return freqs, np.swapaxes(np.swapaxes(np.asarray(dens), 0, 1), 1, 2)


def band_power(freqs, density, inclusive_range):
    """
    Calculates the band power for the passed frequency spectrum
    :param freqs: List of frequencies
    :param density: Densities of the corresponding frequencies
    :param inclusive_range: Inclusive range to calculate the band power over
    :return: Unnormalized Band power over the given range - shape -> (epoch, channel)
    """
    low, high = inclusive_range
    low_index = bisect.bisect_left(freqs, low)
    high_index = bisect.bisect_right(freqs, high)
    # density -> shape (epoch, density)
    # high index is noninclusive when indexing a np array, add 1 to account for this.
    # Square the density
    powers = np.square(density[:, low_index:high_index + 1])  # density[:, low_index:high_index + 1] #
    # Sum up the power
    power = np.sum(powers, axis=1)
    # power.shape -> (epoch, channel)
    return power


def get_typical_channel_band_power(freqs, density):
    """
    Returns the band power of standard frequencies
    :param freqs: frequencies
    :param density: Frequency densities
    :return: delta, theta, alpha, low_beta, high_beta
    """
    # Get the band powers of delta, theta, alpha, low_beta, high_beta
    # delta is a np array of shape [epoch, channel]
    delta = band_power(freqs, density, (1, 4))
    theta = band_power(freqs, density, (4, 8))
    alpha = band_power(freqs, density, (8, 12))
    low_beta = band_power(freqs, density, (12, 20))
    high_beta = band_power(freqs, density, (30, 40))
    # Return the values as a tuple.
    return delta, theta, alpha, low_beta, high_beta
