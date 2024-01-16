import time

class Timer(object):
    def __init__(self, name='Timing'):
        self.name = name

    def __enter__(self):
        self.tstart = time.time()

    def __exit__(self, type, value, traceback):
            print('[%s]' % self.name,'Elapsed: %s' % (time.time() - self.tstart))