import threading


class LockGuard(object):
    def __init__(self, obj, lock=None):
        self.lock = lock or threading.Lock()
        self._obj = obj

    def __enter__(self):
        self.lock.acquire()
        return self._obj

    def __exit__(self, exc_type, exc_value, traceback):
        self.lock.release()
