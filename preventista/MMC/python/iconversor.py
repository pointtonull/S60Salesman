from formats import Number
from key_codes import *
import appuifw
import e32
from ilistbox import Ilistbox, str_editor, number_editor


class Converter(object):
    def __init__(self, items):
        items = [
            ((u"ARS", u"06,00"), number_editor),
            ((u"EUR", u"01,00"), number_editor),
            ((u"MEX", u"16,95"), number_editor),
            ((u"USD", u"01,47"), number_editor),
        ]
        appuifw.app.exit_key_handler = self.quit
        self.app_lock = e32.Ao_lock()

        self.listbox = Ilistbox(items, handler)

        def configure(self):
            appuifw.app.body = self.listbox

        def loop(self):
            self.configure()
            self.app_lock.wait()

        def quit(self):
            self.app_lock.signal()


class Oldway
        self.listbox.bind(EKeyRightArrow, lambda:self.move('right'))
        self.listbox.bind(EKeyLeftArrow, lambda:self.move('left'))

    def handle_selection(self):
        label = self.items[self.listbox.current()][0]
        value = self.items[self.listbox.current()][1]
        new_value = appuifw.query(label + ":", "float", Number(value))
        self.change(self.listbox.current(), new_value)

    def change(self, position, value):
        unit = self.relation[position][1]
        items = [(item[0], u"%s" % Number(item[1] * value / unit))
            for item in self.relation]
        self.update(items)

    def update(self, items, current=None):
        self.items = items
        if current is None:
            current = self.listbox.current()
        self.listbox.set_list(self.items, self.listbox.current())


if __name__ == "__main__":
    app = Converter()
    app.loop()
