#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from subprocess import call, Popen, PIPE
import os
import sys
from time import sleep

REMOTE = "/media/tarjeta"
LOCAL = os.path.abspath("MMC")
VERBOSE = 0


def vcall(*args, **kwargs):
    """Verbose call. Print the command, execute, return exit code"""
    if VERBOSE:
        print(", ".join(args))
    try:
        error = call(*args, **kwargs)
    except OSError, e:
        print("Command failed: %s" % e)
        error = None
    return error


def mount():
    proc = Popen("mount", stdout=PIPE, shell=True)
    mounteds = proc.stdout.readlines()

    if any((REMOTE in line for line in mounteds)):
        return True
    else:
        error = vcall("mount %s" % REMOTE, shell=True)
        return error == 0

#        # FIXME: add media verification
#        disksdir = "/dev/disk/by-id"
#        disks = os.listdir(disksdir)
#        sd_cards = [disk for disk in disks
#            if (("Nokia_S60" in disk or "SD_MMCReader" in disk)
#                and "part1" in disk)]

#        assert sd_cards
#        error = vcall("mount %s %s" % (os.path.join(disksdir, 
#            sd_cards[0]), REMOTE), shell=True)
#        return error == 0


def umount():
    for attemp in range(3):
        error = vcall('umount "%s"' % REMOTE, shell=True)
        if error:
            print("Retrying")
            sleep(1)
        else:
            break
    return error == 0


def rsync(origen, destino):
    print("%s > %s" % (origen, destino))
    vcall('rsync -var --no-owner --no-g --modify-window=5 --delete'
        ' "%s/" "%s"' % (origen, destino), shell=True)


def main():
    assert mount()
    vcall('tail -n 50 "%s/debug.txt" > "%s/debug.txt"' % (REMOTE, LOCAL),
        shell=True)
    try:
        print(open("%s/debug.txt" % LOCAL).read())
    except:
        print("No debug file found.")

    for dirname in (LOCAL,):
        localdirname = os.path.join(LOCAL, dirname)
        remotedirname = REMOTE
        if "-r" in sys.argv:
            print("Ejecutando en modo inverso")
            rsync(remotedirname, localdirname)
        else:
            rsync(localdirname, remotedirname)

    assert umount()

if __name__ == "__main__":
    exit(main())
