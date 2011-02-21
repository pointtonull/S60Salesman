#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-

from decoradores import Verbose, Retry
from optparse import OptionParser, OptionValueError
import re
import os

APP_NAME = "mails2pedidos"
CONF_FILES = [os.path.expanduser("~/.%s" % APP_NAME),
    os.path.expanduser("~/%s.ini" % APP_NAME)]
LOG_FILE = os.path.expanduser("~/.%s.log" % APP_NAME)

VERBOSE = 1 # modified on __main__
MAIL_REGEX = r"""(\d+)([a-zA-Z]+)"""
FINAL_REGEX = r"""(\d+)([A-Z]+)"""


"""
    Este programa está pensado para ser llamado por  mailparser
    Args: inboxdir outboxdir

    Ennumera todos los ficheros en el inboxdir
    A partir de los ficheros fin de serie determina los necesarios para
        completar el pedido
    Si todos los ficheros necesarios están presentes completa el pedido y lo
        escribe en outboxdir
    Sino denuncia los faltantes en el log
"""

def get_options():
    # Instance the parser and define the usage message
    optparser = OptionParser(version="%prog .2")

    # Define the options and the actions of each one
    optparser.add_option("-l", "--log", help=("Uses the given log file "
        "inteast of the default"), action="store", dest="logfile")
    optparser.add_option("-v", "--verbose", action="count", dest="verbose",
        help="Increment verbosity")
    optparser.add_option("-q", "--quiet", action="count", dest="quiet",
        help="Decrement verbosity")

    # Define the default options
    optparser.set_defaults(verbose=0, quiet=0, logfile="%s.log" % APP_NAME)

    # Process the options
    return optparser.parse_args()


def reglob(path, regex):
    """
        List all the file in path that matches with regex
    """

    return [file for file in os.listdir(path) if re.match(regex, file)]


def main(options, args):
    print(reglob(args[0], FINAL_REGEX))


if __name__ == "__main__":
    # == Reading the options of the execution ==
    options, args = get_options()
    VERBOSE = options.verbose - options.quiet

    debug = Verbose(options.verbose - options.quiet - 2, "D: ")
    moreinfo = Verbose(options.verbose - options.quiet - 1)
    info = Verbose(options.verbose - options.quiet - 0)
    warning = Verbose(options.verbose - options.quiet + 1, "W: ")
    error = Verbose(options.verbose - options.quiet + 2, "E: ")

    debug("Verbose level: %s" %VERBOSE)
    debug("""Options: '%s', args: '%s'""" % (options, args))

    exit(main(options, args))
