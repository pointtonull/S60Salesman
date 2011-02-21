#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import appuifw, e32

def quit():
    app_lock.signal()
    appuifw.app.exit_key_handler=quit


def forming():
    model = [u'6630', u'E90', u'7610', u'N95', u'N73']
    data=[
        (u'Mobile','text', u'Nokia'),
        (u'Model','combo', (model, 0)),
        (u'Amount','number', 5),
        (u'Date', 'date'),
        (u'Time', 'time')
    ]
    flags = appuifw.FFormEditModeOnly
    form = appuifw.Form(data, flags)
    form.execute()


if __name__ == "__main__":
    forming()
    app_lock = e32.Ao_lock()
    app_lock.wait()
