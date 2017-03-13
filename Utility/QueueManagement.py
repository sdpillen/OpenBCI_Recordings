
def clear_queue(q):
    """Clears a queue in a thread-safe manner"""
    with q.mutex:
        q.queue.clear()
