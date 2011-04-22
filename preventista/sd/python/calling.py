

import telephone, appuifw, e32

#Ask the user for the number to call
n=appuifw.query(u"Enter number", "number")
telephone.dial(str(n))

#Wait a while
e32.ao_sleep(5)

#Now hang up
telephone.hang_up()
