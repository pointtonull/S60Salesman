#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from os import listdir, path
import sys

def get_sd_path():
    devices = "kjihgfedcba"
    for device in devices:
        try:
            dirs = listdir("%s:" % device)
        except:
            dirs = []
        dirs = [dir_path.lower() for dir_path in dirs]

        if "resource" in dirs:
            break
    else:
        device = None
    return device


def update_sys_path():
    main_resource_path = [dir for dir in sys.path if dir.startswith("c:")][0]
    sd_path = get_sd_path()
    assert sd_path
    sd_resource_path = "%s:\\resource" % sd_path
    sys.path.insert(sys.path.index(main_resource_path), sd_resource_path)
    return True


def main():
    update_sys_path()
    from debug import debug
    debug(sys.path)
    return 0


if __name__ == "__main__":
    main()
