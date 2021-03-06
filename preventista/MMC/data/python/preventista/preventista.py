# -*- coding: utf-8 -*-

from appuifw import Listbox, note, popup_menu, Text, query, app
from data import Data_manager, escape
from debug import debug, tracetofile
from dialogs import Pedido_editor
from formats import Date, DAY
from ilistbox import Ilistbox, list_editor
from time import time, sleep
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
        app.screen = "normal"
        body = self.ilistbox.listbox

        #FIXME: Crear un menú pertinente
        menu = [
            (u"Preparar envío a PC", self.export_all),
            (u"Number selection", self.number_sel),
            (u"Name list", self.name_list),
        ]

        Application.__init__(self, u"Sistema de pedidos", body, menu)


    def update_database(self):
        for filename in os.listdir(INPUT_DIR):
            if filename.endswith(".csv"):
                debug("Cargando los registros actualizados desde %s" % filename)
                tablename = filename[:-4]
                completefilename = INPUT_DIR + u"\\" + filename
                self.create_table(tablename)
                self.data.csv_import(open(completefilename), tablename)
                os.remove(completefilename)

        for table in ("pedidos", "cliente_activo", "pedidos_detalles",
            "zonas", "estado"): 
            self.create_table(table, force=False)


    def export_all(self):
        #TODO: Escribir y exportar sentencias
        sleep(5)
        note(u"Listo para transferir a PC", "info")


    def create_table(self, tablename, force=True):
        schemas = {

            "clientes":  u"""
                CREATE TABLE clientes (
                    COD_CLI INTEGER,
                    NRO_ZON INTEGER,
                    APNBR_CLI VARCHAR,
                    DOM_PART_CLI VARCHAR,
                    EST_CLI VARCHAR,
                    CARACT_ZON VARCHAR
                )
            """,

            "estado": u"""
                CREATE TABLE estado (
                    key VARCHAR,
                    value LONG VARCHAR
                )
            """,

            "zonas": u"""
                CREATE TABLE zonas (
                    NRO_ZON INTEGER,
                    NRO_ZON_PADRE INTEGER,
                    CARACT_ZON VARCHAR
                )
            """,

            "listas_frecuentes": u"""
                CREATE TABLE listas_frecuentes (
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
                )
            """,

            "preventista": u"""
                CREATE TABLE preventista (
                    COD_MOVIL INTEGER,
                    ULTIMO_NRO_PEDIDO INTEGER
                )
            """,

            "productos": u"""
                CREATE TABLE productos (
                    COD_PRODUCTO INTEGER,
                    ID_PRODUCTO INTEGER,
                    NOMBRE_PRODUCTO VARCHAR,
                    MEDIDA_PRODUCTO VARCHAR,
                    COEF_MEDIDA_PRODUCTO INTEGER,
                    PRECIO_PRODUCTO INTEGER,
                    ESTADO_PRODUCTO VARCHAR
                )
            """,

            "pedidos": u"""
                CREATE TABLE pedidos (
                    NRO_PEDIDO INTEGER,
                    COD_CLI INTEGER,
                    NRO_ZON INTEGER,
                    COD_MOVIL INTEGER,
                    COMENTARIO LONG VARCHAR,
                    FECHA_PEDIDO DATE, 
                    FECHA_ENTREGA DATE
                )
            """,

            "pedidos_detalles": u"""
                CREATE TABLE pedidos (
                    NRO_PEDIDO INTEGER,
                    COD_PRODUCTO INTEGER,
                    CANTIDAD_PEDIDO INTEGER,
                    PRECIO_PRODUCTO FLOAT
                )
            """,

            "cliente_activo": u"""
                CREATE TABLE cliente_activo (
                    COD_CLI INTEGER,
                    NRO_ZON INTEGER,
                    APNBR_CLI VARCHAR,
                    DOM_PART_CLI VARCHAR,
                    EST_CLI VARCHAR,
                    CARACT_ZON VARCHAR
                )
            """,

        }

        if tablename in schemas:
            debug(u"Intentando crear tabla %s." % tablename)
            try:
                error = self.data.execute(schemas[tablename])
            except SymbianError, error:
                if "KErrAlreadyExists" in error:
                    if force:
                        debug(u"La tabla ya existía, reiniciandola.")
                        error = self.data.execute(u"""
                            DROP TABLE %s
                        """ % escape(tablename))
                        error = self.data.execute(schemas[tablename])
                    else:
                        debug(u"La tabla ya existía, se deja intacta.")
                else:
                    raise
        else:
            debug(u"No hay un esquema definido para la tabla: %s" % tablename)
            error = False

        return error


    def get_cliente_activo(self):
        cliente = self.data.query_first(u"""
            SELECT * FROM cliente_activo
            """)
        if cliente is None:
            cliente = self.data.query_first(u"""
                SELECT * FROM clientes
                WHERE CARACT_ZON='%s'
                """ % escape(self.get_zona_activa()))

        return cliente


    def set_cliente_activo(self, cliente=None):
        if cliente is None or not self.data.query_count(u"""
                SELECT * FROM clientes
                WHERE APNBR_CLI='%s'
                """ % escape(cliente[2])):
            cliente = self.data.query_first(u"""
                SELECT * FROM clientes
                """)
        debug("Preventista:set_cliente_activo::cliente = %s" % str(cliente))

        self.create_table("cliente_activo")
        values_fmt = """%s, %s, '%s', '%s', '%s', '%s'"""
        values = values_fmt % escape(cliente)
        insert_statement = u"""
            INSERT INTO cliente_activo
            (COD_CLI, NRO_ZON, APNBR_CLI, DOM_PART_CLI, EST_CLI, CARACT_ZON)
            VALUES (%s)
            """ % values
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
            debug("Preventista:update_ilistbox_items:: ilistbox.items = %s" %
                ilistbox.items)
            self.update_cliente_activo(
                ilistbox.items[0][0][1],
                ilistbox.items[1][0][1])
            items = self.get_ilistbox_items()
            ilistbox.set_items(items)


    def get_ilistbox_items(self, own_item=None):
        zona_cliente_activo, nombre_cliente_activo = self.data.query_first(
            u"""
            SELECT CARACT_ZON, APNBR_CLI FROM cliente_activo
            """)

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

        for pedido in self.get_pedidos(self.get_cliente_activo()):
            item_pedido = (
                (
                    u"  Ped. %s para el %s" % pedido[:2],
                    u"  Comentario: %s " % pedido[2]
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
        º
        numero_ultimo_pedido = self.data.query_first(u"""
            SELECT value FROM estado
            WHERE key='NRO_PEDIDO'
            """)
        if numero_ultimo_pedido:
            numero_nuevo_pedido = int(numero_ultimo_pedido) + 1
        else:
            numero_nuevo_pedido = 1

        cliente_activo = self.data.query_first(u"""
            SELECT value FROM estado
            WHERE key='CLIENTE_ACTIVO'
            """)
        if cliente_activo == None:
            cliente_activo = self.get_cliente

        pedido = {
            u'NRO_PEDIDO' : numero_nuevo_pedido,
            u'COD_CLI' : self.cliente_activo[u"COD_CLI"],
            u'NRO_ZON' : self.cliente_activo[u"NRO_ZON"],
            u'COD_MOVIL' : self.preventista[u"COD_MOVIL"],
            u'COMENTARIO' : u"",
            u'FECHA_PEDIDO': unicode(Date(time())),
            u'FECHA_ENTREGA' : unicode(Date(time() + DAY)),
        }
        return pedido


    def update_cliente_activo(self, nombre_zona, nombre_cliente):
        debug("Preventista:update_cliente_activo::zona = %s" % nombre_zona)
        debug("Preventista:update_cliente_activo::cliente = %s" %
            nombre_cliente)
        nuevo_cliente = self.data.query_first(u"""
            SELECT * FROM clientes
            WHERE CARACT_ZON='%s'
            AND APNBR_CLI='%s'
            """ % escape((nombre_zona, nombre_cliente)))
        self.set_cliente_activo(nuevo_cliente)


    def update_clients_list(self, item_clientes, item_modificado, ilistbox):
        if item_modificado[0][0] == u"Zona":
            nueva_zona = item_modificado[0][1]
            nombre_cliente = item_clientes[0][1]
            debug("Zona ha sido cambiada (%s), actualizando lista de clientes."
                % nueva_zona)
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
        zonas_clientes = uniq((item[0] for item in self.data.query(u"""
            SELECT CARACT_ZON FROM clientes
            ORDER BY CARACT_ZON
            """)))

        return zonas_clientes


    def get_pedidos(self, cliente=None):
        if cliente:
            pedidos_cliente = self.data.query(u"""
                SELECT NRO_PEDIDO, FECHA_ENTREGA, COMENTARIO FROM pedidos
                WHERE COD_CLI=%s
                AND NRO_ZON=%s
                """ % (cliente[0], cliente[1]))
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
        nombres_clientes = uniq((item[0] for item in self.data.query(u"""
            SELECT APNBR_CLI FROM clientes
            WHERE CARACT_ZON='%s'
            OR CARACT_ZON='<TODAS>'
            ORDER BY APNBR_CLI
            """ % escape(zona))))

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
