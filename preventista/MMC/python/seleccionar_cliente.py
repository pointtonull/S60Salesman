#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import appuifw
import e32
from auto_dsv import import_dsv
from uniq import uniq, sorted
from random import randrange


class Seleccionar_cliente(object):
    def __init__(self):
        self.clientes = import_dsv(r"c:\\python\data\input\clientes.csv")
        self.data = self.get_data()
        self.app_lock = e32.Ao_lock()
        self.configure_form()


    def get_data(self):
        zonas_clientes = sorted(uniq([cliente["CARACT_ZON"]
            for cliente in self.clientes]))
        control_zona = (u'Zona','combo', (zonas_clientes, 0))

        zona = zonas_clientes[0]
        nombres_clientes = sorted(uniq([cliente["APNBR_CLI"]
            for cliente in self.clientes
                if cliente["CARACT_ZON"] == zona]))
        control_cliente = (u'Cliente','combo', (nombres_clientes, 0))

        control_prueba_int = (u'Prueba','number', randrange(10))
        data = [
            control_zona,
            control_cliente,
            control_prueba_int,
        ]

#        (u'Mobile','text', u'Nokia')
#        (u'Date', 'date')
#        (u"Date", 'date', time.time())
#        (u'Time', 'time')
        
        return data


    def save_hook(self, data):
        print("save_hook::%s" % data)
        if data != self.data:
            control_zona = data[0]
            zona = control_zona[2][control_zona[3]]
            nombres_clientes = sorted(uniq([cliente["APNBR_CLI"]
                for cliente in self.cliente
                    if cliente["CARACT_ZON"] == zona]))
            control_cliente = (u'Cliente','combo', (nombres_clientes, 0))
            control_prueba_int = data[2][0], data[2][1], data[2][2] + 1
            data[1] = control_cliente
            data[2] = control_prueba_int
            self.data = data
        return False


    def loop(self):
#        appuifw.app.body = self.form
        self.app_lock.wait()


    def quit(self):
        print("Nabo")


    def configure_form(self):
        flags = appuifw.FFormEditModeOnly | appuifw.FFormDoubleSpaced
        self.form = appuifw.Form(self.data, flags)

        self.form.save_hook = self.save_hook
        appuifw.app.exit_key_handler = self.quit
        appuifw.app.title = u'Selección de cliente'
        appuifw.app.screen='large'


if __name__ == "__main__":
    myapp = Seleccionar_cliente()
    myapp.loop()
