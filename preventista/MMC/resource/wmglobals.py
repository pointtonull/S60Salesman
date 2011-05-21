# -*- coding: utf-8 -*-
import sys
import os
import e32

__all__ = [ "VERSION", "DEFDIR", "MIFFILE", "PERSIST", "TOUCH_ENABLED", "RESDIR" ]

# always 3 numbers with two digits each maximum, e.g. 3.44.2, 4.2.33 ...
VERSION = "0.9.5"

# looking for install dir and default paths/files
DEFDIR = u""
MIFFILE = u""
PERSIST = u""
RESDIR = u""
if e32.in_emulator():
    DEFDIR = os.path.join(os.path.dirname(sys.argv[0]),"wordmobi_tmp")
    if not os.path.exists(DEFDIR):
        os.makedirs(DEFDIR)
else:
    for d in e32.drive_list():
        appd = d + u"\\data\\python\\wordmobidir\\"
        if os.path.exists(appd + u"wordmobi.py"):
            DEFDIR = appd
            break
if DEFDIR:
    sys.path.append(DEFDIR)
    sys.path.append(os.path.join(DEFDIR,u"loc"))
    MIFFILE = os.path.join(DEFDIR,u"wordmobi.mif")
    PERSIST = os.path.join(DEFDIR,u"persist.bin")
    RESDIR = os.path.join(DEFDIR,u"res")
    
# checking touch UI
try:
    from appuifw import touch_enabled
    TOUCH_ENABLED = touch_enabled()
except:
    # python < 1.9.3 does not support touch ui
    TOUCH_ENABLED = False

# Use standard media gallery
MGFETCH = False

    
