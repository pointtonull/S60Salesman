# -*- coding: utf-8 -*-
#
# Marcelo Barros de Almeida
# marcelobarrosalmeida (at) gmail.com
# License: GPL3
 
from appuifw import Listbox, note, popup_menu, Text, query
from debug import debug, tracetofile
from window import Application, Dialog
from ilistbox import Ilistbox
from dialogs.select_client import Select_client
 

class Preventista(Application):
    def __init__(self):
        self.txt = u""
        self.names = []
        items = [
            (u"Seleccionar cliente", self.select_client)
            ]
        menu = [
            (u"Text editor", self.text_editor),
            (u"Number selection", self.number_sel),
            (u"Name list", self.name_list),
            ]

        self.ilistbox = Ilistbox(items)
        body = self.ilistbox.listbox
        Application.__init__(self, u"MyApp title", body, menu)
 
    def check_items(self):
        idx = self.body.current()
        try:
            (
                self.select_client,
            )[idx]()
        except:
            tracetofile()
 
    def select_client(self, listboxitem, itemdata):
        def callback():
            if not self.dialog.cancel:
                self.client = self.dialog.ilistbox.items[1][0][1]
                note(self.client, "conf")
            self.refresh()
            return True
 
        try:
            self.dialog = Select_client(callback)
            self.dialog.run()
        except:
            tracetofile()

        return listboxitem, itemdata


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
        ny = popup_menu([u"No", u"Si"], u"Salir?")
        if ny is not None:
            if ny == 1:
                Application.close_app(self)
