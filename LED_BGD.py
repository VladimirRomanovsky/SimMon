#! /usr/bin/env python

from ROOT import *

f = TFile("SimMon_LED_GDA.root")

gDirectory.cd("GDA_LED")
gDirectory.cd("AMP")

nx = 11
ny = 11

hled = TH2F("LED","LED",11,1,12,11,1,12)

for y in range(ny):
	for x in range(nx):
		name = "hamp_%d_%d"%(x+1,y+1)
		h = gDirectory.Get(name)
		mean = h.GetMean()
		rms = h.GetRMS()
		hled.SetBinContent(x+1,y+1,mean)
		

hled.Draw()


dummy = raw_input('Press Enter key.')
