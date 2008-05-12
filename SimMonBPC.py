#! /bin/env python
'''
'''
from ctypes import *

from time import localtime,strftime

from Event import *

#from BegSpill import *
#from EndSpill import *

from Stat import *
from LE78 import *
from LE76 import *
from BPC import *
from PC import *
from Shift import *

from ROOT import TBrowser,TFile

import sys

if len(sys.argv) < 2:
	print '''
Usage: SimMon source
''' 
	sys.exit(0)
	
arg = sys.argv[1]


print '''
SimMon: Monitor which is simple as it is possible ...

If You don't like it, Don't use it!

To STOP it - press ^C

'''
	
size = 1024*8

lib = CDLL("datemon.so")


status = lib.date_init(arg)


print "Status %d"%status

buff_type = c_ushort*size

buff = buff_type()

#filename = strftime("SimMon_%d-%b-%Y_%H:%M:%S.root", localtime())
filename = "SimMon.root"

f = TFile(filename,"RECREATE")

methlist = []

methlist.append(Stat(f))

methlist.append(DecodeLE78(10))
methlist.append(DecodeLE78(11))
methlist.append(DecodeLE78(12))
methlist.append(DecodeLE78(13))

methlist.append(DecodeLE76())
methlist.append(ViewHodos(f))

#methlist.append(ViewLE78(f,10))
#methlist.append(ViewLE78(f,11))
#methlist.append(ViewLE78(f,12))
#methlist.append(ViewLE78(f,13))

methlist.append(ViewBPC(f))
methlist.append(ViewPC(f))
methlist.append(Select())
methlist.append(Shift(f))


b = TBrowser()

try:
	while True:
		status = lib.date_getevent(byref(buff),size*2)
		if status:
			print "Status %x"%(status&0x3FFFFFFF)
			break
	
		event = Event(buff)
#		print "Type of ev. %d"%event.Type()

#		if event.Type()==5:
#			event.Decode()
#			BS.Execute(event)

#		if event.Type()==6:
#			event.Decode()
#			for m in ESmethlist:
#				m.Execute(event)

		if event.Type()==7:
			event.Decode()
			for m in methlist:
				m.Execute(event)
			
except KeyboardInterrupt:
	print "KeyboardInterrupt"
else:
	print "End of File?"
	dummy = raw_input('Press Enter key.')

print '''
Saving Histograms,
Wait,  Please.
'''

f.Write()
