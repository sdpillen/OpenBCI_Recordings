"""
============================
A m p l i f i e r  S e t u p
============================

Default Sampling Rate - 5000 Fs
Number of channels: 32 (includeing ECG channel)
Sampling Interval [micro seconds]: 200  (0.0002 seconds; 5000 Hz)

Packet size = 100 samples
Packet arrival = 50 Hz

See DLUtil/Documentation/BrainAmp for more information on how to use the Brain Amp interface.

This script is a modified Python RDA client for the RDA tcpip interface of the BrainVision Recorder. The unmodified file is
within this same folder.

"""

# Todo  This script has 32 channels hard-coded.  This needs to be fixed to work with other numbers.

# needs socket and struct library
from socket import *
from struct import *
import time
import Queue
import threading
import DataSaver
import numpy as np
import EEG_INDEX


class Marker:
    """Marker class for storing marker information"""
    def __init__(self):
        self.position = 0
        self.points = 0
        self.channel = -1
        self.type = ""
        self.description = ""


class DataCollect(object):

    def __init__(self, subject_data_path, channels_for_live, process_queue, subject_name=None, subject_tracking_number=None, experiment_number=None):
        """
        A data collection object for the Brain Amp interface.  This provides option for live data streaming and saving data to file.

        For live data streaming, use with a threading or multiprocessing queue (ie. Queue.queue().
           Data will be put on the queue, which can be read by another thread.)

        Modifies the EEG_INDEX and EEG_INDEX_2 in DLUtil/EEGInterface/EEG_INDEX.py when each packet arrives.  These variables can be read from any thread.
            Use this to time mark events in your other programs.

        :param subject_data_path: Path to save the save the data.  If None, no data will be saved.
        :param channels_for_live: List of channel names (or indexes) to put on the process_queue.
        :param process_queue: The channels_for_live channel data will be placed on this queue if it is not None.
        :param subject_name: Optional -- Name of the subject. Defaults to 'None'
        :param subject_tracking_number: Optional -- Subject Tracking Number (AKA TMS group experiment number tracker). Defaults to 'None'
        :param experiment_number: Optional -- Experimental number. Defaults to 'None'
        """
        # Typical 32 channels for live (take from signal tester)
        # ['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4', 'P3', 'P4', 'O1', 'O2', 'F7', 'F8', 'T7', 'T8', 'P7', 'P8', 'Fz', 'Cz',
        #  'Pz', 'Oz', 'FC1', 'FC2', 'CP1', 'CP2', 'FC5', 'FC6', 'CP5', 'CP6', 'TP9', 'TP10', 'POz', 'ECG']

        self.data_save_queue = None
        if subject_data_path is not None:
            self.data_save_queue = Queue.Queue()
            threading.Thread(target=lambda: DataSaver.start_data_saving(subject_data_path, self.data_save_queue, header=None)).start()
        self.collect_data = True
        self.subject_data_path = subject_data_path

        self.subject_data_path = subject_data_path
        self.subject_name= str(subject_name) if subject_name is not None else "None"
        self.subject_number = str(subject_tracking_number) if subject_tracking_number is not None else 'None'
        self.experiment_number = str(experiment_number) if experiment_number is not None else 'None'

        # Count each block we recieve
        self.data_index = -1

        # A separate queue (other than the one for storing data) that puts the channels_for_live data points on
        self.process_queue = process_queue

        # block counter to check overflows of tcpip buffer
        self.last_block = -1

        self.put_data_on_process_queue = False
        self.channels_for_live = channels_for_live

        # Create a tcpip socket
        self.con = socket(AF_INET, SOCK_STREAM)
        # Connect to recorder host via 32Bit RDA-port
        # adapt to your host, if recorder is not running on local machine
        # change port to 51234 to connect to 16Bit RDA-port

        try:
            self.con.connect(("localhost", 51244))
        except:
            print "--Ensure that the BrainVision software is on and the dongle is plugged in and functioning."
            print "See DLUtil Documentation for instructions on how to run the BrainVision EEG system --"
            raise

    @staticmethod
    def recv_data(socket, requestedSize):
        # Helper function for receiving whole message
        returnStream = ''
        while len(returnStream) < requestedSize:
            databytes = socket.recv(requestedSize - len(returnStream))
            if databytes == '':
                raise RuntimeError("connection broken")
            returnStream += databytes

        return returnStream

    @staticmethod
    def split_string(raw):
        """
          Helper function for splitting a raw array of
          zero terminated strings (C) into an array of python strings
        """
        stringlist = []
        s = ""
        for i in range(len(raw)):
            if raw[i] != '\x00':
                s = s + raw[i]
            else:
                stringlist.append(s)
                s = ""

        return stringlist

    @staticmethod
    def get_properties(rawdata):
        # Helper function for extracting eeg properties from a raw data array
        # read from tcpip socket

        # Extract numerical data
        (channelCount, samplingInterval) = unpack('<Ld', rawdata[:12])
        print channelCount
        # Extract resolutions
        resolutions = []
        for c in range(channelCount):
            index = 12 + c * 8
            restuple = unpack('<d', rawdata[index:index+8])
            resolutions.append(restuple[0])

        # Extract channel names
        channelNames = DataCollect.split_string(rawdata[12 + 8 * channelCount:])

        return channelCount, samplingInterval, resolutions, channelNames

    @staticmethod
    def get_data(rawdata, channelCount):
        # Helper function for extracting eeg and marker data from a raw data array
        # read from tcpip socket

        # Extract numerical data
        (block, points, markerCount) = unpack('<LLL', rawdata[:12])

        # Extract eeg data as array of floats
        data = []
        for i in range(points * channelCount):
            index = 12 + 4 * i
            value = unpack('<f', rawdata[index:index+4])
            data.append(value[0])

        # Extract markers
        markers = []
        index = 12 + 4 * points * channelCount
        for m in range(markerCount):
            markersize = unpack('<L', rawdata[index:index+4])

            ma = Marker()
            (ma.position, ma.points, ma.channel) = unpack('<LLl', rawdata[index+4:index+16])
            typedesc = DataCollect.split_string(rawdata[index + 16:index + markersize[0]])
            ma.type = typedesc[0]
            ma.description = typedesc[1]

            markers.append(ma)
            index = index + markersize[0]
        return block, points, markerCount, data, markers

    def start_recording(self):
        """
        Start our recording
        """
        # data buffer for calculation, empty in beginning
        data1s = []

        # ##### Main Loop #### #
        while self.collect_data:
            raw_data, msgsize, msgtype = self.get_raw_data()
            # Perform action dependend on the message type
            if msgtype == 1:
                channel_count, sampling_interval, resolutions, channel_names, channel_dict, meta_info_str = self.first_message_actions(raw_data)
            elif msgtype == 4:
                # Data message, extract data and markers
                (block, points, marker_count, data, markers) = DataCollect.get_data(raw_data, channel_count)

                if self.data_index == 1:
                    print "Length of packet:", len(data)
                # Get the time we collected the sample
                data_recieve_time = time.time()
                self.data_index += 1  # Increase our sample counter

                EEG_INDEX.EEG_INDEX = self.data_index
                EEG_INDEX.EEG_INDEX_2 = self.data_index
                ######################
                # Check for overflow #
                ######################
                if self.last_block != -1 and block > self.last_block + 1:
                    print "*** Index: " + str(self.data_index) + "OVERFLOW with " + str(block - self.last_block) + " datablocks ***"
                    if self.subject_data_path is not None:
                        with open(self.subject_data_path + self.subject_name + '_Overflow.txt', 'a') as handle_f:
                            handle_f.write(str(self.data_index) + '\t' + str(block - self.last_block) + '\n')
                self.last_block = block
                self.print_marker_count(markers=marker_count, marker_count=marker_count)

                ###################
                # Handle the Data #
                ###################
                # Save the Data - We put data on the queue to be saved - format for queue (index, time, data)
                if self.data_save_queue is not None:
                    self.data_save_queue.put((self.data_index, data_recieve_time, data))
                if False:
                    # print len(data)
                    # Put data at the end of actual buffer
                    data1s.extend(data)
                    # If more than 1s of data is collected, calculate average power, print it and reset data buffer
                    data1s = self.calc_avg_power(data1s, channel_count, sampling_interval, resolutions)

                self.put_data_on_process_queue = True
                if self.put_data_on_process_queue:
                    self.handle_process_queue(data, resolutions, channel_count, channel_dict)

            elif msgtype == 3:
                self.con.close()  # Stop message, terminate program; Close tcpip connection
                break

    def handle_process_queue(self, data, resolutions, channel_count, channel_dict):
        """
        Number of channels: 32
        Sampling Rate [Hz]: 5000
        Sampling Interval [micro seconds]: 200  (0.0002 seconds; 5000 Hz)

        Packet size = 100 samples
        Packet arrival = 50 Hz
        """
        # We sample at 5000 Hz.  We want to down sample to 500 hz.  We collect data in packets of 100 samples
        # at 50 Hz. 100 * 50 = 5000
        # If we took a single sample from each packet, we would be sampling at 50 Hz.
        # Because we want to sample at 500 Hz, we need to take 10x as many samples, so for every packet,
        # we need to collect 10 data points out of the 100 (aka, we need to collect every 10th data point)

        indexes_needed = range(0, 100, 10)
        # Shape is (Samples, Channels)
        channels = np.zeros((len(indexes_needed), len(self.channels_for_live)))
        for ii, ch in enumerate(self.channels_for_live):
            # Get the channel index
            if type(ch) is str:
                channel_index = channel_dict[ch]
            else:
                channel_index = ch

            # Get our resolution for this channel
            resolution = resolutions[channel_index]

            channel_data = [data[index + channel_index] * resolution for index in indexes_needed]
            channels[:, ii] = np.asarray(channel_data)
        # Put our numpy array of channels on the queue.  Channels shape -> [samples (10), channel]
        self.process_queue.put(channels)

    @staticmethod
    def print_marker_count(markers, marker_count):
        # Print markers, if there are some in actual block
        if marker_count > 0:
            for m in range(marker_count):
                print "Marker " + markers[m].description + " of type " + markers[m].type

    @staticmethod
    def calc_avg_power(data1s, channel_count, sampling_interval, resolutions):
        if len(data1s) > channel_count * 1000000 / sampling_interval:
            index = int(len(data1s) - channel_count * 1000000 / sampling_interval)
            data1s = data1s[index:]

            avg = 0
            # Do not forget to respect the resolution !!!
            for i in range(len(data1s)):
                avg = avg + data1s[i] * data1s[i] * resolutions[i % channel_count] * resolutions[i % channel_count]

            avg /= len(data1s)
            print "Average power: " + str(avg)
            return []
        else:
            return data1s

    def first_message_actions(self, raw_data, verbose=True):
        """
        Executes all actions associated with the first message (such as collecting meta information)
        :param raw_data:
        :param verbose: If true, prints message to console.
        :return:
        """
        # Start message, extract eeg properties and display them
        (channel_count, sampling_interval, resolutions, channel_names) = DataCollect.get_properties(raw_data)
        # reset block counter
        self.last_block = -1

        sampling_interval_seconds = sampling_interval * 10.0 ** -6
        meta_info_str = "Subject Name:\t" + str(self.subject_name) + \
                        "Subject Tracking Number:\t" + str(self.subject_number) + \
                        "Experiment Number:\t" + str(self.experiment_number) + \
                        "Data Save Location:\t" + str(self.subject_data_path) + \
                        "Number of channels:\t" + str(channel_count) + '\n' + \
                        "Sampling interval:\t" + str(sampling_interval) + 'microseconds (' + str(sampling_interval_seconds) + ' seconds)\n' + \
                        'Sampling Frequency:\t' + str(1.0 / sampling_interval_seconds) + ' Hz\n' + \
                        "Resolutions:\t" + str(resolutions) + \
                        "Channel Names:\t" + str(channel_names)
        if verbose:
            print meta_info_str

        channel_dict = dict(zip(channel_names, range(channel_count)))
        return channel_count, sampling_interval, resolutions, channel_names, channel_dict, meta_info_str

    def get_raw_data(self):
        # Get message header as raw array of chars
        raw_hdr = DataCollect.recv_data(self.con, 24)

        # Split array into usefull information id1 to id4 are constants
        (id1, id2, id3, id4, msgsize, msgtype) = unpack('<llllLL', raw_hdr)

        # Get data part of message, which is of variable size
        raw_data = DataCollect.recv_data(self.con, msgsize - 24)
        return raw_data, msgsize, msgtype

if __name__ == '__main__':
    dc = DataCollect('Placeholder', ['C3', 'C4'], Queue.Queue())
    dc.start_recording()
