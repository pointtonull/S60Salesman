#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-

from ConfigParser import SafeConfigParser
from collections import OrderedDict, defaultdict
from decoradores import Verbose, Retry
from email.parser import Parser
from optparse import OptionParser, OptionValueError
from subprocess import Popen, PIPE
import os
import poplib
import re
import smtplib
import sys
import time

APP_NAME = "mailparser"
CONF_FILES = [os.path.expanduser("~/.%s" % APP_NAME),
    os.path.expanduser("~/%s.ini" % APP_NAME)]
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
    config = SafeConfigParser(None, OrderedDict)
    read_from = conf_file or CONF_FILES
    files = config.read(read_from)
    debug("Readed config files at: %s" % files)

    return config

@Retry(5, pause=10)
def get_messages(server, user, password, delete=True):
    """apop dele getwelcome host list noop pass_ port quit retr rpop
    rset set_debuglevel stat timestamp top uidl user welcome """

    pop3 = poplib.POP3(server)
    pop3.user(user)
    pop3.pass_(password)

    quantity = len(pop3.list()[1])

    messages = []
    for number in range(1, quantity + 1):
        message = Parser().parsestr("\n".join(pop3.retr(number)[1]))
        messages.append(message)

    if delete:
        for number in xrange(1, quantity + 1):
            pop3.dele(number)

    #TODO: save the readed messages just now!

    pop3.quit()
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
            file.write("%d: %s\n" % (time.time(), message))


@Retry(5, pause=10)
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

    subject_body = open(mailfile).read()

    msg = "From: %s\nTo: %s\n%s" % (
            fromaddr,
            toaddr,
            subject_body
           )

    server = smtplib.SMTP(server)
    server.set_debuglevel(VERBOSE - 1)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(user, password) 
    error = server.sendmail(fromaddr, toaddr, msg)
    server.quit()

    return error

def get_headers(message):
    return headers

def main(options, args):

    # Read the config values from the config files
    config = get_config(options.conffile)

#    # Read the history log
#    logfile = Logging(options.logfile)
#    history = logfile.readlines()

    if options.test:
        info("Entering to test mode")
        debug("Args: %s" % args)

        for filename in args:
            info("Sending %s" % filename)
            error = send_mail(config.get("SMTP", "server"),
                config.get("SMTP", "user"), config.get("SMTP", "password"),
                config.get("TESTMODE", "fromaddr"), config.get("TESTMODE",
                "toaddr"), filename)
            debug("Returned %s" % error)
            debug("Sleeping...")
            time.sleep(config.getint("TESTMODE", "delay"))

    else:
        sections = config.sections()
        actions = [section
            for section in sections
                if section.startswith("ACTION")]
        debug("Actions: %s" % actions)

        messages = get_messages(
            config.get("POP", "server"),
            config.get("POP", "user"),
            config.get("POP", "password"))

        for message in messages:
            debug(u"Message: %s" % unicode(str(message), "latin-1", "ignore"))

            for action in actions:
                debug(u"  Action: %s" % action)

                safe_globals = {}
                safe_globals["__builtins__"] = globals()["__builtins__"]
                safe_locals = {}
                for key, value in config.items(action, True):
                    moreinfo("Executing %s = %s" % (key, value))
                    safe_locals[key] = eval(value, safe_globals, safe_locals)
                    debug("safe_locals: %s" % safe_locals)
                    



if __name__ == "__main__":
    # == Reading the options of the execution ==
    options, args = get_options()
    VERBOSE = options.verbose - options.quiet

    error = Verbose(options.verbose - options.quiet + 2, "E: ")
    moreinfo = Verbose(options.verbose - options.quiet + 1)
    info = Verbose(options.verbose - options.quiet + 0)
    warning = Verbose(options.verbose - options.quiet - 1, "W: ")
    debug = Verbose(options.verbose - options.quiet - 2, "D: ")

    debug("""Options: '%s', args: '%s'""" % (options, args))

    exit(main(options, args))
