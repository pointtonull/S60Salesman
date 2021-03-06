#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from time import time
import sys
import traceback
from appuifw import note

DEBUG_FILE = ur"e:\data\movil\debug.txt"
IMPORT_TIME = time()
DEBUG = 1
# 0: no messages
# 1: messages to file
# 2: messages to file and stderr


if DEBUG > 0:
    file = open(DEBUG_FILE, "a")
    file.write("\n\nRe-estarting debug: %d\n" % IMPORT_TIME)
    file.close()

def debug(message):
    files = []
    if DEBUG > 1:
        files.append(sys.stderr)
    if DEBUG > 0:
        try:
            files.append(open(DEBUG_FILE, "a"))
        except IOError:
            files.append(open(DEBUG_FILE, "w"))

    if files:
        if isinstance(message, basestring):
            try:
                message = message.encode("latin1", "replace")
            except UnicodeDecodeError:
                message = message.encode("utf8", "replace")
        new_time = time() - IMPORT_TIME
        message = "%4d - %s\n" % (new_time, message)
        for file in files:
            file.write(message)
            file.close()

    return DEBUG

def tracetofile():
    file = open(DEBUG_FILE, "a")
    file.write("Captured traceback\n")
    traceback.print_exc(file=file)
    file.close()
    note(u"Error inesperado", "error")
    raise

__all__ = ["debug"]
