import e32
import appuifw
import btconsole

def getpass(prompt='Password?'):
    if btconsole.inside_btconsole() or not e32.is_ui_thread():
        return raw_input(prompt)
    else:
        if isinstance(prompt,str):
            prompt=prompt.decode('utf8')
        reply=appuifw.query(prompt,'code')
        if reply is None:
            raise KeyboardInterrupt
        return reply

# This is a bit clumsy, but since the Symbian OS has no concept
# of a username, it's the best we can do.
def getuser(prompt='Username?'):
    if btconsole.inside_btconsole() or not e32.is_ui_thread():
        return raw_input(prompt)
    else:
        if isinstance(prompt,str):
            prompt=prompt.decode('utf8')
        reply=appuifw.query(prompt,'text')
        if reply is None:
            raise KeyboardInterrupt
        return reply

