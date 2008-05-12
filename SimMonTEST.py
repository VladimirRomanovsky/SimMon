#! /bin/env python
'''
'''
from ctypes import *

from time import localtime,strftime

from Event import *

from BegSpill import *
from EndSpill import *

from Gorin import *
from Stat import *
from LE78 import *
from QDC import *
from TDC import *
from WideHead import *
from Hodos import *
from HodoMISS import *
from Drift import *
from PIM import *
from Hodoscopes import *
from BC import *
from DT import *
from SG import *
from GDA import *
from GAMS import *
from BGD import *

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

filename = "SimMonCALO.root"
#filename = strftime("SimMon_%d-%b-%Y_%H:%M:%S.root", localtime())
filename = "SimMon.root"

f = TFile(filename,"RECREATE")

methlist = []

methlist.append(Stat(f))

b = TBrowser()

try:
	while True:
		status = lib.date_getevent(byref(buff),size*2)
		if status:
			print "Status %x"%(status&0x3FFFFFFF)
			break
	
		event = Event(buff)
#		print "Type of ev. %d"%event.Type()


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
