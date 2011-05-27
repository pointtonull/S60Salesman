#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from sys import stderr

def debug(message):
    for file in (open(r"e:\\debug.txt", "a"), stderr):
        file.write("%s\n" % message)
        file.flush()

__all__ = ["debug"]
