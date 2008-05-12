from ROOT import TH1F
from ROOT import TH2F

class LE84:
	" Decode LE84 from OKA2006 DATA"
	
	def __init__(self,data):

		self.data = data

class ViewDrift:

	class HLE84:
		def __init__(self,rootfile,number):
			dir = rootfile.mkdir("LE84_%02i"%number)
			dir.cd()

			dir1 = dir.mkdir("TDC1")
			dir2 = dir.mkdir("TDC2")

			self.hch = []
			self.hch.append(TH1F( 'hchanel1', 'hchanel1', 32, 0, 32 ))
			self.hch.append(TH1F( 'hchanel2', 'hchanel2', 32, 0, 32 ))
			
			
			self.ht = [[],[]]
			ht1 = self.ht[0]
			ht2 = self.ht[1]
			for i in range(32):
				dir1.cd()
				ht1.append(TH1F( 'h1time-%02d'%i, 'h1time-%02d'%i, 1024, 0, 1024 ))
				dir2.cd()
				ht2.append(TH1F( 'h2time-%02d'%i, 'h2time-%02d'%i, 1024, 0, 1024 ))
			
		def Fill(self,data):
			
			for i,tdc in enumerate(data):
				for ch,t in tdc:
					self.hch[i].Fill(ch)
					self.ht[i][ch].Fill(t)
			
			
	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("Drift")
		self.dir.cd()
		
		self.hle84 = {}
		for i in range(1,4):
			self.hle84[i]=self.HLE84(self.dir,i)


		self.h13 = TH2F( 'htime13', 'htime13', 1024, 0, 1024 , 1024, 0, 1024 )
		self.hd13 = TH1F( 'hdtime13', 'hdtime13', 2048, -1024, 1024 )

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
#		for im in mods.keys():
#		    print im,len(mods[im])
#		return
		
		le84 = {}		
		
		for im in mods.keys():

#			print "Modul: %i leng: %i"%(im,len(mods[im]))
			
			if im not in (1,2,3):
				print " LE84:: Error modul number: %i"%i
				continue 

			mod = mods[im]
		
			TDC1 = []
			TDC2 = []

			for i in range(len(mod)/2):

				w32 = mod[2*i+1]<<16|mod[2*i]

#				print "%08X"%w32
				w8 = w32>>24
				tdc = w8&0xF
				ident = w8>>4
#				print tdc,ident
			
				if tdc==2:
					TDC2.append(w32)
				if tdc==1:
					TDC1.append(w32)

			dt1 = []
			if len(TDC1)==(TDC1[-1]&0xFF):
				for h in TDC1[1:-1]:
					time = h&0x3FF
					chan = h>>18&0x1F
#					print chan,time
					dt1.append((chan,time))
				
			dt2 = []
			if len(TDC2)==(TDC2[-1]&0xFF):
				for h in TDC2[1:-1]:
					time = h&0x3FF
					chan = h>>18&0x1F
#					print chan,time
					dt2.append((chan,time))
				
			dt  = (dt1,dt2)
			self.hle84[im].Fill(dt)
			
			le84[im] = dt

		print le84

		t1 = le84[3][0][0][1]
		t3 = le84[3][0][1][1]
		self.h13.Fill(t1,t3)
		self.hd13.Fill(t1-t3)		
		
