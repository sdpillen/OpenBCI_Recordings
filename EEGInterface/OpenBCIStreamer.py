import OpenBCIHardwareInterface as BciHwInter
import time
import Utility.SystemInformation as SystemInfo
import EEG_INDEX


class OpenBCIStreamer(object):

    def __init__(self, data_dir_path, subject_num, data_value_queue, current_eeg_index_lock, port, live_data_queue=None):

        self.data_value_queue, self.current_eeg_index_lock = data_value_queue, current_eeg_index_lock

        self.data_file = file(data_dir_path + subject_num + '_OpenBCIData.csv', 'w')
        header = "Number of channels: " + str('N/A') + \
                 "\nSampling interval: " + str('N/A') +\
                 "\nResolutions: " + str('NA') + "\nChannel Names: " + str('Sample index, '
                                                                           'Sample index from Open BCI (Safe Sample Index), '
                                                                           'time'
                                                                           'data'
                                                                           'aux') + '\n\n' +\
                 'NA' + '\nDownsample:' + str('false') + '\nStartTime:' + str('%.4f' % time.time()) + '\n'
        self.data_file.write(header)
        self.data_file.flush()
        self.overall_data_index = 0

        # Set our port to default if a port isn't passed
        self.port = OpenBCIStreamer.get_default_port() if port is None else port

        self.live_data_queue = live_data_queue
        self.baud = 115200

    @staticmethod
    def get_default_port():
        """
        Returns the default port for the current operating system.
        :return:
        """
        if SystemInfo.is_linux():
            return '/dev/ttyUSB0'
        elif SystemInfo.is_windows():
            return 'COM0'
        else:
            raise ValueError('Default Port for OS not recognized')

    def write_file_callback(self, data_packet):
        try:
            data_time = time.time()
            data = data_packet.channel_data
            if self.overall_data_index % 250 == 0 and self.data_value_queue is not None:
                self.data_value_queue.put('Data = ' + str(data[0]))
            if self.overall_data_index % 250 == 0:
                print 'Data = ' + str(data[0])
            id_val = data_packet.id
            channel_data = data_packet.channel_data
            aux_data = data_packet.aux_data
        except Exception as e:
            # If we throw an error in this portion of the code, exit everything
            import os
            print e.message, e
            os._exit(1)
            raise  # Won't run
        data_str = str(self.overall_data_index) + ',' + str(id_val) + ',' + ','.join([str(xx) for xx in data]) + ',' + \
                   ','.join([str(yy) for yy in aux_data]) + '\n'
        if self.live_data_queue is not None:
            self.live_data_queue.put(data_str)
        self.data_file.write(data_str)
        self.data_file.flush()
        EEG_INDEX.CURR_EEG_INDEX = self.overall_data_index
        EEG_INDEX.CURR_EEG_INDEX_2 = self.overall_data_index
        self.overall_data_index += 1

    def start_open_bci_streamer(self):
        """
        Starts the open BciHwInter streamer. This method streams data infinitely and does not return.
        """
        board = BciHwInter.OpenBCIBoard(port=self.port, scaled_output=False, log=True)
        board.start_streaming(self.write_file_callback)
