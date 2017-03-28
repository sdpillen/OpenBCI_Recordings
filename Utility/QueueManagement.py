"""
For the use of multithreading and multiprocessing queues.

See https://docs.python.org/3/library/queue.html for Queue api.

"""

import Queue

def clear_queue(q):
    """Clears a queue in a thread-safe manner"""
    with q.mutex:
        q.queue.clear()

def get_queue_dict(all_queues):
    """
    Gets a queue dictionary with keys equal to all queues names in ALL_QUEUES
    :param all_queues: A list of queue names (strings).  These will be the keys of the returned dict.
    :return: Returns a queue dictionary of the the form:
     queue_dict['queue name'] -> Python Queue
    """
    queue_dict = dict()
    for q in all_queues:
        queue_dict[q] = Queue.Queue()
    return queue_dict