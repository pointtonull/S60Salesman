#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from subprocess import call, Popen, PIPE
from decoradores import Retry
from time import sleep
import os
import sys

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


@Retry(10, pause=1)
def mount():
    proc = Popen("mount", stdout=PIPE, shell=True)
    mounteds = proc.stdout.readlines()

    if any((REMOTE in line for line in mounteds)):
        return True
    else:
        phones = get_phones()
        assert phones
        error = vcall("mount %s" % phones[0], shell=True)

        if error == 0:
            return True
        else:
            return


@Retry(5)
def get_phones():
    disksdir = "/dev/disk/by-id"
    disks = os.listdir(disksdir)
    phones = [os.path.join(disksdir, disk) for disk in disks
        if (("Nokia_S60" in disk or "SD_MMCReader" in disk)
            and "part1" in disk)]
    if phones:
        return phones


@Retry(5)
def umount():
    phone = get_phones()[0]
    error = vcall('umount "%s"' % phone, shell=True)
    if error == 0:
        return True
    else:
        return


def rsync(origen, destino):
    print("%s > %s" % (origen, destino))
    vcall('rsync -var --no-owner --no-g --modify-window=5 --delete'
        ' "%s/" "%s"' % (origen, destino), shell=True)


def main():
    assert mount()
    rsync("%s/data/movil" % REMOTE, "%s/data/movil" % LOCAL)
    rsync("%s/data/output" % REMOTE, "%s/data/output" % LOCAL)
    vcall('tail -n 30 "%s/debug.txt" > "%s/debug.txt"' % (REMOTE, LOCAL),
        shell=True)

    for dirname in ("data", ):
        localdirname = os.path.join(LOCAL, dirname)
        remotedirname = os.path.join(REMOTE, dirname)
        if "-r" in sys.argv:
            print("Ejecutando en modo inverso")
            rsync(remotedirname, localdirname)
        else:
            rsync(localdirname, remotedirname)

    assert umount()

    try:
        print(open("%s/debug.txt" % LOCAL).read())
    except:
        print("No debug file found.")


if __name__ == "__main__":
    exit(main())
