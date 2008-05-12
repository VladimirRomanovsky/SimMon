
class LE84:
	" LE84 from OKA2007 DATA"
	
	def __init__(self,data):

		self.data = data
                self.moduls = {}

                if len(data)!=data[0]:
                        print "LE94:: Error in leng: %i %i "%(len(data),data[0])
                        return

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

		
		for im in mods.keys():

#			print "Modul: %i leng: %i"%(im,len(mods[im]))
			
			mod = mods[im]

			if len(mod)%2:
				continue
				
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
			if len(TDC1)==0 or len(TDC1)!=(TDC1[-1]&0xFF):
				continue
			if TDC1[0]>>28 != 2:
				continue
			if TDC1[-1]>>28 != 3:
				continue
			for h in TDC1[1:-1]:
				time = h&0x3FF
				chan = h>>18&0x1F
#				print chan,time
				dt1.append((chan,time))

			dt2 = []
			if len(TDC2)==0 or len(TDC2)!=(TDC2[-1]&0xFF):
				continue
			if TDC2[0]>>28 != 2:
				continue
			if TDC2[-1]>>28 != 3:
				continue
			for h in TDC2[1:-1]:
				time = h&0x3FF
				chan = h>>18&0x1F
#				print chan,time
				dt2.append((chan,time))

			self.moduls[im] = (dt1,dt2)
#		print self.moduls

class DecodeLE84:
        " Decode LE84 from OKA2007 DATA"


        def __init__(self,cr):
                self.cr = 9

        def Execute(self,event):

                try:
                        data = event.det[self.cr]         # Detector Number

                except  KeyError:
                        return

                event.reco["LE84"] = LE84(data)

from ROOT import TH1F,TH2F

class ViewLE84:

	class HLE84:
		def __init__(self,rootfile,number):
			dir = rootfile.mkdir("MOD_%02i"%number)
			dir.cd()

			dir1 = dir.mkdir("TDC1")
			dir2 = dir.mkdir("TDC2")

			self.hch = []
			self.hch.append(TH1F( 'hchanel1', 'hchanel1', 32, 0, 32 ))
			self.hch.append(TH1F( 'hchanel2', 'hchanel2', 32, 0, 32 ))
			self.htall = []
			self.htall.append(TH1F( 'h1time', 'h1time', 1024, 0, 1024 ))
			self.htall.append(TH1F( 'h2time', 'h2time', 1024, 0, 1024 ))
			
			
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
					self.htall[i].Fill(t)
					self.ht[i][ch].Fill(t)
			
	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("LE84")
		self.dir.cd()
		
		
		self.hmod = TH1F( 'hmod', 'hmod', 25, 0, 25 )
		self.hle84 = {}
		for i in range(1,12):
			self.hle84[i]=self.HLE84(self.dir,i)
		

	def Execute(self,event):
		
		try:
			le84 = event.reco["LE84"]
			
		except 	KeyError:
			return
			
		moduls = le84.moduls
		for im in moduls.keys():
			self.hmod.Fill(im)
			self.hle84[im].Fill(moduls[im])


class ViewCH2_LE84:

	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("CH2_LE84")
		self.dir.cd()
		
		
		self.htime0 = TH1F( 'htime0', 'htime0', 1000, 0, 1000 )
		self.hnch = TH1F( 'hnch', 'hnch', 10, 0, 10 )
		self.htimech = TH1F( 'htimech', 'htimech', 1000, 0, 1000 )
		self.hdtimech = TH1F( 'hdtimech', 'hdtimech', 1000, -300, 700 )
		self.hdtimech1 = TH1F( 'hdtimech1', 'hdtimech1', 1000, -300, 700 )
		self.hdtimech21 = TH1F( 'hdtimech21', 'hdtimech21', 1000, -300, 700 )
		self.hdtimech22 = TH1F( 'hdtimech22', 'hdtimech22', 1000, -300, 700 )
		self.hdtimech1_2 = TH1F( 'hdtimech1_2', 'hdtimech1_2', 100, -500, 500 )
		self.hdtimech2 = TH2F( 'hdtimech2', 'hdtimech2', 100, -300, 700, 100, -300, 700 )
		self.hdtimeg = TH1F( 'hdtimeg', 'hdtimeg', 100, 0, 500 )
		self.hdtimel = TH1F( 'hdtimel', 'hdtimel', 100, 0, 500 )
		
	def Execute(self,event):
		
		try:
			le84 = event.reco["LE84"]
			
		except 	KeyError:
			return
			
		moduls = le84.moduls
		
		try:
			mod = moduls[10]
			
		except 	KeyError:
			return

#		print mod


		tdc1 = mod[0]
		tdc2 = mod[1]

		n0 = 0
		for ch,time in tdc2:
			if ch == 30:
				n0 += 1
				t0 = time
		
		if n0 != 1:
			return
		
		
		self.htime0.Fill(t0)
		
		ch2 = []
		for ch,time in tdc1:
			if ch == 0:
				ch2.append(time)
		
		self.hnch.Fill(len(ch2))

		ch2.sort()

		ig = None
		for i,t in enumerate(ch2):
			self.htimech.Fill(t)
			self.hdtimech.Fill(t0-t)
			if 210<t0-t<230:
				ig = i

		if len(ch2)==1:
			self.hdtimech1.Fill(t0-ch2[0])
			
		if len(ch2)==2:
			self.hdtimech21.Fill(t0-ch2[0])
			self.hdtimech22.Fill(t0-ch2[1])
			self.hdtimech2.Fill(t0-ch2[0],t0-ch2[1])
			self.hdtimech1_2.Fill(ch2[1]-ch2[0])
			
			
		if ig:
			tg = ch2[ig]

			try:
				tn = ch2[ig+1]
				self.hdtimeg.Fill(tn - tg) 
			except:
				pass			
			
			if ig>0:
				tp = ch2[ig-1]
				self.hdtimel.Fill(tg - tp) 
			
