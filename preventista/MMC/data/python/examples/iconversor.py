from formats import Number
from ilistbox import Ilistbox, str_editor, number_editor
import appuifw
import e32


class Converter(object):
    def __init__(self):
        items = [
            ((u"ARS", u"6,00"), number_editor, 6., update_divisa),
            ((u"EUR", u"1,00"), number_editor, 1., update_divisa),
            ((u"MEX", u"16,95"), number_editor, 16.95, update_divisa),
            ((u"USD", u"1,47"), number_editor, 1.47, update_divisa),
        ]

        appuifw.app.exit_key_handler = self.quit
        self.app_lock = e32.Ao_lock()

        self.ilistbox = Ilistbox(items)

    def configure(self):
        appuifw.app.body = self.ilistbox.listbox

    def loop(self):
        self.configure()
        self.app_lock.wait()

    def quit(self):
        self.app_lock.signal()


def update_divisa(self, changed, ilistbox):
    self_label, self_value = self[0]
    self_divisa = self[2]

    changed_label, changed_value = changed[0]
    changed_divisa = changed[2]
    changed_value = Number(changed_value)

    new_value = (changed_value / changed_divisa) * self_divisa
    new_value = unicode(Number(new_value))

    self[0] = (self_label, new_value)
    return True


if __name__ == "__main__":
    app = Converter()
    app.loop()
