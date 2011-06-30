# -*- coding: utf-8 -*-

from appuifw import Listbox, note, popup_menu, Text, query
from data import Data_manager, escape
from debug import debug, tracetofile
from dialogs import Pedido_editor
from formats import Date, DAY
from ilistbox import Ilistbox, list_editor
from time import time
from uniq import uniq
from window import Application, Dialog
import os

SD_LETTER = "e"
INPUT_DIR = ur"%s:\data\input" % SD_LETTER
OUTPUT_DIR = ur"%s:\data\output" % SD_LETTER
MOVIL_DIR = ur"%s:\data\movil" % SD_LETTER
DBFILE = ur"%s\preventista.db" % MOVIL_DIR

class Preventista(Application):
    def __init__(self):
        self.data = Data_manager(DBFILE)
        self.update_database()
        self.set_cliente_activo()

        self.ilistbox = Ilistbox(self.get_ilistbox_items())

        body = self.ilistbox.listbox

        #FIXME: Crear un menú pertinente
        menu = [
            (u"Text editor", self.text_editor),
            (u"Number selection", self.number_sel),
            (u"Name list", self.name_list),
        ]

        Application.__init__(self, u"MyApp title", body, menu)


    def update_database(self):
        for filename in os.listdir(INPUT_DIR):
            if filename.endswith(".csv"):
                debug("Cargando los registros actualizados desde %s" % filename)
                tablename = filename[:-4]
                completefilename = INPUT_DIR + u"\\" + filename
                self.create_table(tablename)
                self.data.csv_import(open(completefilename), tablename)
                os.remove(completefilename)


    def create_table(self, tablename):
        schemas = {

            "cliente_activo": u"""CREATE TABLE cliente_activo (
                COD_CLI INTEGER,
                NRO_ZON INTEGER,
                APNBR_CLI VARCHAR,
                DOM_PART_CLI VARCHAR,
                EST_CLI VARCHAR,
                CARACT_ZON VARCHAR
            )""",

            "clientes":  u"""CREATE TABLE clientes (
                COD_CLI INTEGER,
                NRO_ZON INTEGER,
                APNBR_CLI VARCHAR,
                DOM_PART_CLI VARCHAR,
                EST_CLI VARCHAR,
                CARACT_ZON VARCHAR
            )""",

            "listas_frecuentes": u"""CREATE TABLE listas_frecuentes (
                COD_CLI INTEGER,
                COD_ZONA INTEGER,
                COD_PRODUCTO INTEGER,
                ID_PRODUCTO INTEGER,
                NOMBRE_PRODUCTO VARCHAR,
                MEDIDA_PRODUCTO VARCHAR,
                CANTIDAD INTEGER,
                PRECIO_PRODUCTO INTEGER,
                COEF_MEDIDA_PRODUCTO INTEGER,
                PCIO_TOTAL INTEGER
            )""",

            "preventista": u"""CREATE TABLE preventista (
                COD_MOVIL INTEGER,
                ULTIMO_NRO_PEDIDO INTEGER
            )""",

            "productos": u"""CREATE TABLE productos (
                COD_PRODUCTO INTEGER,
                ID_PRODUCTO INTEGER,
                NOMBRE_PRODUCTO VARCHAR,
                MEDIDA_PRODUCTO VARCHAR,
                COEF_MEDIDA_PRODUCTO INTEGER,
                PRECIO_PRODUCTO INTEGER,
                ESTADO_PRODUCTO VARCHAR
            )"""
        }

        if tablename in schemas:
            debug(u"Intentando crear tabla %s." % tablename)
            try:
                error = self.data.execute(schemas[tablename])
            except SymbianError, error:
                if "KErrAlreadyExists" in error:
                    debug(u"La tabla ya existía, reiniciandola.")
                    drop_sql = u"DROP TABLE %s" % tablename
                    error = self.data.execute(drop_sql)
                    error = self.data.execute(schemas[tablename])
                else:
                    raise
        else:
            debug(u"No hay un esquema definido para la tabla: %s" % tablename)
            error = False

        return error


    def get_cliente_activo(self):
        return self.data_query_first(u"SELECT * FROM cliente_activo")


    def set_cliente_activo(self, cliente=None):
        if cliente is None or cliente in self.data.query(
            "SELECT * FROM clientes"):
            cliente = self.data.query_first(u"SELECT * FROM clientes")

        self.create_table("cliente_activo")
        values_fmt = """%d, %d, '%s', '%s', '%s', '%s'"""
        values = values_fmt % cliente
        insert_statement = u"""INSERT INTO cliente_activo
            (COD_CLI, NRO_ZON, APNBR_CLI, DOM_PART_CLI,
            EST_CLI, CARACT_ZON) VALUES (%s)""" % values
        return self.data.execute(insert_statement)


    def edit_pedido(self, listboxitem, pedido):
        def callback():
            if self.dialog.cancel:
                note(u"Pedido cancelado", "conf")
            else:
                self.pedidos.append(pedido)
                note(u"Pedido guardado", "info")
            self.refresh()
            return True

        if not pedido:
            pedido = self.get_nuevo_pedido()

        nombre_cliente = self.cliente_activo[u"APNBR_CLI"]
        try:
            self.dialog = Pedido_editor(callback, nombre_cliente, pedido,
                self.pedidos_detalles, self.productos)
            self.dialog.run()
        except:
            tracetofile()
        return listboxitem, pedido



    def update_ilistbox_items(self, own_item, changed_item, ilistbox):
        if changed_item[0][0] in (u"Zona", u"Cliente"):
            debug("preventista:update_ilistbox_items:: ilistbox.items = %s" %
                ilistbox.items)
            self.update_cliente_activo(
                ilistbox.items[0][0][1],
                ilistbox.items[1][0][1])
            items = self.get_ilistbox_items()
            ilistbox.set_items(items)


    def get_ilistbox_items(self, own_item=None):
        zona_cliente_activo, nombre_cliente_activo = self.data.query_first(
            u"SELECT CARACT_ZON, APNBR_CLI FROM cliente_activo")

        zonas_clientes = self.get_zonas_clientes()
        nombres_clientes = self.get_nombres_clientes(zona_cliente_activo)

        items = [
            (
                (u"Zona", zona_cliente_activo),
                list_editor, (zonas_clientes, 0, 1),
            ),
            (
                (u"Cliente", nombre_cliente_activo),
                list_editor, (nombres_clientes, 0, 1), self.update_clients_list,
            ),
        ]

        for pedido in self.get_pedidos(self.cliente_activo):
            item_pedido = (
                (
                    u"  Ped. %s para el %s" % (           
                    pedido[u"NRO_PEDIDO"],
                        unicode(Date(pedido[u"FECHA_ENTREGA"]))),
                    u"  Comentario: %s " % pedido[u"COMENTARIO"]
                ),
                self.edit_pedido, pedido,
                self.update_ilistbox_items
            )
            items.append(item_pedido)

        item_pedido_nuevo = (
                (u"Añadir pedido", u"Crea un pedido nuevo"),
                self.edit_pedido, None,
                self.update_ilistbox_items
        ) 

        items.append(item_pedido_nuevo)
        return items


    def get_nuevo_pedido(self):
        pedido = {
            u'NRO_PEDIDO' :
                unicode(int(self.preventista[u"ULTIMO_NRO_PEDIDO"]) + 1),
            u'COD_CLI' : self.cliente_activo[u"COD_CLI"],
            u'NRO_ZON' : self.cliente_activo[u"NRO_ZON"],
            u'COD_MOVIL' : self.preventista[u"COD_MOVIL"],
            u'COMENTARIO' : u"",
            u'FECHA_PEDIDO': unicode(Date(time())),
            u'FECHA_ENTREGA' : unicode(Date(time() + DAY)),
        }
        return pedido


    def update_cliente_activo(self, nombre_zona, nombre_cliente):
        debug("Preventista:update_cliente_activo::zona = %s, cliente = %s" %
            (nombre_zona, nombre_cliente))
        nuevos_clientes = [cliente for cliente in self.clientes
            if cliente[u"CARACT_ZON"] == nombre_zona
                and cliente[u"APNBR_CLI"] == nombre_cliente]
        debug(nuevos_clientes)
        nuevo_cliente = nuevos_clientes[0]
        self.cliente_activo = nuevo_cliente
        self.data.tofile(MOVIL_DIR % "cliente_activo.csv" ,
            [nuevo_cliente])


    def update_clients_list(self, item_clientes, item_modificado, ilistbox):
        if item_modificado[0][0] == u"Zona":
            nueva_zona = item_modificado[0][1]
            nombre_cliente = item_clientes[0][1]
            debug("Zona ha sido cambiada, actualizando lista de clientes.")
            clientes = sorted(self.get_nombres_clientes(nueva_zona))
            posicion = item_clientes[2][1]
            if item_clientes[0][1] not in clientes:
                item_clientes[0] = (item_clientes[0][0], clientes[0])
                self.update_cliente_activo(item_modificado[0][1],
                    item_clientes[0][1])
                posicion = 0
            item_clientes[2] = (clientes, posicion, 1)
        else:
            debug("Zona no ha sido actualizada")


    def get_zonas_clientes(self):
        zonas_clientes = sorted(uniq(
            self.data.query(u"SELECT CARACT_ZON FROM clientes")))

        return zonas_clientes


    def get_pedidos(self, cliente=None):
        if cliente:
            pedidos_cliente = [pedido
                for pedido in self.pedidos
                    if pedido[u"COD_CLI"] == self.cliente_activo[u"COD_CLI"] and
                        pedido[u"NRO_ZON"] == self.cliente_activo[u"NRO_ZON"]]
            return pedidos_cliente
        else:
            return self.pedidos


    def get_pedido_detalles(self, pedido):
        pedido_detalles = [detalle
            for detalle in self.pedidos_detalles
                if detalle[u"NRO_PEDIDO" == pedido[u"NRO_PEDIDO"]]
        ]
        return pedido_detalles


    def get_nombres_clientes(self, zona="<TODAS>"):
        nombres_clientes = sorted(uniq(
            self.data.query(u"""SELECT APNBR_CLI FROM clientes
                WHERE CARACT_ZON='%s'
                OR CARACT_ZON='<TODAS>'""" % escape(zona))))

        return nombres_clientes


    def text_editor(self):
        def cbk():
            if not self.dlg.cancel:
                self.txt = self.dlg.body.get()
                note(self.txt, "info")
            self.refresh()
            return True
        self.dlg = Notepad(cbk, self.txt)
        self.dlg.run()

    def number_sel(self):
        def cbk():
            if not self.dlg.cancel:
                val = self.dlg.items[self.dlg.body.current()]
                try:
                    n = int(val)
                except:
                    note(u"Invalid number", "info")
                    return False
                note(u"Valid number", "info")
            self.refresh()
            return True

        self.dlg = NumSel(cbk)
        self.dlg.run()

    def name_list(self):
        def cbk():
            if not self.dlg.cancel:
                self.names = self.dlg.names
            self.refresh()
            return True

        self.dlg = NameList(cbk, self.names)
        self.dlg.run()

    def close_app(self):
        answer = popup_menu([u"No", u"Si"], u"Salir?")
        if answer is not None:
            if answer == 1:
                Application.close_app(self)
