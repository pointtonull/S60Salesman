import re
import mktimefix as time

MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

def safe_unicode(value):
    "http://aspyplayer.googlecode.com/svn/trunk/src/aspyplayer.py"
    if type(value) == type(unicode("unicode")):
        return value

    result = ""
    for enc in ['utf8', 'latin1']:
        try:
            result = value.decode(enc)
            break
        except:
            pass
			
    return unicode(result)

def decode_html(line):
    "http://mail.python.org/pipermail/python-list/2006-April/378536.html"
    pat = re.compile(r'&#(\d+);')
    def sub(mo):
        return unichr(int(mo.group(1)))
    return pat.sub(sub, safe_unicode(line))

def parse_iso8601(val):
    "Returns a tupple with (yyyy, mm, dd, hh, mm, ss). Argument is provided by xmlrpc DateTime.value"
    dt,tm= val.split('T')
    tm = tm.split(':')
    return (int(dt[:4]),int(dt[4:6]),int(dt[6:8]),int(tm[0]),int(tm[1]),int(tm[2]))

def utf8_to_unicode(s):
    if isinstance(s, unicode):
        return s
    else:
        return unicode(s,'utf-8',errors='ignore')

def unicode_to_utf8(s):
    return s.encode('utf-8')

def localtime_iso8601():
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())

def gm_to_localtime( tm ):
    diff = time.time() - time.mktime(time.gmtime())
    return time.localtime(time.mktime( tm ) + diff)
    
