
# needs socket and struct library
import socket
import struct
import time
import Queue
import threading
import EEGInterface.EEGDataSaver
import numpy as np
import EEGInterface.EEG_INDEX
import EEGInterface.EEGInterfaceParent
import pylsl


class BrainAmpStreamer(EEGInterface.EEGInterfaceParent.EEGInterfaceParent):

    """
    A Parent interface that should be inherited other systems that interface with EEG.
    """

    def __init__(self, channels_for_live, out_buffer_queue, data_save_queue=None, subject_name=None, subject_tracking_number=None, experiment_number=None):
        """
        A data collection object for the EEG interface.  This provides option for live data streaming and saving data to file.

        For live data streaming, use with a threading or multiprocessing queue (ie. Queue.queue()
           Data will be put on the queue, which can be read by another thread.)

        Modifies the EEG_INDEX and EEG_INDEX_2 in CCDLUtil/EEGInterface/EEG_INDEX.py when each packet arrives.  These variables can be read from any thread.
            Use this to time mark events in your other programs.

        :param channels_for_live: List of channel names (or indexes) to put on the out_buffer_queue. If [], no channels will be put on the out_buffer_queue.
                                  If 'All', all channels will be placed on the out_buffer_queue.
        :param data_save_queue: queue to put data to save.  If None, data will not be saved.
        :param out_buffer_queue: The channel listed in the channels_for_live parameter will be placed on this queue. This is intended for live data analysis.
                                 If None, no data will be put on the queue.
                                 Items put on the out buffer queue will be a numpy array (though this can be either a 2D or a 1D numpy array)
        :param subject_name: Optional -- Name of the subject. Defaults to 'None'
        :param subject_tracking_number: Optional -- Subject Tracking Number (AKA TMS group experiment number tracker). Defaults to 'None'
        :param experiment_number: Optional -- Experimental number. Defaults to 'None'
        """
        # Call our EEGInterfaceParent init method.
        super(BrainAmpStreamer, self).__init__(channels_for_live, out_buffer_queue, data_save_queue=data_save_queue, subject_name=subject_name,
                                               subject_tracking_number=subject_tracking_number, experiment_number=experiment_number)

        # first resolve an EEG stream on the lab network
        # print("looking for an EEG stream...")
        self.streams = pylsl.resolve_stream('type', 'EEG')

        # create a new inlet to read from the stream
        self.inlet = pylsl.StreamInlet(self.streams[0])

    def start_recording(self):
        """
        Start our recording
        """

        # ##### Main Loop #### #
        while True:
            sample, timestamp = self.inlet.pull_sample()
            # Get the time we collected the sample
            data_recieve_time = time.time()

            self.data_index += 1  # Increase our sample counter

            EEGInterface.EEG_INDEX.EEG_INDEX = self.data_index
            EEGInterface.EEG_INDEX.EEG_INDEX_2 = self.data_index


            ###################
            # Handle the Data #
            ###################
            # Save the Data - We put data on the queue to be saved - format for queue (index, time, data)
            if self.data_save_queue is not None:
                self.data_save_queue.put((self.data_index, data_recieve_time, data))

            # if we are
            if self.put_data_on_out_queue_flag is not None:
                self.handle_out_buffer_queue(data, resolutions, channel_count, channel_dict)



if __name__ == '__main__':
    dc = BrainAmpStreamer('Placeholder', ['C3', 'C4'], Queue.Queue())
    dc.start_recording()
