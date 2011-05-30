#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from time import time
from sys import stderr

DEBUG_FILE = r"e:\debug.txt"
IMPORT_TIME = time()
DEBUG = 1
# 0: no messages
# 1: messages to file
# 2: messages to file and stdout

if DEBUG > 0:
    file = open(DEBUG_FILE, "w")
    file.write("Re-estarting debug: %d\n" % IMPORT_TIME)
    file.close()

def debug(message):
    files = []
    if DEBUG > 1:
        files.append(stderr)
    if DEBUG > 0:
        files.append(open(DEBUG_FILE, "a"))
    
    if files:
        new_time = time() - IMPORT_TIME
        message = "%4d - %s\n" % (new_time, message)
        for file in files:
            file.write(message)
            file.flush()

    return DEBUG


__all__ = ["debug"]
