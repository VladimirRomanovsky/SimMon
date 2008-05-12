from ROOT import TH1F
from ROOT import TH2F

class LE84:
	" Decode LE84 from OKA2006 DATA"
	
	def __init__(self,data):

		self.data = data

class ViewDrift:

	def __init__(self,rootfile):

		dir = rootfile.mkdir("Drift")
		dir.cd()
		
		self.h1ch = TH1F( 'h1ch', 'h1ch',32, 0, 32 )
		self.h1time = TH1F( 'h1time', 'h1time', 1024, 0, 1024 )
		self.h2ch = TH1F( 'h2ch', 'h2ch',32, 0, 32 )
		self.h2time = TH1F( 'h2time', 'h2time', 1024, 0, 1024 )

		self.hdtime24 = TH1F( 'hdtime24', 'hdtime24', 1024, 0, 1024 )
		self.hdtime28 = TH1F( 'hdtime28', 'hdtime28', 1024, 0, 1024 )

		self.hddtime = TH1F( 'hddtime', 'hddtime', 1024, -1024, 1024 )
		
		dir1 = dir.mkdir("TDC1")
		dir2 = dir.mkdir("TDC2")

		self.h1l = []
		self.h2l = []
		for i in range(32):
			dir1.cd()
			self.h1l.append(TH1F( 'h1time-%02d'%i, 'h1time-%02d'%i, 1024, 0, 1024 ))
			dir2.cd()
			self.h2l.append(TH1F( 'h2time-%02d'%i, 'h2time-%02d'%i, 1024, 0, 1024 ))
		

	def Execute(self,event):
		
		try:
			data = event.det[9]
		except 	KeyError:
			return

#		print data
#		print data[0],len(data)
					
		k = 2
		num = 0	
		mods = {}
		mod = []

		while k < data[0]:
			if num != data[k+1]:
				if len(mod) != 0:
#					print num,mod
					mods[num] = mod
					mod = []
				num = data[k+1]	

			mod.append(data[k])
			k += 2
#		print mods

		try:
		    mod = mods[2]
		except 	KeyError:
			return
		
		TDC1 = []
		TDC2 = []
		for i in range(len(mod)/2):
			w32 = mod[2*i+1]<<16|mod[2*i]
#			print "%08X"%w32
			w8 = w32>>24
			tdc = w8&0xF
			ident = w8>>4
#			print tdc,ident
			
			if tdc==2:
				TDC2.append(w32)
			if tdc==1:
				TDC1.append(w32)

		dt1 = []
		if len(TDC1)==(TDC1[-1]&0xFF):
			for h in TDC1[1:-1]:
				time = h&0x3FF
				chan = h>>18&0x1F
#				print chan,time
				self.h1ch.Fill(chan)
				self.h1time.Fill(time)
				self.h1l[chan].Fill(time)
				dt1.append((chan,time))
				
		dt2 = []
		if len(TDC2)==(TDC2[-1]&0xFF):
			for h in TDC2[1:-1]:
				time = h&0x3FF
				chan = h>>18&0x1F
#				print chan,time
				self.h2ch.Fill(chan)
				self.h2time.Fill(time)
				self.h2l[chan].Fill(time)
				dt2.append((chan,time))
				

		event.reco["DT"] = dt1

		t0_24 = None
		t0_28 = None
		for chan,time in dt1:
			if chan == 24:
				if t0_24:
					self.hdtime24.Fill(time-t0_24)
				else:
					t0_24 = time
			if chan == 28:
				if t0_28:
					self.hdtime28.Fill(time-t0_28)
				else:
					t0_28 = time
		if t0_28 and t0_24:
			self.hddtime.Fill(t0_28 - t0_24)
