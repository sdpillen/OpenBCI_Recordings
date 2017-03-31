"""
A class for generating log files.

This takes data from a queue and writes it to disk.  This is typically event data from
an experiment (not EEG data).

"""
import StringParser


class Log(object):

    """
    A log object is responsible for reading items from a queue and writing them to file.
    """

    def __init__(self, subject_log_file_path, log_queue, header=None):
        """
        Logs all items to file.  Files are taken from the log_queue and written to the file specified by
        subject_log_file_path.
        :param subject_log_file_path: String. where to save the file
        :param log_queue: queue to read items from
        :param header:
        """
        self.f = file(subject_log_file_path, 'w')
        self.log_queue = log_queue
        if header is not None:
            self.f.write(header)

    def start_log(self, verbose=False):
        """
        Starts reading items from the queue.  All items passed to the queue must be a string or it will be converted
        (raising a warning).  If no new line is at the end of the string, one will be added.

        The buffer is immediately flushed after every write.

        :param verbose: If verbose, will print the items to console.  Defaults to False.
        :return: Runs forever.  Kill thread to terminate.
        """

        while True:
            body = self.log_queue.get()
            assert type(body) is str
            body = StringParser.idempotent_append_newline(body)
            if verbose:
                print body
            self.f.write(body)
            self.f.flush()
