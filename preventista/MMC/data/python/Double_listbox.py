import appuifw, e32
import key_codes

appuifw.app.screen='normal'

app_lock = e32.Ao_lock()

def quit():
    app_lock.signal()

appuifw.app.exit_key_handler = quit

file_icon = appuifw.Icon(u"Z:\\resource\\apps\\avkon2.mif", 17504, 17505)
folder_icon = appuifw.Icon(u"Z:\\resource\\apps\\avkon2.mif", 17506, 17507)

items = [
    (u"Folder1", u"Empty", folder_icon),
    (u"Folder2", u"Empty", folder_icon),
    (u"Folder3", u"Empty", folder_icon),
    (u"Folder4", u"Empty", folder_icon),
    (u"Folder5", u"Empty", folder_icon),
    (u"Folder6", u"Empty", folder_icon),
    (u"Folder7", u"Empty", folder_icon),
    (u"Folder8", u"Empty", folder_icon),
    (u"Folder9", u"Empty", folder_icon),
    (u"Folder10", u"Empty", folder_icon),
    (u"Folder11", u"Empty", folder_icon),
    (u"Folder12", u"Empty", folder_icon),
    (u"File1", u"Unknown type", file_icon),
    (u"File2", u"Unknown type", file_icon),
    (u"File3", u"Unknown type", file_icon),
    (u"File4", u"Unknown type", file_icon),
]

def handle_selection():
    appuifw.note(items[lb.current()][0] + u" has been selected.", 'info')

def refresh():
    print("Evento")
    lb.set_list(items, lb.current())

#Create an instance of Listbox and set it as the application's body
lb = appuifw.Listbox(items, handle_selection)
lb.bind(key_codes.EKeyEdit, refresh)

appuifw.app.body = lb
app_lock.wait()
