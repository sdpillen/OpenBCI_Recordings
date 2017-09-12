"""
To save data, it is suggested that this module is used with the EEGDataSaver.
threading.Thread(target=lambda: EEGDataSaver.start_eeg_data_saving(subject_data_path, self.data_save_queue, header=None)).start()

"""

import Queue


class EEGInterfaceParent(object):

    """
    A Parent interface that should be inherited other systems that interface with EEG.
    """

    def __init__(self, channels_for_live='All', live=True, save_data=True, subject_name=None,
                 subject_tracking_number=None, experiment_number=None):
        """
        A data collection object for the EEG interface.
        This provides option for live data streaming and saving data to file.

        Modifies the EEG_INDEX and EEG_INDEX_2 in CCDLUtil/EEGInterface/EEG_INDEX.py when each packet arrives.
        These variables can be read from any thread. Use this to time mark events in your other programs.

        :param channels_for_live: List of channel names (or indexes) to put on the out_buffer_queue. If [], no channels
                    will be put on the out_buffer_queue. If 'All' (case is ignored), all channels will be placed on the
                    out_buffer_queue.  Defaults to All.
        :param live: True to create out_buffer_queue. Default to True
        :param save_data: True to create data_save_queue. Default to True
        :param subject_name: Optional -- Name of the subject. Defaults to 'None'
        :param subject_tracking_number: Optional -- Subject Tracking Number (AKA TMS group experiment number tracker). Defaults to 'None'
        :param experiment_number: Optional -- Experimental number. Defaults to 'None'
        """

        self.subject_name = str(subject_name) if subject_name is not None else "None"
        self.subject_number = str(subject_tracking_number) if subject_tracking_number is not None else 'None'
        self.experiment_number = str(experiment_number) if experiment_number is not None else 'None'
        # Count each block we receive, start at -1 to avoid a fence/post problem.
        self.data_index = -1
        # data saving and live analysis flags
        self.live = live
        self.save_data = save_data
        # A separate queue (other than the one for storing data) that puts the channels_for_live data points on
        self.out_buffer_queue = Queue.Queue() if live else None
        # block counter to check overflows of tcpip buffer
        self.last_block = -1
        self.channels_for_live = channels_for_live
        if type(self.channels_for_live) is str:
            self.channels_for_live = self.channels_for_live.lower()
            if self.channels_for_live != 'all':
                raise ValueError('Invalid channels_for_live parameter')
        # create data save queue
        self.data_save_queue = Queue.Queue() if save_data else None

    @staticmethod
    def trim_channels_with_channel_index_list(data, channel_index_list):
        """
        Saves data[i] where i is an element in channel_index_list.
        For example:
            data = [500, 400, 350, 450]
            channel_index_list = [0, 2]
            trim_channels_with_channel_index_list(data, channel_index_list) -> [500, 350]

        :param data: A string of data points
        :param channel_index_list: A list of channel indexes that we want to save.
        :return: trimmed data list
        """
        return [data[xx] for xx in channel_index_list]

    def start_recording(self):
        """
        To be overridden by child
        """
        pass
