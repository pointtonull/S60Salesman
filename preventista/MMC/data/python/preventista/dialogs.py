#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from debug import debug
from formats import Date
from ilistbox import Ilistbox, list_editor, text_editor, date_editor
from ilistbox import dummy_editor
from uniq import uniq
from window import Dialog
import e32


class Pedido_editor(Dialog):
    def __init__(self, callback, nombre_cliente, pedido, pedidos_detalles,
            productos):
        self.nombre_cliente = nombre_cliente
        self.pedido = pedido
        self.pedidos_detalles = pedidos_detalles
        self.productos = productos
        items = self.get_ilistbox_items()
        self.ilistbox = Ilistbox(items)
        self.body = self.ilistbox.listbox
        Dialog.__init__(self, callback, u"Editar pedido", self.body)


    def get_ilistbox_items(self):
        items = []
        items.append(
            ((u"Cliente", self.nombre_cliente),
                dummy_editor)
        )
        fecha_entrega = unicode(Date(self.pedido[u"FECHA_ENTREGA"]))
        items.append(
            ((u"Fecha entrega", fecha_entrega),
                date_editor)
        )
        nro_pedido = self.pedido[u"NRO_PEDIDO"]
        for detalle in self.pedidos_detalles:
            if detalle[u"NRO_PEDIDO"] == nro_pedido:
                codigo = detalle[u"COD_PRODUCTO"]
                producto = [producto for producto in self.productos
                    if producto[u"COD_PRODUCTO"] == codigo][0]
                nombre = producto[u"NOMBRE_PRODUCTO"]
                medida = producto[u"MEDIDA_PRODUCTO"]
                precio_original = producto[u"PRECIO_PRODUCTO"]
                cantidad = detalle[u"CANTIDAD_PEDIDO"]
                precio_pedido = detalle[u"PRECIO_PRODUCTO"]
                items.append(
            ((nombre, u"%s x %s x %s" % (cantidad, medida, precio_pedido)),
                dummy_editor)
                )
        items.append(
            ((u"Agregar articulo", u"Click para seleccionar un nuevo producto"),
                dummy_editor)
        )
        items.append(((U"Comentario", self.pedido[u"COMENTARIO"]), text_editor))
        return items

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
