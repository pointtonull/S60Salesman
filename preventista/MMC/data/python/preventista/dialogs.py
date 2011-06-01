#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from debug import debug
from ilistbox import Ilistbox, list_editor, text_editor, date_editor
from formats import Date
from ilistbox import dummy_editor
from uniq import uniq
from window import Dialog
import e32


class Pedido_editor(Dialog):
    def __init__(self, callback, nombre_cliente, pedido):
        items = (
            ((u"Cliente", nombre_cliente), dummy_editor),
            ((u"Fecha entrega",
                unicode(Date(pedido[u"FECHA_ENTREGA"]))), date_editor),
            ((U"Comentario", pedido[u"COMENTARIO"]), text_editor), 
        ) 
        debug(items)
        self.ilistbox = Ilistbox(items)
        self.body = self.ilistbox.listbox
        Dialog.__init__(self, callback, u"Editar pedido", self.body)


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

 
class Notepad(Dialog):
    def __init__(self, cbk, txt=u""):
        menu = [
            (u"Save", self.close_app),
            (u"Discard", self.cancel_app)
            ]
        Dialog.__init__(self, cbk, u"Preventista", Text(txt), menu)
 
class NumSel(Dialog):
    def __init__(self, cbk):
        self.items = [ u"1", u"2", u"a", u"b" ]
        Dialog.__init__(self, cbk, u"Select a number", Listbox(self.items,
            self.close_app))
