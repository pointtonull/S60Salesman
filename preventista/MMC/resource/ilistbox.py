from appuifw import Listbox
from debug import debug
import appuifw

class IListbox(Listbox):
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

            change_handler is a callable that acepts this Ilistbox_instance as
            argumner. Could call anothers listbox's items change_handlers.
            Will be called when listboxitem or data are modified.

        default_editor, if one, will be used to edit the items withnot explicit
        editor, else a generic string editor will be used.
        """

        if default_editor:
            self.default_editor = default_editor
        else:
            self.default_editor = edit_str
        
        completed_items = []
        for item in items:
            new_item = [None, self.default_editor, None, None]
            for pos in xrange(len(item)):
                if item[pos] is not None:
                    new_item[pos] = item[pos]
            completed_items.append(new_item)
        self.items = completed_items

        self.listboxitems = []
        self.update_listboxitems()
        Listbox.__init__(self, self.listboxitems, self.handler)


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
            current_pos = self.current()
        self.set_list(self.listboxitems, current_pos)


    def handler(self):
        """
        Will be called when a item is selected. Calls itemeditor,
        change_handler (if any) and redraw.
        """
        current_pos = self.current()
        current_item = self.items[current_pos]

        listboxitem, itemeditor, itemdata, change_handler = current_item
        new_listboxitem, new_itemdata = itemeditor(listboxitem, itemdata)
        current_item[0] = new_listboxitem
        current_item[2] = new_itemdata

        self.update_listboxitems()
        
        if change_handler:
            if listboxitem != new_listboxitem or itemdata != new_itemdata:
                debug("Ilistbox:change:change_handler::%s" %
                    change_handler(self))
            else:
                debug("Ilistbox:change:no changes were made")
        else:
            debug("Ilistbox:no change_handler")

        self.update_listboxitems()
        self.redraw(current_pos)


def edit_str(listboxitem, itemdata=None):
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
