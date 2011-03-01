#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from subprocess import call, Popen, PIPE
import os
import sys

REMOTE = "/media/tarjeta"
LOCAL = os.path.abspath("sd")


def vcall(*args, **kwargs):
    print(", ".join(args))
    return call(*args, **kwargs)


def mount():
    proc = Popen("mount", stdout=PIPE, shell=True)
    mounteds = proc.stdout.readlines()

    if any((REMOTE in line for line in mounteds)):
        return True
    else:
        disksdir = "/dev/disk/by-id"
        disks = os.listdir(disksdir)
        sd_cards = [disk for disk in disks
            if ("usb-ChipsBnk_SD_MMCReader" in disk and
                "part1" in disk)]

        assert sd_cards
        error = vcall("sudo mount %s %s" % (os.path.join(disksdir, 
            sd_cards[0]), REMOTE), shell=True)
        return error == 0


def umount():
    error = vcall("sudo eject %s" % REMOTE, shell=True)
    return error == 0


def rsync(origen, destino):
    print("%s > %s" % (origen, destino))
    vcall('sudo rsync -a "%s/" "%s"' % (origen, destino), shell=True)


def main():
    assert mount()
    for dirname in os.listdir(LOCAL):
        localdirname = os.path.join(LOCAL, dirname)
        remotedirname = os.path.join(REMOTE, dirname)
        if "-r" in sys.argv:
            rsync(remotedirname, localdirname)
        else:
            rsync(localdirname, remotedirname)
    assert umount()


if __name__ == "__main__":
    exit(main())
