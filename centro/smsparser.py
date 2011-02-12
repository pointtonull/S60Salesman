#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ConfigParser import SafeConfigParser
from decoradores import Verbose
from optparse import OptionParser, OptionValueError
from subprocess import Popen, PIPE
import os
import poplib
import re
import smtplib
import sys
import time

APP_NAME = "smsparser"
CONF_NAME = "%s.conf" % APP_NAME
CONF_FILES = [os.path.expanduser("~/.%s" % CONF_NAME),
    os.path.expanduser("~/%s" % CONF_NAME)]
LOG_FILE = os.path.expanduser("~/.%s.log" % APP_NAME)


def get_options():
    # Instance the parser and define the usage message
    optparser = OptionParser(version="%prog .2")

    # Define the options and the actions of each one
    optparser.add_option("-c", "--config", help=("Uses the given conf file "
        "inteast of the default"), action="store", dest="conffile")
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


def get_config(conf_file=None):
    'Read config files'
    config = SafeConfigParser()
    read_from = conf_file or CONF_FILES
    files = config.read(read_from)
    debug("Readed config files at: %s" % files)

    return config


def get_messages(server, user, password, delete=True):
    """apop dele getwelcome host list noop pass_ port quit retr rpop
    rset set_debuglevel stat timestamp top uidl user welcome """

    POP3 = poplib.POP3(server)
    POP3.user(user)
    POP3.pass_(password)

    cantidad = len(POP3.list()[1])

    messages = []

    for numero in range(1, cantidad + 1):
        messages.append("\r\n".join(POP3.retr(numero)[1]))

    if delete:
        for numero in xrange(1, cantidad + 1):
            POP3.dele(numero)

    POP3.quit()
    debug(messages)
    return messages


class Logging(object):
    def __init__(self, filename):
        self.filename = filename
        self.touch()

    def touch(self):
        file = open(self.filename, "a")
        file.write("")
        file.close()

    def readlines(self):
        return open(self.filename).readlines()

    def write(self, message):
        with open(self.filename, "a") as file:
            file.write("%d: %s\r\n" % (time.time(), message))


def send_mail(server, user, password, fromaddr, toaddr, mailfile):
    msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s" % (
            fromaddr,
            toaddr,
            subject,
            message
           )

    server = smtplib.SMTP("SMTPSERVER")
    server.set_debuglevel(0)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()


def main(options, args):

    # Read the config values from the config files
    config = get_config(options.conffile)

    # Read the history log
    logfile = Logging(options.logfile)
    history = logfile.readlines()

    messages = get_messages(config.get("POP", "server"), config.get("POP",
        "user"), config.get("POP", "password"))

    for message in messages:
        regex = (r"""^Subject:\s*(\d+?)([a-zA-Z]+)""")
        match = re.search(regex, message,  re.MULTILINE|re.DOTALL)

        if match:
            pedido = match.group(1)
            parte = match.group(2)

            match = re.search(r"""[\r\n]{2}(.*)""", message, re.DOTALL)
            body = match.group(1)
            
            for line in body.splitlines():
                moreinfo(pedido, parte, line)


if __name__ == "__main__":
    # == Reading the options of the execution ==
    options, args = get_options()

    error = Verbose(options.verbose - options.quiet + 1, "E: ")
    info = Verbose(options.verbose - options.quiet + 0)
    warning = Verbose(options.verbose - options.quiet - 1, "W: ")
    debug = Verbose(options.verbose - options.quiet - 2, "D: ")

    debug("""Options: '%s', args: '%s'""" % (options, args))

    exit(main(options, args))
