#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from subprocess import call, Popen, PIPE
import os
import sys

REMOTE = "/media/tarjeta"
LOCAL = os.path.abspath("sd")


def mount():
    proc = Popen("mount", stdout=PIPE, shell=True)
    mounteds = proc.stdout.readlines()

    if any((REMOTE in line for line in mounteds)):
        return True
    else:
        disks = os.listdir("/dev/disk/by-id")
        sd_cards = [disk for disk in disks
            if ("usb-ChipsBnk_SD_MMCReader" in disk and
                "part1" in disk)]

        assert sd_cards
        call("sudo mount %s %s" % (sd_cards[0], REMOTE), shell=True)


def umount():
    call("sudo eject %s" % REMOTE, shell=True)


def rsync(origen, destino):
    print("%s > %s" % (origen, destino))
    call('sudo rsync -av "%s/" "%s"' % (origen, destino), shell=True)


def main():
    mount()
    for dirname in os.listdir(LOCAL):
        localdirname = os.path.join(LOCAL, dirname)
        remotedirname = os.path.join(REMOTE, dirname)
        if "-r" in sys.argv:
            rsync(remotedirname, localdirname)
        else:
            rsync(localdirname, remotedirname)
    umount()


if __name__ == "__main__":
    exit(main())
