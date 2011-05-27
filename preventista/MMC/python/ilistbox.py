from debug import debug

class IListbox():
    def __init__(self, items, callback=None):
        """
        Creates a Listbox instance.

        Items is a list with tuples that defines the item behavior:

            [listboxitem, ...]
            [(listboxitem, itemeditor), ...]
            [(listboxitem, itemeditor, data), ...]

            Where listboxitem could be:
                unicode: for a single lien listbox
                (unicode, Icon): for a single line listbox with icons
                (unicode, unicode): for a double line listbox
                (unicode, unicode, Icon): for a double line listbox with icons

            itemeditor is a callable that acepts this args:
                listboxitem, itemeditor, data=None
            and returns the new listboxitem value:
                listboxitem
                listboxitem, itemeditor
                listboxitem, itemeditor, data

        data is the auxiliar data that itemeditor could need.

        callback, if one, will be the default itemeditor.
        """
