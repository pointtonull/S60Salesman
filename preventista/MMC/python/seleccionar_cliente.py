#!/usr/bin/env python
#-*- coding: UTF-8 -*-

#    def save_hook(self, data):
#        print("save_hook::%s" % data)
#        if data != self.data:
#            control_zona = data[0]
#            zona = control_zona[2][control_zona[3]]
#            nombres_clientes = sorted(uniq([cliente["APNBR_CLI"]
#                for cliente in self.cliente
#                    if cliente["CARACT_ZON"] == zona]))
#            control_cliente = (u'Cliente','combo', (nombres_clientes, 0))
#            control_prueba_int = data[2][0], data[2][1], data[2][2] + 1
#            data[1] = control_cliente
#            data[2] = control_prueba_int
#            self.data = data
#        return False
#    def loop(self):
##        appuifw.app.body = self.form
#        self.app_lock.wait()


#    def quit(self):
#        print("Nabo")


#    def configure_form(self):
#        flags = appuifw.FFormEditModeOnly | appuifw.FFormDoubleSpaced
#        self.form = appuifw.Form(self.data, flags)

#        self.form.save_hook = self.save_hook
#        appuifw.app.exit_key_handler = self.quit
#        appuifw.app.title = u'Selección de cliente'
#        appuifw.app.screen='large'


#if __name__ == "__main__":
#    myapp = Seleccionar_cliente()
#    myapp.loop()

from appuifw import Listbox, note
from auto_dsv import import_dsv
from uniq import uniq, sorted
from window import Application
import e32

class MyApp(Application):
    def __init__(self):
        self.clientes = import_dsv(r"c:\\python\data\input\clientes.csv")
        self.data = self.get_data() 
        file = open("salida.txt", "w")
        file.write(str(self.data))
        file.close()

        items = [
                    (u"Zona", u"Zona1"),
                    (u"Cliente", u"Cliente1"),
                    (u"Option C", u"No Se")
                ]

        menu = [ (u"Menu A", self.option_a),
                 (u"Menu B", self.option_b),
                 (u"Menu C", self.option_c) ]

        body = Listbox(items, self.check_items)
        Application.__init__(self,
                             u"MyApp title",
                             body,
                             menu)

    def get_data(self):
        zonas_clientes = sorted(uniq([cliente["CARACT_ZON"]
            for cliente in self.clientes]))
        control_zona = (u'Zona', 'combo', (zonas_clientes, 0))
        zona = zonas_clientes[0]

        nombres_clientes = sorted(uniq([cliente["APNBR_CLI"]
            for cliente in self.clientes
                if cliente["CARACT_ZON"] == zona]))
        control_cliente = (u'Cliente','combo', (nombres_clientes, 0))
        data = [
            control_zona,
            control_cliente,
        ]

#        (u'Mobile','text', u'Nokia')
#        (u'Date', 'date')
#        (u"Date", 'date', time.time())
#        (u'Prueba','number', randrange(10))
#        (u'Time', 'time')

        return data


    
    def check_items(self):
        idx = self.body.current()
        (self.option_a, self.option_b, self.option_c )[idx]()

    def option_a(self):
        note(u"A","info")
    def option_b(self):
        note(u"B","info")
    def option_c(self):
        note(u"C","info")


if __name__ == "__main__":

    app = MyApp()
    app.run()
    app.__lock.app_lock.signal() 
