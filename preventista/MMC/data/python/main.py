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
    sys.path.insert(sys.path.index(main_resource_path), sd_resource_path)
    return True


def main():
    def naturales(desde, hasta):
        for n in xrange(desde, hasta):
            yield n

    for n in naturales(5, 50):
        print n

    update_sys_path()
    from debug import debug, tracetofile
    debug("Path: %s" % sys.path)

    from appuifw import note
    try:
        from preventista import Preventista
        app = Preventista()
        app.run()
    except:
        tracetofile()


if __name__ == "__main__":
    main()
