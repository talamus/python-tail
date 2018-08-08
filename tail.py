#!/usr/bin/env python

'''
Python-Tail - Unix tail follow implementation in Python.

python-tail can be used to monitor changes to a file.

Example:
    import tail

    # Create a tail instance:
    t = tail.Tail('file-to-be-followed', callback=print, sleep=1)
    # Optionally you can register a callback function and set the sleep time.

    # Start tailing:
    t.start()

    # Wait for a key press, and stop trailing:
    input()
    t.stop() '''

# Authors - Kasun Herath <kasunh01 at gmail.com>, Tero Niemi <talamus at gmail.com>
# Source - https://github.com/talamus/python-tail

import os
import sys
import time
from threading import Thread

class Tail(Thread):
    ''' Represents a tail command. '''
    def __init__(self, tailed_file, callback=print, sleep=1):
        ''' Initiate a Tail instance.
            Check for file validity, assigns callback function to standard out.

            Arguments:
                tailed_file - File to be followed.
                callback - alternative callback function. (Default: print)
                sleep - time between re-checks. (Default: 1) '''

        self.check_file_validity(tailed_file)
        self.tailed_file = tailed_file
        self.callback = callback
        self.sleep = sleep
        self.is_active = True
        Thread.__init__(self)

    def run(self):
        ''' Do a tail follow. For every new line a callback is called. '''
        with open(self.tailed_file) as file_:
            # Go to the end of file
            file_.seek(0,2)
            while self.is_active:
                curr_position = file_.tell()
                line = file_.readline()
                if not line:
                    file_.seek(curr_position)
                    time.sleep(self.sleep)
                else:
                    self.callback(line.rstrip())

    def stop(self):
        ''' Stop the tailing. '''
        self.is_active = False

    def check_file_validity(self, file_):
        ''' Check whether the a given file exists, is readable and is a file. '''
        if not os.access(file_, os.F_OK):
            raise TailError("File '%s' does not exist" % (file_))
        if not os.access(file_, os.R_OK):
            raise TailError("File '%s' not readable" % (file_))
        if os.path.isdir(file_):
            raise TailError("File '%s' is a directory" % (file_))

class TailError(Exception):
    def __init__(self, msg):
        self.message = msg
    def __str__(self):
        return self.message
