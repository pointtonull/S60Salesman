import appuifw, e32


app_lock = e32.Ao_lock()

def quit():
    app_lock.signal()

appuifw.app.exit_key_handler = quit

file_icon = appuifw.Icon(u"Z:\\resource\\apps\\avkon2.mif", 17504, 17505)
folder_icon = appuifw.Icon(u"Z:\\resource\\apps\\avkon2.mif", 17506, 17507)

items = [
    (u"File", u"Unknown type", file_icon),
    (u"Folder", u"Empty", folder_icon),
    (u"Otro", u"Empty", folder_icon),
]

def handle_selection():
    appuifw.note(items[lb.current()][0] + u" has been selected.", 'info')

#Create an instance of Listbox and set it as the application's body
lb = appuifw.Listbox(items, handle_selection)
appuifw.app.body = lb

app_lock.wait()
