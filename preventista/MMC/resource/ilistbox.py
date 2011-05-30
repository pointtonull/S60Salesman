from appuifw import Listbox
from formats import Number
from debug import debug
import appuifw

class Ilistbox: # Cannot inherit because of python version
    def __init__(self, items, default_editor=None):
        """
        Creates a Listbox instance.

        Items is a list with iterables that defines the item behavior:

            [listboxitem, ...]
            [(listboxitem, itemeditor), ...]
            [(listboxitem, itemeditor, data), ...]
            [(listboxitem, itemeditor, data, change_handler), ...]

            Where listboxitem could be:
                unicode: for a single line listbox
                (unicode, Icon): for a single line listbox with icons
                (unicode, unicode): for a double line listbox
                (unicode, unicode, Icon): for a double line listbox with icons

            itemeditor is a callable that acepts this args:
                listboxitem, itemdata=None
            and returns the new listboxitem values:
                listboxitem, itemdata: updates listboxitem and itemdata

            data is the auxiliar data that itemeditor could need.

            change_handler is a callable that acepts this args:
                own_item, changed_item, Ilistbox_instance
            Will be called when some item change their listboxitem or data.

        default_editor, if one, will be used to edit the items withnot explicit
        editor, else a generic string editor will be used.
        """

        debug("ilistbox:Ilistbox:__init__::start")
        if default_editor:
            self.default_editor = default_editor
        else:
            self.default_editor = str_editor
        
        completed_items = []
        for item in items:
            new_item = [None, self.default_editor, None, None]
            for pos in xrange(len(item)):
                if item[pos] is not None:
                    new_item[pos] = item[pos]
            completed_items.append(new_item)
        self.items = completed_items
        debug("ilistbox:Ilistbox:__init__::self.items = %s" % self.items)

        self.update_listboxitems()
        debug("ilistbox:Ilistbox:__init__::self.listboxitems = %s" %
            self.listboxitems)
        self.listbox = Listbox(self.listboxitems, self.handler)
        debug("ilistbox:Ilistbox:__init__::end")


    def update_listboxitems(self):
        """
        Updates the list of listbox items

        """
        self.listboxitems = [item[0] for item in self.items]


    def redraw(self, current_pos=None):
        """
        Updates listbox updating and applying the listbox items
        """
        if not current_pos:
            current_pos = self.listbox.current()
        self.listbox.set_list(self.listboxitems, current_pos)


    def handler(self):
        """
        Will be called when a item is selected. Calls itemeditor,
        change_handler (if any) and redraw.
        """
        changed_pos = self.listbox.current()
        changed_item = self.items[changed_pos]

        listboxitem, itemeditor, itemdata, change_handler = changed_item
        new_listboxitem, new_itemdata = itemeditor(listboxitem, itemdata)
        changed_item[0] = new_listboxitem
        changed_item[2] = new_itemdata

        if listboxitem != new_listboxitem or itemdata != new_itemdata:
            for item in self.items:
                change_handler = item[3]
                if change_handler:
                    result = change_handler(item, changed_item, self)
                    debug("Ilistbox:item %s:change_handler::%s" %
                        (item[0][0], result))
                else:
                    debug("Ilistbox:item %s has no change_handler" % item[0][0])

            self.update_listboxitems()
            self.redraw(changed_pos)

        else:
            debug("Ilistbox:change:no changes were made")

def str_editor(listboxitem, itemdata=None):
    """
    Simple universal text editor.
    """
    strings = [None]
    icon = None
    for element in listboxitem:
        if type(element) is unicode:
            strings.append(element)
        else:
            icon = element
    value = strings.pop()
    label = strings.pop()

    new_value = appuifw.query(u"%s:" % label, "text", value)

    listboxitem = []
    for element in (label, new_value, icon):
        if element:
            listboxitem.append(element)

    return tuple(listboxitem), itemdata


def number_editor(listboxitem, itemdata=None):
    """
    Number editor
    """
    strings = [None]
    icon = None
    for element in listboxitem:
        if type(element) is unicode:
            strings.append(element)
        else:
            icon = element
    value = strings.pop()
    label = strings.pop()

    new_value = u"%s" % Number(appuifw.query(u"%s:" % label, "float",
        Number(value)))

    listboxitem = []
    for element in (label, new_value, icon):
        if element:
            listboxitem.append(element)

    return tuple(listboxitem), itemdata
