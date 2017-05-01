# needs socket and struct library
import socket
import struct
import time
import Queue
import threading
import CCDLUtil.EEGInterface.EEGDataSaver
import numpy as np
import CCDLUtil.EEGInterface.EEG_INDEX
import CCDLUtil.EEGInterface.EEGInterfaceParent as CCDLEEGParent
import pylsl


class GUSBAmpStreamer(CCDLEEGParent.EEGInterfaceParent):



    def __init__(self, channels_for_live, out_queue, put_data_on_out_queue_flag=False, data_save_queue=None, subject_name=None, subject_tracking_number=None, experiment_number=None):
        """
        A data collection object for the EEG interface.  This provides option for live data streaming and saving data to file.

        For live data streaming, use with a threading or multiprocessing queue (ie. Queue.queue()
           Data will be put on the queue, which can be read by another thread.)

        Modifies the EEG_INDEX and EEG_INDEX_2 in CCDLUtil/EEGInterface/EEG_INDEX.py when each packet arrives.  These variables can be read from any thread.
            Use this to time mark events in your other programs.

        :param channels_for_live: List of channel names (or indexes) to put on the out_buffer_queue. If [] or None, no channels will be put on the out_buffer_queue.
                                  If 'All', all channels will be placed on the out_buffer_queue.
        :param data_save_queue: queue to put data to save.  If None, data will not be saved.
        :param out_queue: The channel listed in the channels_for_live parameter will be placed on this queue. This is intended for live data analysis.
                                 If None, no data will be put on the queue.
                                 Items put on the out buffer queue will be a numpy array (though this can be either a 2D or a 1D numpy array)
        :param subject_name: Optional -- Name of the subject. Defaults to 'None'
        :param subject_tracking_number: Optional -- Subject Tracking Number (AKA TMS group experiment number tracker). Defaults to 'None'
        :param experiment_number: Optional -- Experimental number. Defaults to 'None'
        """



        # Call our EEGInterfaceParent init method.  Channels_for_live is converted to lower case in super call if it is a string.
        super(GUSBAmpStreamer, self).__init__(channels_for_live, out_queue, data_save_queue=data_save_queue, put_data_on_out_queue_flag=put_data_on_out_queue_flag,
                                              subject_name=subject_name, subject_tracking_number=subject_tracking_number, experiment_number=experiment_number)

        # first resolve an EEG stream on the lab network
        print "looking for an EEG stream..."
        self.streams = pylsl.resolve_stream('type', 'EEG')

        # create a new inlet to read from the stream
        print "Creating inlet..."
        self.inlet = pylsl.StreamInlet(self.streams[0])

        self.current_index = 0

    def start_recording(self):
        """
        Start our recording
        """
        parity = 0
        print "Starting recording..."
        # ##### Main Loop #### #
        while True:
            sample, timestamp = self.inlet.pull_sample()
            parity += 1

            # Get the time we collected the sample
            self.data_index += 1  # Increase our sample counter

            CCDLUtil.EEGInterface.EEG_INDEX.EEG_INDEX = self.data_index
            CCDLUtil.EEGInterface.EEG_INDEX.EEG_INDEX_2 = self.data_index
            self.current_index = self.data_index

            # print self.data_index, CCDLUtil.EEGInterface.EEG_INDEX.EEG_INDEX
            ###################
            # Handle the Data #
            ###################
            # Save the Data - We put data on the queue to be saved - format for queue (index, time, data)
            if self.data_save_queue is not None:
                self.data_save_queue.put((self.data_index, timestamp, sample))

            # Put dota on the out queue
            if self.put_data_on_out_queue_flag and self.out_queue is not None and self.channels_for_live is not None and self.channels_for_live != []:
                # Only put on the channels we need.  self.channels_for_live is guaranteed lower case... we'll program defensively
                if self.channels_for_live == 'all' or self.channels_for_live == 'All' or self.channels_for_live == 'ALL':
                    trimmed_data_for_out_queue = sample
                else:
                    trimmed_data_for_out_queue = [sample[index] for index in self.channels_for_live]
                self.out_queue.put(trimmed_data_for_out_queue)


if __name__ == '__main__':
    dc = GUSBAmpStreamer(channels_for_live='All', out_queue=Queue.Queue, data_save_queue=None)
    dc.start_recording()
