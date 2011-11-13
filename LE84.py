class LE84:
	" LE84 from OKA2007 DATA"
	
	def __init__(self,data):

		self.data = data
                self.moduls = {}

                if len(data)!=data[0]:
                        print "LE94:: Error in leng: %i %i "%(len(data),data[0])
                        return

		k = 2+6       #Skip 6 words
		num = 0	
		mods = {}
		

		while k < data[0]:
			num = data[k+1]
			mod = mods.setdefault(num,[])
			mod.append(data[k])
			k += 2
		
		for im in mods.keys():

			mod = mods[im]
                        #print "Modul: %2i leng: %i"%(im,len(mods[im]))
                        #print mod
				
			if len(mod)%2:
				continue
				
			TDC1 = []
			TDC2 = []
			dt = []

			for i in range(len(mod)/2):

				w32 = mod[2*i+1]<<16|mod[2*i]

                                #print "%08X"%w32
				w8 = w32>>24
				tdc = w8&0xF
				ident = w8>>4
                                #print im,tdc,ident
			        if ident == 4:
 					if tdc==2:
						TDC2.append(w32)
						time = w32&0x3FF
						chan = w32>>19&0x1F
						if im!=16:
							dt.append((32+chan,time))
					if tdc==1:
						TDC1.append(w32)
						time = w32&0x3FF
						chan = w32>>19&0x1F
						if im!=16:
							dt.append((chan,time))
			if im == 16:
				self.TDC1 = TDC1
				self.TDC2 = TDC2
			else:
				self.moduls[im] = dt
				
		#print self.moduls


class LE84_OLD:
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
		

		while k < data[0]:
			num = data[k+1]
			mod = mods.setdefault(num,[])
			mod.append(data[k])
			k += 2
		
		for im in mods.keys():

			mod = mods[im]
                        #print "Modul: %2i leng: %i"%(im,len(mods[im]))
                        #print mod
				
			if len(mod)%2:
				continue
				
			TDC1 = []
			TDC2 = []

			for i in range(len(mod)/2):

				w32 = mod[2*i+1]<<16|mod[2*i]

                                print "%08X"%w32
				w8 = w32>>24
				tdc = w8&0xF
				ident = w8>>4
                                print tdc,ident
			
				if tdc==2:
					TDC2.append(w32)
				if tdc==1:
					TDC1.append(w32)
                        print im,len(TDC1),len(TDC2)

			dt = []

                        #print "TDC1",TDC1[-1]&0xFF
			if len(TDC1)==0 or len(TDC1)!=(TDC1[-1]&0xFF):
				continue
			if TDC1[0]>>28 != 2:
				continue
			if TDC1[-1]>>28 != 3:
				continue
			for h in TDC1[1:-1]:
				time = h&0x3FF
				chan = h>>19&0x1F
				print im,"%08X"%h,chan,time
				if im!=16:
					dt.append((chan,time))
			
                        #print "TDC2",TDC2[-1]&0xFF
			if len(TDC2)==0 or len(TDC2)!=(TDC2[-1]&0xFF):
				continue
			if TDC2[0]>>28 != 2:
				continue
			if TDC2[-1]>>28 != 3:
				continue
			for h in TDC2[1:-1]:
				time = h&0x3FF
				chan = h>>19&0x1F
				print chan,time
				if im!=16:
					dt.append((32+chan,time))

			self.moduls[im] = dt
			if im == 16:
				self.TDC1 = TDC1
				self.TDC2 = TDC2
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

			self.hch = TH1F( 'hchanel', 'hchanel', 64, 0, 64 )
			self.ht = TH1F( 'htime', 'htime', 1024, 0, 1024 )
			self.hl = TH1F( 'hl', 'hl', 64, 0, 64 )
			self.hcht = TH2F( 'hcht', 'hcht', 64, 0, 64, 1024, 0, 1024 )
			

		def Fill(self,data):
			
			self.hl.Fill(len(data))
			for ch,t in data:
				self.hch.Fill(ch)
				self.ht.Fill(t)
				self.hcht.Fill(ch,t)
			
	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("LE84")
		self.dir.cd()
		
		self.ht01ht02 = TH2F( 'ht01t02', 'ht01t02', 100, 600, 700, 100, 600, 700 )
#		self.ht01ht03 = TH2F( 'ht01t03', 'ht01t03', 100, 600, 700, 100, 600, 700 )
#		self.ht02ht03 = TH2F( 'ht02t03', 'ht02t03', 100, 600, 700, 100, 600, 700 )

		
		self.hmod = TH1F( 'hmod', 'hmod', 25, 0, 25 )
		self.hle84 = {}
		for i in range(1,20):
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

		try:
			hits1=moduls[ 8]
			hits2=moduls[15]
#			hits3=moduls[13]
			
		except 	(KeyError,IndexError),x:
#			print x
			return
			
		t1 = None
		for e,t in hits1:
			if e == 63:
				t1 = t
				break
		t2 = None
		for e,t in hits2:
			if e == 63:
				t2 = t
				break
#		t3 = None
#		for e,t in hits3:
#			if e == 63:
#				t3 = t
#				break
		
		if t1 and t2:
			self.ht01ht02.Fill(t1,t2)
#		if t1 and t3:
#			self.ht01ht03.Fill(t1,t3)
#		if t2 and t3:
#			self.ht02ht03.Fill(t2,t3)


class MiscTDC:

	class hch:
		def __init__(self,rootfile,name):
			
			self.dir = rootfile.mkdir(name)
			self.dir.cd()
			self.ht = TH1F( 'time', 'time', 1000, 0, 1000 )
			self.hmul = TH1F( 'mul', 'mul', 10, 0, 10 )
			self.ht2 = TH2F( 't2', 't2', 1000, 0, 1000, 1000, 0, 1000)
			self.hdt = TH1F( 'time', 'time', 1000, -500, 500 )
			
			self.ht_tr = []
			for i in range(8):
				self.ht_tr.append(TH1F( 'time_%i'%i, 'time_%i'%i, 1000, 0, 1000 ))
				
		def Fill(self,hits,event):
		
			self.hmul.Fill(len(hits))	
			for t in hits:
				self.ht.Fill(t)
				for t2 in hits:
					self.ht2.Fill(t,t2)
					self.hdt.Fill(t2-t)

			try:
				sc = event.reco["Scalers"]
			
			except 	KeyError:
				return
			
			for t in hits:
				for i in range(8):
			
					if sc[2][i*2]:
						self.ht_tr[i].Fill(t)
					
			

	class hchch:
		def __init__(self,rootfile,name):
			
			self.dir = rootfile.mkdir(name)
			self.dir.cd()
			self.hm2 = TH2F( 'm2', 'm2', 10, 0, 10, 10, 0, 10)
			self.ht2 = TH2F( 't2', 't2', 1000, 0, 1000, 1000, 0, 1000)
			self.hdt = TH1F( 'dt', 'dt', 1000, -500, 500)
			self.ht2_1 = TH2F( 't2_1', 't2_1', 1000, 0, 1000, 1000, 0, 1000)
			self.hdt_1 = TH1F( 'dt_1', 'dt_1', 1000, -500, 500)

		def Fill(self,hits1,hits2):
		
			self.hm2.Fill(len(hits1),len(hits2))	
			for t1 in hits1:
				for t2 in hits2:
					self.ht2.Fill(t1,t2)
					self.hdt.Fill(t1-t2)
			if len(hits1) == 1 and 	len(hits2)==1:
				self.ht2_1.Fill(hits1[0],hits2[0])				
				self.hdt_1.Fill(hits1[0]-hits2[0])				

	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("MiscTDC")
		self.dir.cd()
		
		self.hs = []
		for i in range(64):
			name = "h%02d"%i
			self.hs.append(TH1F( name, name, 1000, 0, 1000 ))
		
		self.hch1 = self.hch(self.dir,"C1")
		self.hch2 = self.hch(self.dir,"C2")
#		self.hchh = self.hch(self.dir,"CH")
#		self.hmtrx = self.hch(self.dir,"Matrix")
#		self.hsgams = self.hch(self.dir,"SumGams")

		self.hch1ch2 = self.hchch(self.dir,"C1C2")
#		self.hch1chh = self.hchch(self.dir,"C1CH")
#		self.hch2chh = self.hchch(self.dir,"C2CH")

	def Execute(self,event):
		
		try:
			le84 = event.reco["LE84"]
			mod = le84.moduls[15]
		except 	(KeyError,IndexError),x:
#			print x
			return
		t63 = []
		for ch,t in mod:
			if ch == 63:
				t63.append(t)
		if len(t63)!=1:
			print "Error in 15  time"
			return
		t0 = t63[0]

		ch1 = []
		ch2 = []
#		chh = []
#		matrix = []
#		sgams = []

		for ch,t in mod:
			if ch<63:
				tc = t-t0+800
				self.hs[ch].Fill(tc)
				if ch==0:
					ch1.append(tc)
				if ch==2:
					ch2.append(tc)
#				if ch==2:
#					chh.append(tc)
#				if ch==3:
#					matrix.append(tc)
#				if ch==4:
#					sgams.append(tc)

		self.hch1.Fill(ch1,event)
		self.hch2.Fill(ch2,event)
#		self.hchh.Fill(chh,event)
#		self.hmtrx.Fill(matrix,event)
#		self.hsgams.Fill(sgams,event)
		
		self.hch1ch2.Fill(ch1,ch2)
#		self.hch1chh.Fill(ch1,chh)
#		self.hch2chh.Fill(ch2,chh)
		

class TDC100:

	class HCHAN:
		def __init__(self,rootfile,number):
			self.dir = rootfile.mkdir("chanel_%02i"%number)
			self.dir.cd()			

			self.hlstart = TH1F( 'lstart', 'lstart', 100, 0, 100)
			self.hlstop = TH1F( 'lstop', 'lstop', 100, 0, 100)
			self.hlstartlstop = TH2F( 'll', 'll', 20, 0, 20, 20, 0, 20)
			self.hstartstop = TH2F( 'tt', 'tt', 4096, 0, 4096,  4096, 0, 4096)
			self.hdt = TH1F( 'dt', 'dt', 2000, -1000, 1000)

		def Fill(self,data):
			
			start = data[0]
			stop = data[1]
			self.hlstart.Fill(len(start))
			self.hlstop.Fill(len(stop))
			self.hlstartlstop.Fill(len(start),len(stop))
			for t1 in start:
				for t2 in stop:
					self.hstartstop.Fill(t1,t2)
					self.hdt.Fill(t2-t1)

	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("TDC100")
		self.dir.cd()

		self.hch = TH1F( 'hchanel', 'hchanel', 64, 0, 64 )
		self.ht = TH1F( 'htime', 'htime', 8192, 0, 8192 )
		self.hl = TH1F( 'hl', 'hl', 64, 0, 64 )
		self.hcht = TH2F( 'hcht', 'hcht', 64, 0, 64, 8192, 0, 8192 )
		self.hchtm = TH2F( 'hchtm', 'hchtm', 64, 0, 64, 8192, 0, 8192 )
		
		self.hls1 = TH1F( 'hlS1', 'hlS1', 16, 0, 16 )
		self.hls2 = TH1F( 'hlS2', 'hlS2', 16, 0, 16 )
		self.hls3 = TH1F( 'hlS3', 'hlS3', 16, 0, 16 )
		self.hs1 = TH1F( 'htimeS1', 'htimeS1', 8192, 0, 8192 )
		self.hs2 = TH1F( 'htimeS2', 'htimeS2', 8192, 0, 8192 )
		self.hs3 = TH1F( 'htimeS3', 'htimeS3', 8192, 0, 8192 )
		self.hs1s2 = TH1F( 'htimeS1S2', 'htimeS1S2', 2000, -1000, 1000 )
		self.hs1s3 = TH1F( 'htimeS1S3', 'htimeS1S3', 2000, 0, 2000 )
		self.hs2s3 = TH1F( 'htimeS2S3', 'htimeS2S3', 2000, 0, 2000 )
		
				
	def Execute(self,event):
		
		try:
			le84 = event.reco["LE84"]
			TDC1 = le84.TDC1
			TDC2 = le84.TDC2
#			print "TDC1", TDC1
#			print "TDC2", TDC2
		except 	(KeyError,IndexError,AttributeError),x:
#			print x
			return

		dt = []
		for w32 in TDC1:
			time = w32&0x1FFF
			chan = w32>>19&0x1F
			dt.append((chan,time))
		for w32 in TDC2:
			time = w32&0x1FFF
			chan = w32>>19&0x1F
			dt.append((32+chan,time))

#		print dt
		
		self.hl.Fill(len(dt))
		t0 = None
		for ch,t in dt:
			self.hch.Fill(ch)
			self.ht.Fill(t)
			self.hcht.Fill(ch,t)
			if ch == 63:
				t0 = t
		 
		if not t0:
			return
		
		dtm = []
		s1 = []
		s2 = []
		s3 = []
		for ch,t in dt:
			if ch != 63:
				tm = t - t0 + 700
				self.hchtm.Fill(ch,tm)
				dtm.append((ch, tm))
				if ch == 9:
					s3.append(tm)
				if ch == 8:
					s1.append(tm)
				if ch == 7:
					s2.append(tm)
				
#		print dtm, s1,s2,s3
		
		self.hls1.Fill(len(s1))
		self.hls2.Fill(len(s2))
		self.hls3.Fill(len(s3))
				
		if len(s1) == 1:
			self.hs1.Fill(s1[0])
		if len(s2) == 1:
			self.hs2.Fill(s2[0])
		if len(s3) == 1:
			self.hs3.Fill(s3[0])
			
		if len(s1) == 1 and len(s2) == 1:
			self.hs1s2.Fill(s1[0]-s2[0])
		if len(s1) == 1 and len(s3) == 1:
			self.hs1s3.Fill(s1[0]-s3[0])
		if len(s2) == 1 and len(s3) == 1:
			self.hs2s3.Fill(s2[0]-s3[0])
		
class TDC100_old:

	class HCHAN:
		def __init__(self,rootfile,number):
			self.dir = rootfile.mkdir("chanel_%02i"%number)
			self.dir.cd()			

			self.hlstart = TH1F( 'lstart', 'lstart', 100, 0, 100)
			self.hlstop = TH1F( 'lstop', 'lstop', 100, 0, 100)
			self.hlstartlstop = TH2F( 'll', 'll', 20, 0, 20, 20, 0, 20)
			self.hstartstop = TH2F( 'tt', 'tt', 4096, 0, 4096,  4096, 0, 4096)
			self.hdt = TH1F( 'dt', 'dt', 2000, -1000, 1000)

		def Fill(self,data):
			
			start = data[0]
			stop = data[1]
			self.hlstart.Fill(len(start))
			self.hlstop.Fill(len(stop))
			self.hlstartlstop.Fill(len(start),len(stop))
			for t1 in start:
				for t2 in stop:
					self.hstartstop.Fill(t1,t2)
					self.hdt.Fill(t2-t1)

	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("TDC100")
		self.dir.cd()

		self.hdt = TH1F( 'hdt', 'hdt', 200, -1000, 1000)
		self.htt = TH2F( 'htt', 'htt', 4098, 0, 4098, 4098, 0, 4098 )
		self.hdt0t2 = TH1F( 'hdt0t2', 'hdt0t2', 2000, -1000, 1000)
		self.ht0t2 = TH2F( 'ht0t2', 'ht0t2', 4098, 0, 4098, 4098, 0, 4098 )

		self.startdir = self.dir.mkdir("Start")
		self.startdir.cd()

		self.hchStart = TH1F( 'hchanel', 'hchanel', 64, 0, 64 )
		self.htStart = TH1F( 'htime', 'htime', 4098, 0, 4098 )
		self.hlStart = TH1F( 'hl', 'hl', 64, 0, 64 )
		self.hchtStart = TH2F( 'hcht', 'hcht', 64, 0, 64, 4096, 0, 4096 )
		

		self.stopdir = self.dir.mkdir("Stop")
		self.stopdir.cd()

		self.hchStop = TH1F( 'hchanel', 'hchanel', 64, 0, 64 )
		self.htStop = TH1F( 'htime', 'htime', 4098, 0, 4098 )
		self.hlStop = TH1F( 'hl', 'hl', 64, 0, 64 )
		self.hchtStop = TH2F( 'hcht', 'hcht', 64, 0, 64, 4096, 0, 4096 )
		
		self.hchan = []
			
		for i in range(16):
			self.hchan.append(self.HCHAN(self.dir,i))

		
	def Execute(self,event):
		
		try:
			le84 = event.reco["LE84"]
			TDC1 = le84.TDC1
			TDC2 = le84.TDC2
#			print TDC1
#			print TDC2
		except 	(KeyError,IndexError,AttributeError),x:
#			print x
			return
		start = []
		stop = []
		chanels = {}
		for i in range(16):
			chanels[i]=([],[])
			
		if len(TDC1)>0 and len(TDC1)==(TDC1[-1]&0xFF) and TDC1[0]>>28 == 2 and TDC1[-1]>>28 == 3:
			for h in TDC1[1:-1]:
				front = h>>28
				time = h&0x1FFF
				chan = h>>19&0x1F
#				print "%08X"%h,chan,time
				if front == 4:
					start.append((chan,time)) 
					chanels[chan][0].append(time)
				if front == 5:
					stop.append((chan,time)) 
					chanels[chan][1].append(time)
					
		if len(TDC2)>0 and len(TDC2)==(TDC2[-1]&0xFF) and TDC2[0]>>28 == 2 and TDC2[-1]>>28 == 3:
			for h in TDC2[1:-1]:
				front = h>>28
				time = h&0x1FFF
				chan = h>>19&0x1F
#				print "%08X"%h,chan,time
				if front == 4:
					start.append((chan+32,time))
				if front == 5:
					stop.append((chan+32,time)) 

		self.hlStart.Fill(len(start))
		for ch,t in start:
			self.hchStart.Fill(ch)
			self.htStart.Fill(t)
			self.hchtStart.Fill(ch,t)

		self.hlStop.Fill(len(stop))
		for ch,t in stop:
			self.hchStop.Fill(ch)
			self.htStop.Fill(t)
			self.hchtStop.Fill(ch,t)

		for ch1,t1 in start:
			for ch2,t2 in stop:
				if ch1 == ch2:
					self.hdt.Fill(t2-t1)
					self.htt.Fill(t1,t2)

		for i in range(16):
			self.hchan[i].Fill(chanels[i])
			
		for t1 in chanels[0][0]:
			for t2 in chanels[2][0]:
				self.hdt0t2.Fill(t1-t2)
				self.ht0t2.Fill(t1,t2)		

class StrPC:

	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("StrPC")
		self.dir.cd()
		
		self.hx1 = TH2F( "hx1", "hx1", 256, 0, 256, 640, 0, 640 )
		self.hy1 = TH2F( "hy1", "hy1", 256, 0, 256, 640, 0, 640 )
		self.hx2 = TH2F( "hx2", "hx2", 256, 0, 256, 640, 0, 640 )
		self.hy2 = TH2F( "hy2", "hy2", 256, 0, 256, 640, 0, 640 )
		
	def Execute(self,event):
		
		try:
			le84 = event.reco["LE84"]
			mod = le84.moduls[13]
			pcx = event.reco["PCX2"]
			pcy = event.reco["PCY2"]
		except 	(KeyError,IndexError),x:
#			print x
			return
			

		t0 = mod.get(63,[])
		if len(t0)!=1:
			print "Error in 13 reper time"
			return
		time0 = t0[0]

		dtx = {}
		dty = {}
		for imod,mod in le84.moduls.items():
			for ch,times in mod.items():
				ok = False
				for t in times:
					if 300<t<500:
						ok = True
				if ok:
					if imod in [1,2,3,4]:
						c = ch+(imod-1)*64
						for t,e in pcx.hits:
							self.hx1.Fill(c,e)
						for t,e in pcy.hits:
							self.hy1.Fill(c,e)
					if imod in [7,8,9,10]:
						c = ch+(imod-7)*64
						for t,e in pcx.hits:
							self.hx2.Fill(c,e)
						for t,e in pcy.hits:
							self.hy2.Fill(c,e)
