import inbox, e32, appuifw


#Define the exit function
app_lock=e32.Ao_lock()
def quit():
    app_lock.signal()
    appuifw.app.exit_key_handler=quit

#Define the function to be executed when a message is received
def cb(id):
    print "New message!"

i=inbox.Inbox()

#Now wait for the message:
i.bind(cb)

app_lock.wait()
