#! /usr/bin/env python

from ROOT import *

f = TFile("SimMon.root")

gDirectory.cd("BGD_LED")
nx = 39
ny = 32

for y in range(ny+1,-1,-1):
  for x in range(nx+2):
    if y == 0 or y == ny+1:
      print "%4d"%x,
    else:
      if x == 0 or x == nx+1:
        print "%4d"%y,
      else:
        name = "hLED_%02d_%02d"%(x,y)
        h = gDirectory.Get(name)
	str = "    "
	if h.GetSum()>0:
#	  str = "%4.0f#%3.0f"%(h.GetMean(),h.GetRMS())
	  str = "%4.0f"%(h.GetMean())
        print str,
  print

