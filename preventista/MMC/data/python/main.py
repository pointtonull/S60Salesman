#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from os import path
import sys

SD_RESOURCE_PATH = r"%s:\data\python\preventista"

def get_sd_path():
    devices = "hgfedcba"
    for device in devices:
        if path.isdir(SD_RESOURCE_PATH % device):
            break
    else:
        device = None
    return device


def update_sys_path():
    main_resource_path = [dirname for dirname in sys.path
        if dirname.startswith("c:") and "resource" in dirname][0]
    sd_path = get_sd_path()
    assert sd_path
    sd_resource_path = SD_RESOURCE_PATH % sd_path
    if sd_resource_path not in sys.path:
        sys.path.insert(sys.path.index(main_resource_path), sd_resource_path)
        return True
    else:
        return False


def main():

    update_sys_path()
    from debug import debug, tracetofile
    debug("Path: %s" % sys.path)

#    from data import main as data_main
#    try:
#        data_main()
#    except:
#        tracetofile()

    try:
        from preventista import Preventista
        app = Preventista()
        app.run()
    except:
        tracetofile()


if __name__ == "__main__":
    main()
