
#
# View MBM
#
 
'''
1.00 2008-03-30 Initial release
'''
 
VERSION = "1.00"
 
import appuifw
import e32
 
def showicon(a_title, a_file, id_list, maskfunc=lambda x:x):
    ''' Create new Listbox with given parameters '''
    # a_title: change application title, show list name
    # a_file: get icons from this file, with full path
    # id_list: icon id numbers to show,  must be list
    # maskfunc: define icon mask number algorithm
    #     showicon(range(0,100,2), lambda x:x+1)
    #     icon number: 0, 2, 4, 6, 8, 10 etc.
    #     mask number: icon number + 1
 
    # http://snippets.dzone.com/posts/show/1482
    # You can define more complex mask algoriths
    #     if type(id_list) == int:
    #         id_list = [id_list] # one item
    #     if type(maskfunc) == dict:  # allow dict as a func
    #         func = lambda id: maskfunc.get(id,id)
    #     else:
    #         func = maskfunc
 
    # Get all icons from given file.mbm
    try:
        entries = []
        for id in id_list:
            # 2-row listbox item to show bigger icon
            row1 = u"Icon: %s" % id
            row2 = u"Mask: %s" % maskfunc(id)
            icon = appuifw.Icon(a_file, id, maskfunc(id))
            entries.append((row1, row2, icon))
 
        # Make the new listbox visible
        appuifw.app.title = a_title
        appuifw.app.body = appuifw.Listbox(entries)
    except:
        appuifw.note(u"Error!")
 
def menu_about():
    ''' Callback for menu item About '''
    appuifw.note(u'View MBM v' + VERSION + u'\n' +\
        u'jouni.miettunen.googlepages.com\n\u00a92009 Jouni Miettunen')
 
def cb_quit():
    ''' Cleanup before exit '''
    app_lock.signal()
 
# Initialize application UI
lb = appuifw.Listbox([u"Use Options menu...", u"...to see built-in icons."])
appuifw.app.body = lb
appuifw.app.exit_key_handler=cb_quit
 
# How to find MBM files and count how many picteres they contain:
# for %%a in (C:\Symbian\9.2\S60_3rd_FP1\Epoc32\release\winscw\udeb\z\resource\apps\*.mbm) do bmconv /v %%a
#
# Better readability if you do:
# scan_mbm.bat | grep containing > results.txt
 
# Hox: Error if you try to "see" more icons that the file contains
# SymbianError: [Errno -25] KErrEof
 
# Hox: Error if more that 30 items in appuifw.app.menu
# ValueError: too many menuitems
 
appuifw.app.menu = [
    (u"About (3)", lambda:showicon(u"About (3)", u"z:\\resource\\apps\\about.mbm", range(3))),
    (u"AknMemoryCardUI (8)", lambda:showicon(u"AknMemoryCardUI (8)", u"z:\\resource\\apps\\aknmemorycardui.mbm", range(8))),
    # S60 3.1 emulator ok, but error in N82
    #(u"Apn (4)", lambda:showicon(u"Apn (4)", u"z:\\resource\\apps\\apn.mbm", range(4))),
    (u"AspSyncUtil (2)", lambda:showicon(u"AspSyncUtil (2)", u"z:\\resource\\apps\\aspsyncutil.mbm", range(2))),
    # S60 3.1 emulator has 238 items, N82 only 233 !?!?!
    #(u"Avkon2 (238)", lambda:showicon(u"Avkon2 (238)", u"z:\\resource\\apps\\avkon2.mbm", range(238))),
    (u"Avkon2 (233)", lambda:showicon(u"Avkon2 (233)", u"z:\\resource\\apps\\avkon2.mbm", range(233))),
    (u"Blid (10)", lambda:showicon(u"Blid (10)", u"z:\\resource\\apps\\blid.mbm", range(10))),
    (u"Browser (42)", lambda:showicon(u"Browser (42)", u"z:\\resource\\apps\\browser.mbm", range(42))),
    (u"BrowserBitmaps (32)", lambda:showicon(u"BrowserBitmaps (32)", u"z:\\resource\\apps\\browserbitmaps.mbm", range(32))),
    (u"BubbleManager (20)", lambda:showicon(u"BubbleManager (20)", u"z:\\resource\\apps\\bubblemanager.mbm", range(20))),
    (u"CalcSoft (2)", lambda:showicon(u"CalcSoft (2)", u"z:\\resource\\apps\\calcsoft.mbm", range(2))),
    (u"CallStatus (8)", lambda:showicon(u"CallStatus (8)", u"z:\\resource\\apps\\callstatus.mbm", range(8))),
    (u"ConnMan (2)", lambda:showicon(u"ConnMan (2)", u"z:\\resource\\apps\\connman.mbm", range(2))),
    (u"DefaultAppIcon (6)", lambda:showicon(u"DefaultAppIcon (6)", u"z:\\resource\\apps\\default_app_icon.mbm", range(6))),
    (u"DisconnectDlgUi (4)", lambda:showicon(u"DisconnectDlgUi (4)", u"z:\\resource\\apps\\disconnectdlgui.mbm", range(4))),
    (u"DownloadMgrUiLib (2)", lambda:showicon(u"DownloadMgrUiLib (2)", u"z:\\resource\\apps\\downloadmgruilib.mbm", range(2))),
    (u"FotaServer (4)", lambda:showicon(u"FotaServer (4)", u"z:\\resource\\apps\\fotaserver.mbm", range(4))),
    (u"Launcher (2)", lambda:showicon(u"Launcher (2)", u"z:\\resource\\apps\\launcher.mbm", range(2))),
    (u"MidpErm (4)", lambda:showicon(u"MidpErm (4)", u"z:\\resource\\apps\\midperm.mbm", range(4))),
    (u"MsgUrlHandler (4)", lambda:showicon(u"MsgUrlHandler (4)", u"z:\\resource\\apps\\msgurlhandler.mbm", range(4))),
    (u"Muiu (2)", lambda:showicon(u"Muiu (2)", u"z:\\resource\\apps\\muiu.mbm", range(2))),
    (u"NsmldmSync (4)", lambda:showicon(u"NsmldmSync (4)", u"z:\\resource\\apps\\nsmldmsync.mbm", range(4))),
    (u"Phonebook (8)", lambda:showicon(u"Phonebook (8)", u"z:\\resource\\apps\\phonebook.mbm", range(8))),
    (u"ProvisioningCx (2)", lambda:showicon(u"ProvisioningCx (2)", u"z:\\resource\\apps\\provisioningcx.mbm", range(2))),
    (u"ScreenGrabber (2)", lambda:showicon(u"ScreenGrabber (2)", u"z:\\resource\\apps\\screengrabber.mbm", range(2))),
    (u"StartUp (12)", lambda:showicon(u"StartUp (12)", u"z:\\resource\\apps\\startup.mbm", range(12))),
    (u"TrustRoots (4)", lambda:showicon(u"TrustRoots (4)", u"z:\\resource\\apps\\trustroots.mbm", range(4))),
    (u"Vm (2)", lambda:showicon(u"Vm (2)", u"z:\\resource\\apps\\vm.mbm", range(2))),
    (u"WebKit (38)", lambda:showicon(u"WebKit (38)", u"z:\\resource\\apps\\webkit.mbm", range(38))),
    (u"-- About --", menu_about),
    (u"Exit", cb_quit)
]
 
# Wait for user to do anything
app_lock = e32.Ao_lock()
app_lock.wait()
