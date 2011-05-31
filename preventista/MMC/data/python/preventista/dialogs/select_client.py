#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from auto_dsv import import_dsv
from debug import debug
from ilistbox import Ilistbox, list_editor
from uniq import uniq, sorted
from window import Dialog
import e32


class NameList(Dialog):
    def __init__(self, cbk, names=[]):
        self.names = names
        self.body = Listbox([(u"")],self.options)
        Dialog.__init__(self, cbk, u"Name list", self.body)
 

    def options(self):
        op = popup_menu( [u"Insert", u"Del"] , u"Names:")
        if op is not None:
            if op == 0:
                name = query(u"New name:", "text", u"" )
                if name is not None:
                    self.names.append(name)
                    print(self.names)
            elif self.names:
                del self.names[self.body.current()]
            self.refresh()
 

    def refresh(self):
        menu = []
        if self.names:
            menu = map(lambda x: (x, lambda: None), self.names)
            items = self.names + [u"<empty>"]
        else:
            items = [u"<empty>"]
        self.menu = menu + [(u"Exit", self.close_app)]
        self.body.set_list(items, 0)
        Dialog.refresh(self)


class Select_client(Dialog):
    def __init__(self, callback):
        self.clientes = import_dsv(r"e:\data\input\clientes.csv")
        zonas_clientes = self.get_zonas_clientes()
        nombres_clientes = self.get_nombres_clientes()

        items = [
            (
                (u"Zona", zonas_clientes[0]),
                list_editor, (zonas_clientes, 0, 1),
            ),
            (
                (u"Cliente", nombres_clientes[0]),
                list_editor, (nombres_clientes, 0, 1), self.update_clients_list,
            ),
            ]

        self.ilistbox = Ilistbox(items)
        self.body = self.ilistbox.listbox
        Dialog.__init__(self, callback, u"Seleccionar cliente", self.body)


    def get_zonas_clientes(self):
        zonas_clientes = sorted(uniq([cliente["CARACT_ZON"]
            for cliente in self.clientes]))
        zonas_clientes.insert(0, u"<TODAS>")

        return zonas_clientes


    def get_nombres_clientes(self, zona="<TODAS>"):
        nombres_clientes = sorted(uniq([cliente["APNBR_CLI"]
            for cliente in self.clientes
                if cliente["CARACT_ZON"] == zona or zona==u"<TODAS>"]))

        return nombres_clientes


    def update_clients_list(self, clients_item, changed_item, ilistbox):
        debug("update_clients_list::changed_item[0]: %s" % str(changed_item[0]))
        if changed_item[0][0] == u"Zona":
            debug("Zona ha sido cambiada, actualizando lista de clientes.")
            new_clients = self.get_nombres_clientes(changed_item[0][1])
            position = clients_item[2][1]
            if clients_item[0][1] not in new_clients:
                clients_item[0] = (clients_item[0][0], new_clients[0])
                position = 0
            clients_item[2] = (new_clients, position, 1)
        else:
            debug("Zona no ha sido actualizada")
