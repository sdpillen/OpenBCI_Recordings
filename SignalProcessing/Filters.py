import scipy.signal as scisig
from scipy.fftpack import rfft, irfft, fftfreq


class Butter(object):
    """
    Class for Butter Filters
    """

    @staticmethod
    def butter_bandpass(low, high, fs, order=5):
        """
        Wrapper function for the scipy butter
        :param low: Frequency to filter above
        :param high: Frequency to filter below
        :param fs: Sampling rate (hz)
        :param order: Order of filter to use (default = 5)
        :return: Numerator (b) and denominator (a) polynomials of the IIR filter
        """
        nyq = 0.5 * fs
        b, a = scisig.butter(order, [low / nyq, high / nyq], btype='band')
        return b, a

    @staticmethod
    def butter_bandpass_filter(data, low, high, fs, order=5):
        """
        Filters passed data with a bandpass butter function
        :param data: data to be bandpass filtered
        :param low: Frequency to filter above
        :param high: Frequency to filter below
        :param fs: Sampling rate (hz)
        :param order: Order of filter to use (default = 5)
        :return: filtered data (and modifies original data).
        """
        b, a = Butter.butter_bandpass(low, high, fs, order=order)
        return scisig.lfilter(b, a, data)


def filter_noise(signal, fs):
    W = fftfreq(len(signal), d=1.0 / fs)
    f_signal = rfft(signal)
    low = 5
    f_signal[(W < low)] = 0
    for i in range(len(f_signal)):
        if 3 < W[i] < 65 or W[i] < low:
            f_signal[i] = 0
    cut_signal = irfft(f_signal)
    return cut_signal
