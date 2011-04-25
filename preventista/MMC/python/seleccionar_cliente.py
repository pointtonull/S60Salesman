#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from lib. import DSV
import appuifw
import e32

def quit():
    app_lock.signal()
    appuifw.app.exit_key_handler = quit


def forming():
    appuifw.app.title = u'Formulario'

    models = [
        u'630',
        u'90',
        u'610',
        u'95',
        u'73',
        u'6630',
        u'E90',
        u'7610',
        u'N95',
        u'N73',
        ]

    data = [
        (u'Mobile','text', u'Nokia'),
        (u'Model','combo', (models, 1)),
        (u'Amount','number', 5),
        (u'Date', 'date'),
        (u'Time', 'time')
    ]

    flags = appuifw.FFormEditModeOnly
    form = appuifw.Form(data, flags)
    form.execute()

    names = [
        u"Michael",
        u"Michael",
        u"Devon",
        u"Bonnie",
        u"April",
        u"Michael",
        u"Devon",
        u"Bonnie",
        u"April",
        u"RC3",
        u"RC3",
        u"Devon",
        u"Bonnie",
        u"April",
        u"RC3",
        ]
    index = appuifw.selection_list(names, 1)
    if index == 2:
        print "I love you!"
    else:
        print "You're great!"



if __name__ == "__main__":
    forming()
    app_lock = e32.Ao_lock()
    app_lock.wait()
