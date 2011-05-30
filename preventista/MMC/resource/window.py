# -*- coding: utf-8 -*-
"""

 Marcelo Barros de Almeida
 marcelobarrosalmeida (at) gmail.com

"""

from appuifw import *
import e32
import key_codes
from wmlocale import LABELS
from wmglobals import TOUCH_ENABLED

__all__ = [ "Application", "Dialog" ]

class Window(object):
    """ This class is responsible for holding UI contents like menu, body
        and exit handler and exchanging properly all UI elements for
        the derived classes. Moreover, it may lock/unlock the UI when necessary.
    """
    __ui_lock = False
    
    def __init__(self, title, body, global_menu = None, exit_handler = None):
        """ Creates a new window given a title, body or a set of bodies (for tabbed
            window) and optional global_menu and exit handler. Global menu is
            available for all tabs at bottom or it is used as the default
            menu for non tabbed window

            The list of bodies must have the following format:
                [(tab_text, body, menu),(tab_text, body, menu),...]
            
            where:
                tab_text: unicode string used in tab
                body: a valid body (Listbox, Text or Canvas)
                menu: typical menu            
        """
        self.title = title
        
        if isinstance(body,list):
            self.tabbed = True
            self.bodies = body
            self.body = None
        else:
            self.tabbed = False
            self.bodies = None
            self.body = body
    
        if global_menu is None:
            global_menu = [(LABELS.loc.wi_info_exit, self.close_app)]

        if exit_handler is None:
            exit_handler = self.close_app

        self.global_menu = global_menu
        self.exit_handler = exit_handler
        self.last_tab = 0

    def set_title(self,title):
        " Sets the current application title "
        app.title = self.title = title

    def get_title(self):
        " Returns the current application title "
        return self.title

    def bind(self, key, cbk):
        " Bind a key to the body. A callback must be provided."
        if not TOUCH_ENABLED:
            self.body.bind(key,cbk)
        
    def refresh(self):
        " Update the application itens (menu, body and exit handler) "
        if self.tabbed:
            app.set_tabs([b[0] for b in self.bodies],self.tab_handler)
            self.tab_handler(self.last_tab)
            app.activate_tab(self.last_tab)
        else:
            app.set_tabs([], None)
            app.menu = self.global_menu
            app.body = self.body
        app.title = self.title
        app.exit_key_handler = self.exit_handler

    def tab_handler(self,idx):
        " Update tab and its related contents "
        self.last_tab = idx
        self.body = self.bodies[idx][1]
        self.menu = self.bodies[idx][2] + self.global_menu
        app.title = self.title
        app.menu = self.menu
        app.body = self.body
        
    def run(self):
        " Show the dialog/application "
        self.refresh()
        
    def lock_ui(self,title = u""):
        """ Lock UI (menu, body and exit handler are disabled).
            You may set a string to be shown in the title area.
        """
        Window.__ui_lock = True
        app.menu = []
        app.set_tabs([], None)
        app.exit_key_handler = lambda: None
        if title:
            app.title = title

    def unlock_ui(self):
        "Unlock UI. Call refresh() for restoring menu, body and exit handler."
        Window.__ui_lock = False

    def ui_is_locked(self):
        "Chech if UI is locked or not, return True or False"
        return Window.__ui_lock

class Application(Window):
    """ This class represents the running application itself
        and it is responsible for handling the termination semaphore.
        Only one Application class must be instantiated per application.
    """
    __highlander = None
    __lock = None
    
    def __init__(self, title, body, menu = None, exit_handler = None):
        """ Only one application is allowed. It is resposible for starting
            and finishing the program.
            run() is overrided for controling this behavior.
        """
        if Application.__highlander:
            raise "Only one Application() allowed"
        Application.__highlander = self

        if not Application.__lock:
            Application.__lock = e32.Ao_lock()

        Window.__init__(self, title, body, menu, exit_handler)

    def close_app(self):
        """ Signalize the application lock, allowing run() to terminate the application.
        """
        Application.__lock.signal()
            
    def run(self):
        """ Show the the application and wait until application lock is
            signalized. After that, make all necessary cleanup.
        """
        old_title = app.title
        self.refresh()        
        Application.__lock.wait()
        # restore everything !
        app.set_tabs( [], None )
        app.title = old_title
        app.menu = []
        app.body = None
        app.set_exit()        

class Dialog(Window):
    """ This class is in the charge of showing/hiding dialogs when necessary.
        Many dialogs are allowed, each one with their own set of body+menu+exit
        handler.
    """
    def __init__(self, cbk, title, body, menu = None, exit_handler = None):
        """ Create a dialog. cbk is called when dialog is closing.
            Dialog contents, like title and body need
            to be specified. If menu or exit_handler are not specified,
            defautl values for dialog class are used. 
        """
        self.cbk = cbk
        self.cancel = False        
        Window.__init__(self, title, body, menu, exit_handler)

    def close_app(self):
        """ When closing the dialog, a call do self.cbk() is done.
            If this function returns True the dialog is not refreshed
            and the latest dialog/window takes control. If something fails
            during calback execution, callback function should return False
            and does not call refresh(). Using self.cancel it is possible
            to determine when the dialog  was canceled or not. 
        """
        if self.cbk() == False:
            self.refresh()

    def cancel_app(self):
        """ Close the dialog but turn the cancel flag on.
        """
        self.cancel = True
        self.close_app()
