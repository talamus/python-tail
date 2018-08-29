#!/usr/bin/env python

'''
Python-Tail - Unix tail follow implementation in Python.

python-tail can be used to monitor changes to a file.

Example:
    import tail

    # Create a tail instance:
    t = tail.Tail('logs/*.txt', callback=print, sleep=1)
    # Optionally you can register a callback function and set the sleep time.

    # Start tailing:
    t.start()

    # Wait for a key press, and stop tailing:
    input()
    t.stop() '''

# Authors - Kasun Herath <kasunh01 at gmail.com>, Tero Niemi <talamus at gmail.com>
# Source - https://github.com/talamus/python-tail

import os
import sys
import time
import signal
import glob
from threading import Thread

def default_callback(message, filename):
    print(filename, ':', message, flush=True)

class Tail(Thread):
    ''' Represents a tail command. '''
    def __init__(self, glob_to_be_tailed, callback=default_callback, sleep=2):
        ''' Initiate a Tail instance.
            Check for file validity, assigns callback function to standard out.

            Arguments:
                glob_to_be_tailed - Glob pattern to be followed.
                callback - alternative callback function. (Default: print)
                sleep - time between re-checks. (Default: 2) '''

        self.glob_to_be_tailed = glob_to_be_tailed
        self.callback = callback
        self.sleep = sleep
        self.is_active = True
        self.positions = {}
        Thread.__init__(self)

    def run(self):
        ''' Do the tailing. For every new line a callback is called. '''

        # Seek existing files and go to the end of the file
        filenames = glob.glob(self.glob_to_be_tailed)
        for filename in filenames:
            print(filename, os.path.getsize(filename))
            self.positions[filename] = os.path.getsize(filename)

        # get a list of matching filenames, and for each try to seek new lines
        while self.is_active:
            positions = {}
            filenames = glob.glob(self.glob_to_be_tailed)
            for filename in filenames:
                try:
                    with open(filename) as file:
                        if filename in self.positions:
                            position = self.positions[filename]
                        else:
                            position = 0
                        file.seek(position)
                        for line in file:
                            self.callback(line.rstrip(), filename)
                        position = file.tell()
                        file.close()
                    positions[filename] = position
                except PermissionError:
                    pass
            self.positions = positions
            time.sleep(self.sleep)

    def stop(self):
        ''' Stop the tailing. '''
        self.is_active = False


if __name__ == '__main__':

    tails = []
    sys.argv.pop(0)
    for glob_pattern in sys.argv:
        tail = Tail(glob_pattern)
        tails.append(tail)
        print('Tailing "'+ glob_pattern +'"')
        tail.start()

    if not tails:
        print('Usage: python tail.py [glob to be tailed] [...]')
        exit(1)

    def signal_handler(signal, frame):
        for tail in tails:
            tail.stop()
        print('Tailing stopped')
        exit()
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    while True:
        time.sleep(127)
