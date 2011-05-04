
# -*- coding: utf-8 -*-
#
# Marcelo Barros de Almeida
# marcelobarrosalmeida (at) gmail.com
# License: GPL3
 
from window import Application, Dialog
from appuifw import Listbox, note, popup_menu, Text, query, app
 
class Notepad(Dialog):
    def __init__(self, cbk, txt=u""):
        menu = [(u"Save", self.close_app),
                (u"Discard", self.cancel_app)]
        Dialog.__init__(self, cbk, u"MyDlg title", Text(txt), menu)
 
class NumSel(Dialog):
    def __init__(self, cbk):
        self.items = [ u"1", u"2", u"a", u"b" ]
        Dialog.__init__(self, cbk,
                        u"Select a number",
                        Listbox(self.items, self.close_app))
 
class NameList(Dialog):
    def __init__(self, cbk, names=[]):
        self.names = names
        self.body = Listbox([(u"")],self.options)
        # Do not populate Listbox() ! Refresh will do this.
        Dialog.__init__(self, cbk, u"Name list", self.body)
 
    def options(self):
        op = popup_menu( [u"Insert", u"Del"] , u"Names:")
        if op is not None:
            if op == 0:
                name = query(u"New name:", "text", u"" )
                if name is not None:
                    self.names.append(name)
                    print self.names
            elif self.names:
                del self.names[self.body.current()]
            # Menu and body are changing !
            # You need to refresh the interface.
            self.refresh()
 
    def refresh(self):
        menu = []
        if self.names:
            menu = map(lambda x: (x, lambda: None), self.names)
            items = self.names
        else:
            items = [u"<empty>"]
        self.menu = menu + [(u"Exit", self.close_app)]
        self.body.set_list(items,0)
        # Since your self.menu and self.body have already defined their
        # new values, call base class refresh()
        # PSZY:Another way to refresh the body,in this way ,you can even change the body to another type
            #appuifw.app.body = None
            #del self.body
            #self.body = appuifw.Listbox(self.items,self.options)
            #Dialog.refresh(self)
 
        Dialog.refresh(self)
 
class MyApp(Application):
    def __init__(self):
        self.txt = u""
        self.names = []
        items = [ u"Text editor",
                  u"Number selection",
                  u"Name list" ]
        menu = [ (u"Text editor", self.text_editor),
                 (u"Number selection", self.number_sel),
                 (u"Name list", self.name_list) ]
        body = Listbox(items, self.check_items )
        Application.__init__(self,
                             u"MyApp title",
                             body,
                             menu)
 
    def check_items(self):
        idx = self.body.current()
        ( self.text_editor, self.number_sel, self.name_list )[idx]()
 
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
        ny = popup_menu( [u"No", u"Yes"], u"Exit ?")
        if ny is not None:
            if ny == 1:
                Application.close_app(self)
 
if __name__ == "__main__":
 
    app = MyApp()
    app.run()
