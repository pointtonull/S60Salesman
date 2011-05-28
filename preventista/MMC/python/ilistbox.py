from debug import debug
from appuifw import Listbox

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
                listboxitem, data=None
            and returns the new listboxitem values:
                listboxitem: updates listboxitem only
                listboxitem, itemdata: updates listboxitem and itemdata

            data is the auxiliar data that itemeditor could need.

            change_handler is a callable that acepts this args:
                listboxitem, Ilistbox_instance
            could be used to update another listbox's items

        default_editor, if one, will be used to edit the items withnot explicit
        editor, else a generic string editor will be used.
        """
        
        completed_items = []
        for item in items:
            new_item = [None, None, None, None]
            for pos in xrange(len(item)):
                new_item[pos] = item[pos]
            completed_items.append(new_item)
        self.items = completed_items

        if default_editor:
            self.default_editor = default_editor
        else:
            self.default_editor = edit_str

        self.update_listboxitems()
        appuifw.Listbox.__init__(self, self.listboxitems, self.handler)


    def update_listboxitems(self)
        """
        Updates the list of listbox items

        """
        self.listboxitems = [item[0] for item in items]


    def redraw(self, current_pos=None)
        """
        Updates listbox updating and applying the listbox items
        """
        if not current_pos:
            current_pos = self.current()
        self.update_listboxitems()
        self.set_list(self.listboxitems, current_pos)


    def handler(self):
        """
        Will be called when a item is selected. Calls itemeditor,
        change_handler (if any) and redraw.
        """
        current_pos = self.current()
        current_item = self.items[current_pos]

        listboxitem, itemeditor, itemdata, change_handler = current_item

        itemeditor(listboxitem, itemeditor, itemdata)

        self.redraw(current_pos)


def edit_str(listboxitem, data=None):
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

    return tuple(listboxitem)
