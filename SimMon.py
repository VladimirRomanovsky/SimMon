#! /bin/env python
'''
'''

import sys
#sys.path.append("/home.local/daqop/users/roma/lib/python2.4/site-packages")

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
from WideHead import *
from Drift import *
from PIM import *
from BC import *
from DT78 import *
from SG import *
from GDA import *
from GAMS import *
from BGD import *

from ROOT import TBrowser,TFile

import sys

#print """
#	Don't use SimMon.py, PLEASE.
#	Use instead:
#			SimMonCALO
#			SimMonTRACK
#"""
#sys.exit(0)


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

#d = "/".join(__file__.split("/")[:-1])
#lib = CDLL(d+"/datemon.so")
#status = lib.date_init(arg)
#print "Status %d"%status

lib = CDLL("/date/monitoring/Linux/libmonitor.so")

status = lib.monitorDeclareMp("SimMon")
print "Status %d"%status
status = lib.monitorSetDataSource(arg)
print "Status %d"%status


buff_type = c_ushort*size

buff = buff_type()

#filename = strftime("SimMon_%d-%b-%Y_%H:%M:%S.root", localtime())
filename = "SimMon.root"

f = TFile(filename,"RECREATE")

methlist = []

methlist.append(Stat(f))

methlist.append(DecodeQDC(0))
methlist.append(DecodeQDC(1))
methlist.append(DecodeQDC(2))
methlist.append(DecodeQDC(3))
#methlist.append(DecodeTDC())

methlist.append(ViewQDC(f,2))

methlist.append(DecodeLE76())

#methlist.append(ViewLE78(f,10))
#methlist.append(ViewLE78(f,11))
#methlist.append(ViewLE78(f,12))
#methlist.append(ViewLE78(f,13))

#methlist.append(ViewDrift(f))

methlist.append(ViewHodos(f))

methlist.append(ViewDT78(f))

#methlist.append(ViewBC(f))
#methlist.append(ViewDT(f))
methlist.append(ViewSG(f))
methlist.append(ViewGDA(f))
methlist.append(ViewGAMS(f))
methlist.append(ViewBGD(f))

ESmethlist = []
ESmethlist.append(DecodeQDC(2))
ESmethlist.append(DecodeQDC(3))
#ESmethlist.append(ViewBGD_LED(f))

BS = BegSpill(f)

b = TBrowser()

skip_error = (0x400000,)

try:
	while True:
#		status = lib.date_getevent(byref(buff),size*2)
		status = lib.monitorGetEvent(byref(buff),size*2)
		if status:
			print "Status %x"%(status&0x3FFFFFFF)
                        if status&0x3FFFFFFF in skip_error:
                            continue
                        else:
                            break
	
		event = Event(buff)
#		print "Type of ev. %d"%event.Type()

		if event.Type()==5:
			event.Decode()
			BS.Execute(event)

		if event.Type()==6:
			event.Decode()
			for m in ESmethlist:
				m.Execute(event)

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
