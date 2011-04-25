#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import appuifw
import e32
from auto_dsv import import_dsv

def quit():
    app_lock.signal()
    appuifw.app.exit_key_handler = quit


def forming():
    appuifw.app.title = u'Selección de cliente'
    clientes = import_dsv(r"c:\\python\data\input\clientes.csv")
    zonas_clientes = [cliente["CARACT_ZON"] for cliente in clientes]
    nombres_clientes = [cliente["APNBR_CLI"] for cliente in clientes]

    data = [
        (u'Zona','combo', (zonas_clientes, 0)),
        (u'Cliente','combo', (nombres_clientes, 0)),
    ]

#        (u'Cliente','number', 5),
#        (u'Mobile','text', u'Nokia'),
#        (u'Date', 'date'),
#        (u"Date", 'date', time.time()),
#        (u'Time', 'time')

    flags = appuifw.FFormEditModeOnly | appuifw.FFormDoubleSpaced
    form = appuifw.Form(data, flags)
    appuifw.app.menu = [
        (u"Zonas", 
            (u"Zona 1", (
                (u"Cliente 1", forming),
                (u"Cliente 2", forming),
                (u"Cliente 3", forming),
            )),
            (u"Zona 2", (
                (u"Cliente 4", forming),
                (u"Cliente 5", forming),
                (u"Cliente 6", forming),
            )),
        ),
        (u"Clientes", (
            (u"Cliente 1", forming),
            (u"Cliente 2", forming),
            (u"Cliente 3", forming),
            (u"Cliente 4", forming),
            (u"Cliente 5", forming),
            (u"Cliente 6", forming),
        ))
        ]

    form.execute()

if __name__ == "__main__":
    forming()

#    app_lock = e32.Ao_lock()
#    app_lock.wait()
