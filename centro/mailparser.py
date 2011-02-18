#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-

from ConfigParser import SafeConfigParser
from collections import OrderedDict, defaultdict
from decoradores import Verbose, Retry
from email.parser import Parser
from email.message import Message
from email.mime.text import MIMEText
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
def get_messages(server, user, password, msg_class=None, delete=True):
    """apop dele getwelcome host list noop pass_ port quit retr rpop
    rset set_debuglevel stat timestamp top uidl user welcome """

    pop3 = poplib.POP3(server)
    pop3.user(user)
    pop3.pass_(password)

    quantity = len(pop3.list()[1])

    messages = []
    for number in range(1, quantity + 1):
        message = Parser(msg_class).parsestr("\n".join(pop3.retr(number)[1]))
        messages.append(message)

    if delete:
        for number in xrange(1, quantity + 1):
            pop3.dele(number)

    #TODO: save to log the readed messages just now!

    pop3.quit()
    return messages


def send_mail_from_file(server, user, password, fromaddr, toaddr, mailfile):
    """
        Sends a mail fetching Subject and Body from a text file with the
        form:
    """
    subject_body = open(mailfile).readlines()
    subject = subject_body[0]
    body = "\n".join(subject_body[3:])
    error = send_mail(server, user, password, fromaddr, toaddr, subject, body)
    return error
    

@Retry(5, pause=10)
def send_mail(server, user, password, fromaddr, toaddr, subject, body):

    msg = MIMEText(body)
    msg["From"] = fromaddr
    msg["To"] = toaddr
    msg["Subject"] = subject

    server = smtplib.SMTP(server)
    server.set_debuglevel(min(0, VERBOSE - 2))
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(user, password) 
    error = server.sendmail(fromaddr, toaddr, msg.as_string())
    server.quit()

    return error


def process_message(message, actions):
    info(u"Message: %s" % unicode(message["Subject"], "latin-1", "ignore"))

    for name, action in actions.iteritems():
        info(" Action: %s" % name)
        process_action(message, action)


def config_mail_parser(config):

    class Configured_message(Message):

        smtppassword = config.get("SMTP", "password")
        smtpserver = config.get("SMTP", "server")
        smtpuser = config.get("SMTP", "user")

        def __init__(self, *args, **kwargs):
            Message.__init__(self, *args, **kwargs)

        @Retry(5, 5)
        def reply(self, subject, body):
            send_mail(self.smtpserver, self.smtpuser, self.smtppassword,
                self["To"], self["From"], subject, body)

    return Configured_message


def process_action(message, action):
    safe_globals = {}
    safe_globals["__builtins__"] = globals()["__builtins__"]
    safe_globals["re"] = re

    safe_locals = {}
    safe_locals["message"] = message

    for name, expression in action:
        moreinfo("Executing %s = %s" % (name, expression))
        safe_locals[name] = eval(expression, safe_globals, safe_locals)
        debug("safe_locals: %s" % safe_locals)

        if name.startswith("assert"):
            if not safe_locals[name]:
                info("Ignored because assert is false.")
                return


def main(options, args):

    # Read the config values from the config files
    config = get_config(options.conffile)

#    # Read the history log
#    logging = Logging(options.logfile)

    if options.test:
        info("Entering to test mode")
        debug("Args: %s" % args)

        for filename in args:
            info("Sending %s" % filename)
            error = send_mail_from_file(config.get("SMTP", "server"),
                config.get("SMTP", "user"), config.get("SMTP", "password"),
                config.get("TESTMODE", "fromaddr"), config.get("TESTMODE",
                "toaddr"), filename)
            debug("Returned %s" % error)
            debug("Sleeping...")
            time.sleep(config.getint("TESTMODE", "delay"))

    else:
        sections = config.sections()
        actions = OrderedDict()
        for section in sections:
            if section.startswith("ACTION"):
                actions[section] = config.items(section, True)

        debug("Actions: %s" % actions.keys())

        message_parser = config_mail_parser(config)

        messages = get_messages(
            config.get("POP", "server"),
            config.get("POP", "user"),
            config.get("POP", "password"),
            msg_class=message_parser)

        for message in messages:
            process_message(message, actions)
                    


if __name__ == "__main__":
    # == Reading the options of the execution ==
    options, args = get_options()
    VERBOSE = options.verbose - options.quiet

    debug = Verbose(options.verbose - options.quiet - 2, "D: ")
    moreinfo = Verbose(options.verbose - options.quiet - 1)
    info = Verbose(options.verbose - options.quiet - 0)
    warning = Verbose(options.verbose - options.quiet + 1, "W: ")
    error = Verbose(options.verbose - options.quiet + 2, "E: ")

    info("Verbose level: %s" %VERBOSE)
    debug("""Options: '%s', args: '%s'""" % (options, args))

    exit(main(options, args))
