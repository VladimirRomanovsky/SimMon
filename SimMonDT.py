#! /bin/env python
'''
'''
from ctypes import *

from time import localtime,strftime

from Event import *

from BegSpill import *
from EndSpill import *

from Stat import *
from LE76 import *
from LE78 import *
from QDC import *
from TDC import *
from Matrix import *
#from WideHead import *
#from Hodos import *
#from HodoMISS import *
from Drift import *
#from PIM import *
#from Hodoscopes import *
from BC import *
#from BPC import *
from DT78 import *
from SG import *
from GDA import *
from GAMS import *
from BGD import *
from PC import *

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

filename = "SimMonTRACK.root"
#filename = strftime("SimMon_%d-%b-%Y_%H:%M:%S.root", localtime())
filename = "SimMon.root"

f = TFile(filename,"RECREATE")

methlist = []

methlist.append(Stat(f))

#methlist.append(DecodeQDC(0))
#ethlist.append(DecodeQDC(1))
#methlist.append(DecodeQDC(2))
#methlist.append(DecodeQDC(3))

#methlist.append(DecodeTDC())

methlist.append(DecodeLE78(10))
methlist.append(DecodeLE78(11))
methlist.append(DecodeLE78(12))
methlist.append(DecodeLE78(13))

#methlist.append(DecodeLE76())

#methlist.append(ViewLE78(f,10))
#methlist.append(ViewLE78(f,11))
#methlist.append(ViewLE78(f,12))
#methlist.append(ViewLE78(f,13))

#methlist.append(ViewBPC(f))

#methlist.append(ViewHodos(f))

#methlist.append(ViewQDC(f,0))
#methlist.append(ViewQDC(f,1))
#methlist.append(ViewQDC(f,2))
#methlist.append(ViewQDC(f,3))

methlist.append(ViewDT78(f))
methlist.append(ViewMatrix(f))
methlist.append(ViewPC(f))

#methlist.append(ViewHodoscopes(f))
#methlist.append(ViewDT(f))
#methlist.append(ViewSG(f))
#methlist.append(ViewGDA(f))
#methlist.append(ViewGAMS(f))
#methlist.append(ViewBGD(f))

#ESmethlist = []
#ESmethlist.append(DecodeQDC(2))
#ESmethlist.append(DecodeQDC(3))
#ESmethlist.append(ViewBGD_LED(f))

#BS = BegSpill(f)

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
