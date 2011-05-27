#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from os import path, listdir, mkdir, rmdir, remove
from shutil import copy2
from debug import debug

__all__ = ["get_dirs_files", "rm_tree", "cp_tree"]


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


def get_dirs_files(dir_path):
    dirs = []
    files = []
    for name in listdir(dir_path):
        fullname = path.join(dir_path, name)
        if path.isfile(fullname):
            files.append(name)
        elif path.isdir(fullname):
            dirs.append(name)
        else:
            debug("Tipo desconocido: %s" % fullname)
    return dirs, files


def rm_tree(dir_path):
    "Remove the given path and all their contents"
    dirs, files = get_dirs_files(dir_path)
    assert path.isdir(dir_path)
    for filename in files:
        remove(filename)
    for dirname in dirs:
        rm_tree(dirname)
    rmdir(dir_path)


def cp_tree(orig, dest):
    "Copy the orig path and all their contents to dest path"
    debug("  cp_tree::%s, %s" % (orig, dest))
    if path.isdir(orig):
        if not path.exists(dest):
            mkdir(dest)
        for name in listdir(orig):
            orig_name = path.join(orig, name)
            dest_name = path.join(dest, name)
            cp_tree(orig_name, dest_name)
    else:
        try:
            copy2(orig, dest)
        except IOError:
            debug("  cp_tree::%s is protected")
