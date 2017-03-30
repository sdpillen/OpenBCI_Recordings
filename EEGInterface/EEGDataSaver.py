"""
This file is for saving EEG Data
"""

import DataManagement.StringParser as StringParser

def start_eeg_data_saving(save_data_file_path, queue, header=None):
    """

    This function is called from the BrainAmpInterface.

    A function to be called in a new thread whose sole purpose is to save eeg data to disk.
    :param save_data_file_path: A string - The full file name to save the data (for example './data/subjectX.csv').
    :param queue: The queue to read the data from.
            Data should be placed on the queue in the form:
                index, time, data

                - Index
                    Where index is the packet (or sample) index.  This can be a string or a number.
                - Time
                    Time is the time in which the transferred data was collected.  This is typically from time.time().
                        This can be a string or a number.
                - Data
                    A list of data points in the form [chan 1, chan 2...], where chan X is a number.

                If time or index is None, we'll write data to file as is (with a new line appended)

            Data save format.
                Data will be saved in the comma separated format:
                    index,time,chan1,chan2,chan3...\n

    :param header: Header for the file.  If no header is wanted, pass None.  Defaults to None.

    :return: Runs infinitely.  Kill by terminating the thread.
    """
    f = file(save_data_file_path, 'w')

    # Write our header with only one newline character
    if header is not None:
        if header.endswith('\n'):
            f.write(header)
        else:
            f.write(header)
            f.write('\n')
        f.flush()
    while True:
        # get our components
        index, t, data = queue.get()
        if index is None or t is None:
            # Append a newline if needed.
            f.write(StringParser.idempotent_append_newline(str(data)))
        else:
            # Write our index and timestamp
            f.write(str(index) + ',' + str(t))
            # convert our data to strings
            data = map(str, data)
            # convert our data to a comma separated string
            f.write(','.join(data))
            # Write a new line character
            f.write('\n')
            # Flush our buffer
            f.flush()
