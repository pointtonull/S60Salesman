import appuifw
import e32
from key_codes import *
 

class Converter(object):
    def __init__(self, items, handler=None):
        self.items = items
        self.relation = [(item[0], float(item[1])) for item in items]
        appuifw.app.exit_key_handler = self.quit
        self.app_lock = e32.Ao_lock()

        if handler is None:
            handler = self.handle_selection

        self.listbox = appuifw.Listbox(items, handler)
        self.listbox.bind(EKeyRightArrow, lambda:self.move('right'))
        self.listbox.bind(EKeyLeftArrow, lambda:self.move('left'))

    def handle_selection(self):
        label = self.items[self.listbox.current()][0]
        value = self.items[self.listbox.current()][1]
        new_value = appuifw.query(label + ":", "float", float(value))
        self.change(self.listbox.current(), new_value)

    def configure(self):
        appuifw.app.body = self.listbox

    def move(self, direction):
        change = {'right': 1, 'left': -1}.get(direction, 0)
        old_value = float(self.items[self.listbox.current()][1])
        if change > 0:
            new_value = int(old_value + change)
        else:
            new_value = int(old_value + change + .99)
        self.change(self.listbox.current(), new_value)

    def change(self, position, value):
        unit = self.relation[position][1]
        items = [(item[0], u"%.2f" % (item[1] * value / unit))
            for item in self.relation]
        self.update(items)
 
    def update(self, items, current=None):
        self.items = items
        if current is None:
            current = self.listbox.current()
        self.listbox.set_list(self.items, self.listbox.current())

    def loop(self):
        self.configure()
        self.app_lock.wait()

    def quit(self):
        self.app_lock.signal()


if __name__ == "__main__":
    items = [
        (u"ARS", u"6.00"),
        (u"EUR", u"1.00"),
        (u"MEX", u"16.95"),
        (u"USD", u"1.47"),
    ]
    app = Converter(items)
    app.loop()
