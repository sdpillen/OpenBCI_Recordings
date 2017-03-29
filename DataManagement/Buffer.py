"""
This file is for EEG buffers
"""

import numpy as np


class NonOverlappingBuffer(object):
    """
    A NoOverlap Buffer is a buffer that reads in data
    """

    def __init__(self, capacity, num_channels, buffer_queue, out_queue):
        """
        A sample is defined as every read from the buffer_queue.
        A channel is a dimension allong the data read from the buffer queue.

        This nonoverlapping buffer stores capacity samples and, once capacity is reached, it places
        the results on the out_queue.
        :param capacity:  The number of samples to save to the buffer.
        :param num_channels:  Number of channels of data (ie. size of the list placed on the buffer_queue)
        :param buffer_queue:  Buffer queue is the origin of the data.
                                Data passed to this queue should be a list or 1D np array.
        :param out_queue:  Queue to place data on after the buffer reaches capacity.
        """
        self.capacity, self.num_channels = capacity, num_channels
        self.buffer = np.zeros((self.capacity, self.num_channels))
        self.sample_index = 0
        self.buffer_queue = buffer_queue
        self.out_queue = out_queue

    def start_buffer(self):
        """
         Starts the buffer, reading from buffer_queue and writing to out_queue
         once the buffer reaches capacity.  Once the buffer reaches capacity and is placed on the
         queue, the buffer is cleared.
        """
        while True:
            arr = self.buffer_queue.get()  # A blocking call
            if self.sample_index % self.capacity == 0:  # check if we reached capcity
                if self.sample_index != 0:  # Make sure we aren't putting on an empty buffer.
                    self.out_queue.put(self.buffer)

                raise NotImplementedError
                # Todo Fix this!!
                self.buffer = np.zeros((self.capacity, self.num_channels))
                self.buffer = arr  # Set our buffer to our new sample
            else:
                self.buffer = np.vstack((self.buffer, arr))
            self.sample_index += 1