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
VERBOSE = 1 # modified on __main__


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
    optparser.add_option("-t", "--test", action="store_true", dest="test",
        help="Process the files given as argument and sent in the order"
            "given to the testing address")

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
    """
        Sends a mail fetching Subject and Body from a text file with the
        form:

        "
        Subject: The subject


        Start of the body.
        Body Body Body.

        Spam Spam Spam
        Body Body.
        The end.
        "
    """

    subject_body = "\r\n".join(open(mailfile).readlines())

    msg = "From: %s\r\nTo: %s\r\n%s" % (
            fromaddr,
            toaddr,
            subject_body
           )

    server = smtplib.SMTP(server)
    server.set_debuglevel(VERBOSE)
    error = server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

    return error


def main(options, args):

    # Read the config values from the config files
    config = get_config(options.conffile)

    # Read the history log
    logfile = Logging(options.logfile)
    history = logfile.readlines()

    if options.test:
        for filename in args:
            info("Sending %s" % filename)
            error = send_mail(config.get("SMTP", "server"),
                config.get("SMTP", "user"), config.get("SMTP", "password"),
                config.get("TESTMODE", "fromaddr"), config.get("TESTMODE",
                "toaddr"), filename)
            debug("Returned %s" % error)
    else:
        messages = get_messages(config.get("POP", "server"),
            config.get("POP", "user"), config.get("POP", "password"))

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
    VERBOSE = options.verbose - options.quiet

    error = Verbose(options.verbose - options.quiet + 1, "E: ")
    info = Verbose(options.verbose - options.quiet + 0)
    warning = Verbose(options.verbose - options.quiet - 1, "W: ")
    debug = Verbose(options.verbose - options.quiet - 2, "D: ")

    debug("""Options: '%s', args: '%s'""" % (options, args))

    exit(main(options, args))
