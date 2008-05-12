#! /usr/bin/env python

from ROOT import *

f = TFile("SimMon.root")

gDirectory.cd("BegSpill")

hmean = gDirectory.Get("BGD_PED_mean")
hsigma = gDirectory.Get("BGD_PED_sigma")

nx = 39
ny = 32
for y in range(ny+1,-1,-1):
  for x in range(nx+2):
    if (y == 0 or y == ny+1) and (x == 0 or x == nx+1):
      print '    ',
    else:
      if y == 0 or y == ny+1:
        print "%4d"%x,
      else:
        if x == 0 or x == nx+1:
          print "%4d"%y,
        else:
      	  mean = hmean.GetBinContent(x,y)
	  str = "%4d"%(int(mean))
          print str,
  print

print 
print 


for y in range(ny+1,-1,-1):
  for x in range(nx+2):
    if (y == 0 or y == ny+1) and (x == 0 or x == nx+1):
      print '    ',
    else:
      if y == 0 or y == ny+1:
        print "%4d"%x,
      else:
        if x == 0 or x == nx+1:
          print "%4d"%y,
        else:
      	  mean = hsigma.GetBinContent(x,y)
	  str = "%4d"%(int(mean))
          print str,
  print

