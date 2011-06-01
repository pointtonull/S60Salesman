from appuifw import Listbox, selection_list
from formats import Number
from debug import debug, tracetofile
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
                listboxitem, itemdata
            updates listboxitem and itemdata and returns the new values:
                listboxitem, itemdata

            data is the auxiliar data that itemeditor could need.

            change_handler is a callable that acepts this args:
                own_item, changed_item, Ilistbox_instance
            Will be called when some item change their listboxitem or data.

        default_editor, if one, will be used to edit the items withnot explicit
        editor, else a generic dummy editor will be used.
        """

        if default_editor:
            self.default_editor = default_editor
        else:
            self.default_editor = dummy_editor
        
        self.set_items(items)
        self.update_listboxitems()
        self.listbox = Listbox(self.listboxitems, self.handler)


    def set_items(self, items):
        completed_items = []
        for item in items:
            new_item = [None, self.default_editor, None, None]
            for index, element in enumerate(item):
                if element is not None:
                    new_item[index] = element
            completed_items.append(new_item)
        self.items = completed_items


    def update_listboxitems(self):
        """
        Updates the list of listbox items

        """
        listboxitems = [item[0] for item in self.items]
        for index, item in enumerate(listboxitems):
            if isinstance(item, unicode):
                listboxitems[index] = item
            else:
                new_item = []
                for element in item:
                    new_item.append(element)
                listboxitems[index] = tuple(new_item)
        self.listboxitems = listboxitems
        debug("Ilistbox:update_listboxitems::listboxitems = %s" % listboxitems)


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
        change_handler (if any) and redraw if needed.
        """
        changed_pos = self.listbox.current()
        changed_item = self.items[changed_pos]

        # Editing item
        listboxitem, itemeditor, itemdata, change_handler = changed_item
        try:
            new_listboxitem, new_itemdata = itemeditor(listboxitem, itemdata)
        except:
            tracetofile()
        changed_item[0] = new_listboxitem
        changed_item[2] = new_itemdata

        if listboxitem != new_listboxitem or itemdata != new_itemdata:
            debug("Ilistbox:handler::changed were made: new_listboxitem = %s" %
                str(new_listboxitem))

            # Calling all the change handlers
            for item in self.items:
                change_handler = item[3]
                if change_handler:
                    try:
                        result = change_handler(item, changed_item, self)
                    except:
                        tracetofile()
                    debug("Ilistbox:item %s:change_handler::%s" %
                        (item[0][0], result))
                    debug("Ilistbox:item %s:post::chaged_item = %s" %
                        (item[0][0], changed_item))
                else:
                    debug("Ilistbox:item %s has no change_handler" % item[0][0])

            # Updating view
            self.update_listboxitems()
            self.redraw(changed_pos)

        else:
            debug("Ilistbox:handler:no changes were made")


def dummy_edit(listboxitem, itemdata=None):
    """
    Just do nothing. Is the default editor.
    """
    return listboxitem, itemdata


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
    
    new_value = appuifw.query(u"%s:" % label, "float", Number(value))
    new_value = unicode(Number(new_value))

    listboxitem = []
    for element in (label, new_value, icon):
        if element:
            listboxitem.append(element)

    return tuple(listboxitem), itemdata
    

def list_editor(listboxitem, itemdata=None):
    """
    List editor, asumes:
        itemdata = (choices, current_index, search_field)

        choices: is a list of unicode strings
        current_index: is the index of the last selected item
        searchfield: could be 0 or 1
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

    choices, current_index, search_field = itemdata

    new_index = selection_list(choices, search_field=search_field)
    if new_index is None:
        new_index = 0
    new_value = unicode(choices[new_index])

    listboxitem = []
    for element in (label, new_value, icon):
        if element:
            listboxitem.append(element)

    itemdata = (choices, current_index, search_field)

    return tuple(listboxitem), itemdata

#        Quey options
#        (u'Mobile','text', u'Nokia')
#        (u'Date', 'date')
#        (u"Date", 'date', time.time())
#        (u'Prueba','number', randrange(10))
#        (u'Time', 'time')

