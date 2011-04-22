import appuifw

#You can store the information entered by the user in a variable

inf=appuifw.query(u"Enter a number", "number")
#asks for a number, in this case integer; for a fractional number use "float"

inf=appuifw.query(u"Enter a word", "text")
#asks for a text

inf=appuifw.query(u"Enter a password", "code")
#asks for a password, and shows the characters as "*" for protection

inf=appuifw.query(u"Enter a time", "time")
#asks for a time in hh:mm format

inf=appuifw.query(u"Would you like to play again?", "query")
#displays a question, the returned values being 1 if the user has selected "Yes" and 0 if the user has selected "No"

inf=appuifw.multi_query(u"Part1", u"Part2")
#asks for two fields of information
