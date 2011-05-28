from debug import debug
from appuifw import Listbox

class IListbox(Listbox):
    def __init__(self, items, default_editor=None):
        """
        Creates a Listbox instance.

        Items is a list with tuples that defines the item behavior:

            [listboxitem, ...]
            [(listboxitem, itemeditor), ...]
            [(listboxitem, itemeditor, data), ...]

            Where listboxitem could be:
                unicode: for a single line listbox
                (unicode, Icon): for a single line listbox with icons
                (unicode, unicode): for a double line listbox
                (unicode, unicode, Icon): for a double line listbox with icons

            itemeditor is a callable that acepts this args:
                listboxitem, itemeditor, data=None
            and returns the new listboxitem values:
                listboxitem
                listboxitem, itemeditor
                listboxitem, itemeditor, itemdata

        data is the auxiliar data that itemeditor could need.

        default_editor, if one, will be used to edit the items withnot explicit
        editor, else a generic string editor will be used.
        """

        self.items = items
        self.listboxitems = [item[0] for item in items]

        if default_editor:
            self.default_editor = default_editor
        else:
            self.default_editor = self._default_str_editor

        appuifw.Listbox.__init__(self, listboxitems, self.handler)


    def handler(self):
        currentpos = self.current()
        currentitem = items[currentpos]

        listboxitem = currentitem[0]
        if len(currentitem) > 1:
            itemeditor = currentitem[1]
        else:
            itemeditor = self.default_editor

        if len(currentitem) > 2:
            itemdata = currentitem[2]
        else:
            itemdata = None

        self.listbox.set_list(self.items, self.listbox.current())


def edit_str(listboxitem, itemeditor, data=None):
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
