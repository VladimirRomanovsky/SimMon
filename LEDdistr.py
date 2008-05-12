#! /usr/bin/env python

from ROOT import *

f = TFile("SimMon.root")

gDirectory.cd("BGD_LED")
nx = 39
ny = 32

hmean = TH1F("LED","LED",100,0,4000)

for y in range(1,33):
  for x in range(1,39):
    name = "hLED_%02d_%02d"%(x,y)
    h = gDirectory.Get(name)
    if h.GetSum()>0:
      mean = h.GetMean()
      hmean.Fill(mean)

