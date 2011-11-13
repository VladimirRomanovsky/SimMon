		   
decode1 = (63,31,61,29,59,27,57,25,55,23,53,21,51,19,49,17,
           47,15,45,13,43,11,41, 9,39, 7,37, 5,35, 3,33, 1,
	   62,30,60,28,58,26,56,24,54,22,52,20,50,18,48,16,
	   46,14,44,12,42,10,40, 8,38, 6,36, 4,34, 2,32, 0)

decode2 = (33, 1,35, 3,37, 5,39, 7,41, 9,43,11,45,13,47,15,
           49,17,51,19,53,21,55,23,57,25,59,28,61,29,63,31,
	   62,30,60,28,58,26,56,24,54,22,52,20,50,18,48,16,
	   46,14,44,12,42,10,40, 8,38, 6,36, 4,34, 2,32, 0)
		   
decode3 = (48,17,50,19,52,21,54,23,56,25,58,27,60,29,62,31,
           32, 1,34, 3,36, 5,38, 7,40, 9,42,11,44,13,46,15,
	   49,16,51,18,53,20,55,22,57,24,59,26,61,28,63,30,
	   33, 0,35, 2,37, 4,39, 6,41, 8,43,10,45,12,47,14)

decode4 = (49,16,51,18,53,20,55,22,57,24,59,26,61,28,63,30,
           33, 0,35, 2,37, 4,39, 6,41, 8,43,10,45,12,47,14,
	   48,17,50,19,52,21,54,23,56,25,58,27,60,29,62,31,
	   32, 1,34, 3,36, 5,38, 7,40, 9,42,11,44,13,46,15)

decode5 = (62,30,60,28,58,26,56,24,54,22,52,20,50,18,48,16,
	   46,14,44,12,42,10,40, 8,38, 6,36, 4,34, 2,32, 0,
	   63,31,61,29,59,27,57,25,55,23,53,21,51,19,49,17,
           47,15,45,13,43,11,41, 9,39, 7,37, 5,35, 3,33, 1)

class BPC:

	def __init__(self,event,cr,rfirst,rlast,decode,time3,bad):
		
		self.event = event
		self.hits = []
		self.ghits = []
		self.bhits = []
		self.dhits = []
		self.cls = []
	
		try:
			le78 = event.reco["LE78-%2d"%cr]
		
		except KeyError:
			return

		for im in range(rfirst,rlast):
			try:
				m = le78.moduls[im]
			except KeyError:
				continue
		
			for t,e in m:
				e = e + (im-rfirst)*64
				e = decode[e]
				if e in bad:
					continue
				hit = (t,e)
				self.hits.append(hit)
				time = time3[e]
				if time[0]<t<time[1]:
					self.bhits.append(hit)
				if time[1]<t<time[2]:
					self.ghits.append(hit)
				if time[0]<t<time[2]:
					self.dhits.append(hit)
					

		if len(self.hits) > 1:
			self.hits.sort(lambda x,y: cmp(x[1], y[1]))
			
		cl = []
		for h in self.hits:
			if len(cl) == 0:
				cl.append(h)
			else:
				if h[1]-cl[-1][1]<=1:
					cl.append(h)
				else:
					self.cls.append(cl)
					cl = []
		if len(cl) >0:
			self.cls.append(cl)

decodeBPC2X = [decode1[i]+128 for i in range(64)] + [decode1[i]+64 for i in range(64)]  + list(decode1)
time3BPC2X = 64*[(67,78,87)] + 64*[(70,83,93)] + 64*[(70,83,95)]
badBPC2X = []

class BPC2X(BPC):
	def __init__(self,event):
		BPC.__init__(self,event,14,15,18,decodeBPC2X,time3BPC2X,badBPC2X) #2X
					
decodeBPC3X = [decode1[i]+128 for i in range(64)]  + [decode2[i]+64 for i in range(64)]  + list(decode1)
time3BPC3X = 64*[(65,78,87)] + 64*[(65,78,87)] + 64*[(65,78,87)]
badBPC3X = [95,183]

class BPC3X(BPC):
	def __init__(self,event):
		BPC.__init__(self,event,12,12,15,decodeBPC3X,time3BPC3X,badBPC3X) #3X
		
decodeBPC4X = [decode1[i]+128 for i in range(64)] + [decode5[i]+64 for i in range(64)]  + list(decode1) 
time3BPC4X = 64*[(70,77,87)] + 64*[(60,74,85)]+ 64*[(60,74,85)]
badBPC4X = []

class BPC4X(BPC):
	def __init__(self,event):
		BPC.__init__(self,event,12,15,18,decodeBPC4X,time3BPC4X,badBPC4X) #4X

decodeBPC1Y = [decode1[i]+128 for i in range(64)] + [decode1[i]+64 for i in range(64)] + list(decode1)
time3BPC1Y = 64*[(70,85,100)] + 64*[(70,85,100)] + 64*[(60,75,95)]
badBPC1Y = []

class BPC1Y(BPC):
	def __init__(self,event):
		BPC.__init__(self,event,10,18,21,decodeBPC1Y,time3BPC1Y,badBPC1Y) #1Y

decodeBPC2Y = [decode3[i]+128 for i in range(64)]  + [decode3[i]+64 for i in range(64)]  + list(decode3)
time3BPC2Y = 64*[(60,75,90)] + 64*[(65,75,90)] + 64*[(65,75,90)]
badBPC2Y = [147]

class BPC2Y(BPC):
	def __init__(self,event):
		BPC.__init__(self,event,10,21,24,decodeBPC2Y,time3BPC2Y,badBPC2Y) # 2Y

decodeBPC3Y = [decode3[i]+128 for i in range(64)]  + [decode3[i]+64 for i in range(64)]  + list(decode3)
time3BPC3Y = 64*[(70,82,95)] + 64*[(70,80,95)] + 64*[(60,80,90)]
badBPC3Y = []

class BPC3Y(BPC):
	def __init__(self,event):
		BPC.__init__(self,event,12,18,21,decodeBPC3Y,time3BPC3Y,badBPC3Y) # 3Y

decodeBPC4Y = [decode4[i]+128 for i in range(64)]  + [decode4[i]+64 for i in range(64)]  + list(decode4)
time3BPC4Y = 64*[(63,70,90)] + 64*[(67,80,95)] + 64*[(70,82,95)]
badBPC4Y = []

class BPC4Y(BPC):
	def __init__(self,event):
		BPC.__init__(self,event,12,21,24,decodeBPC4Y,time3BPC4Y,badBPC4Y) # 4Y

from ROOT import TH1F,TH2F,TH3F

class ViewBPC:



	class HBPC:
		def __init__(self,rootfile,name):
		
			self.dir = rootfile.mkdir(name)
			self.dir.cd()
			
			self.hprofile = TH1F( 'profile %s'%name, 'profile %s'%name, 192, 0, 192 )
			self.htime = TH2F( 'time %s'%name, 'time %s'%name, 192, 0, 192, 128, 0, 128 )
			self.htimem = {}
			self.htimem[0] = TH1F( 'time0m %s'%name, 'time0m %s'%name, 256, 0, 256 )
			self.htimem[1] = TH1F( 'time1m %s'%name, 'time0m %s'%name, 256, 0, 256 )
			self.htimem[2] = TH1F( 'time2m %s'%name, 'time0m %s'%name, 256, 0, 256 )

			self.hgprofile = TH1F( 'good profile %s'%name, 'good profile %s'%name, 192, 0, 192 )
			self.hbprofile = TH1F( 'bad profile %s'%name, 'bad profile %s'%name, 192, 0, 192 )
			self.hdprofile = TH1F( 'double profile %s'%name, 'double profile %s'%name, 192, 0, 192 )

			self.hgmul = TH1F( 'good mult %s'%name, 'good mult %s'%name, 16, 0, 16 )
			self.hbmul = TH1F( 'bad mult %s'%name, 'bad mult %s'%name, 16, 0, 16 )
			self.hdmul = TH1F( 'double mult %s'%name, 'double mult %s'%name, 16, 0, 16 )
			self.hde = TH1F( 'dhit %s'%name, 'dhit %s'%name, 16, 0, 16 )
			self.hde2 = TH2F( 'dhit2 %s'%name, 'dhit2 %s'%name, 192, 0, 192, 16, 0, 16 )

			cldir = self.dir.mkdir("CL")
			cldir.cd()

			self.hclmul = TH1F( 'cluster mult %s'%name, 'cluster mult %s'%name, 16, 0, 16 )
			self.hcllen = TH1F( 'cluster leng %s'%name, 'cluster leng %s'%name, 16, 0, 16 )

			self.hgtimem = {}
			self.hgtimem[0] = TH1F( 'gtime0m %s'%name, 'gtime0m %s'%name, 256, 0, 256 )
			self.hgtimem[1] = TH1F( 'gtime1m %s'%name, 'gtime0m %s'%name, 256, 0, 256 )
			self.hgtimem[2] = TH1F( 'gtime2m %s'%name, 'gtime0m %s'%name, 256, 0, 256 )

			self.hbtimem = {}
			self.hbtimem[0] = TH1F( 'btime0m %s'%name, 'btime0m %s'%name, 256, 0, 256 )
			self.hbtimem[1] = TH1F( 'btime1m %s'%name, 'btime0m %s'%name, 256, 0, 256 )
			self.hbtimem[2] = TH1F( 'btime2m %s'%name, 'btime0m %s'%name, 256, 0, 256 )

		def Fill(self,pc):
			for t,e in pc.hits:
				self.hprofile.Fill(e)
				self.htime.Fill(e,t)
				self.htimem[e/64].Fill(t)
			for t1,e1 in pc.hits:
				for t2,e2 in pc.hits:
					if not (t1,e1)==(t2,e2):
						self.hde.Fill(abs(e1-e2))
						self.hde2.Fill(e1,abs(e1-e2))
						self.hde2.Fill(e2,abs(e1-e2))
			self.hbmul.Fill(len(pc.bhits))
			for t,e in pc.bhits:
				self.hbprofile.Fill(e)
				
			self.hgmul.Fill(len(pc.ghits))
			for t,e in pc.ghits:
				self.hgprofile.Fill(e)

			self.hdmul.Fill(len(pc.dhits))
			for t,e in pc.dhits:
				self.hdprofile.Fill(e)
					
			self.hclmul.Fill(len(pc.cls))
			for cl in pc.cls:
				self.hcllen.Fill(len(cl))
				if len(cl)==3:
					t,e = cl[1]
					self.hgtimem[e/64].Fill(t)
					t,e = cl[0]
					self.hbtimem[e/64].Fill(t)
					t,e = cl[2]
					self.hbtimem[e/64].Fill(t)
	
					
			try:
				hodos = pc.event.reco["HODOS"]

			except  KeyError:
				return
					
			try:
				h1x = hodos["H1X"]
			except KeyError:
				pass
			else:
				for h in h1x.hits:
					for t,e in pc.dhits:
						self.hhodx.Fill(h,e)
			
			try:
				h1y = hodos["H1Y"]
			except KeyError:
				pass
			else:
				for h in h1y.hits:
					for t,e in pc.dhits:
						self.hhody.Fill(h,e)
	class HBPC2:
		def __init__(self,rootfile,name):
		
			rootfile.cd()
			self.h2 = TH2F( 'profile %s'%name, 'profile %s'%name, 192, 0, 192 , 192, 0, 192 )

		def Fill(self,pc1,pc2):
			for t1,e1 in pc1.hits:
				for t2,e2 in pc2.hits:
					self.h2.Fill(e1,e2)

	class HBPC3:
		def __init__(self,rootfile,name):
		
			rootfile.cd()
			self.h3 = TH3F( 'profile %s'%name, 'profile %s'%name, 192, 0, 192, 192, 0, 192, 192, 0, 192 )

		def Fill(self,pc1,pc2,pc3):
			for t1,e1 in pc1.hits:
				for t2,e2 in pc2.hits:
					for t3,e3 in pc3.hits:
						self.h3.Fill(e1,e2,e3)
			
	class HBPCHOD:
		def __init__(self,rootfile,name,hsize):
		
			rootfile.cd()
			self.h2 = TH2F( 'profile %s'%name, 'profile %s'%name, 192, 0, 192 , hsize, 0, hsize )

		def Fill(self,pc,hod):
			for t1,e1 in pc.hits:
				for e2 in hod.hits:
					self.h2.Fill(e1,e2)

					
	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("BPC")
		self.dir.cd()

		self.hpc2x = self.HBPC(self.dir, "BPC2X")
		self.hpc3x = self.HBPC(self.dir, "BPC3X")
		self.hpc4x = self.HBPC(self.dir, "BPC4X")
		self.hpc1y = self.HBPC(self.dir, "BPC1Y")
		self.hpc2y = self.HBPC(self.dir, "BPC2Y")
		self.hpc3y = self.HBPC(self.dir, "BPC3Y")
		self.hpc4y = self.HBPC(self.dir, "BPC4Y")

		self.hpc2x3x = self.HBPC2(self.dir, "BPC2-2X3X")
		self.hpc2x4x = self.HBPC2(self.dir, "BPC2-2X4X")
		self.hpc3x4x = self.HBPC2(self.dir, "BPC2-3X4X")

		self.hpc1y2y = self.HBPC2(self.dir, "BPC2-1Y2Y")
		self.hpc1y3y = self.HBPC2(self.dir, "BPC2-1Y3Y")
		self.hpc1y4y = self.HBPC2(self.dir, "BPC2-1Y4Y")
		self.hpc2y3y = self.HBPC2(self.dir, "BPC2-2Y3Y")
		self.hpc2y4y = self.HBPC2(self.dir, "BPC2-2Y4Y")
		self.hpc3y4y = self.HBPC2(self.dir, "BPC2-3Y4Y")

		self.hpc2y3y4y = self.HBPC3(self.dir, "BPC3-2Y3Y4Y")
		self.hpc2x3x4x = self.HBPC3(self.dir, "BPC3-2X3X4X")

		self.hpc2xhod = self.HBPCHOD(self.dir, "BPCHOD2X", 48)
		self.hpc3xhod = self.HBPCHOD(self.dir, "BPCHOD3X", 48)
		self.hpc4xhod = self.HBPCHOD(self.dir, "BPCHOD4X", 48)
		self.hpc1yhod = self.HBPCHOD(self.dir, "BPCHOD1Y", 48)
		self.hpc2yhod = self.HBPCHOD(self.dir, "BPCHOD2Y", 48)
		self.hpc3yhod = self.HBPCHOD(self.dir, "BPCHOD3Y", 48)
		self.hpc4yhod = self.HBPCHOD(self.dir, "BPCHOD4Y", 48)

	def Execute(self,event):

#		bpc1x = BPC1X(event)
		bpc2x = BPC2X(event)
		bpc3x = BPC3X(event)
		bpc4x = BPC4X(event)
		bpc1y = BPC1Y(event)
		bpc2y = BPC2Y(event)
		bpc3y = BPC3Y(event)
		bpc4y = BPC4Y(event)

#		event.reco["BPC1Y"] = bpc1y
		event.reco["BPC2X"] = bpc2x
		event.reco["BPC3X"] = bpc3x
		event.reco["BPC4X"] = bpc4x

		event.reco["BPC1Y"] = bpc1y
		event.reco["BPC2Y"] = bpc2y
		event.reco["BPC3Y"] = bpc3y
		event.reco["BPC4Y"] = bpc4y

#		self.hpc1x.Fill(bpc1x)
		self.hpc2x.Fill(bpc2x)
		self.hpc3x.Fill(bpc3x)
		self.hpc4x.Fill(bpc4x)
		self.hpc1y.Fill(bpc1y)
		self.hpc2y.Fill(bpc2y)
		self.hpc3y.Fill(bpc3y)
		self.hpc4y.Fill(bpc4y)
		
		self.hpc2x3x.Fill(bpc2x,bpc3x)
		self.hpc2x4x.Fill(bpc2x,bpc4x)
		self.hpc3x4x.Fill(bpc3x,bpc4x)

		self.hpc1y2y.Fill(bpc1y,bpc2y)
		self.hpc1y3y.Fill(bpc1y,bpc3y)
		self.hpc1y4y.Fill(bpc1y,bpc4y)
		self.hpc2y3y.Fill(bpc2y,bpc3y)
		self.hpc2y4y.Fill(bpc2y,bpc4y)
		self.hpc3y4y.Fill(bpc3y,bpc4y)

		self.hpc2y3y4y.Fill(bpc2y,bpc3y,bpc4y)
		self.hpc2x3x4x.Fill(bpc2x,bpc3x,bpc4x)

                try:
                	hodos = event.reco["HODOS"]

                except  KeyError:
                	return

                try:
                	h2x = hodos["H2X"]
                except KeyError:
                	pass
                else:
                        self.hpc2xhod.Fill(bpc2x,h2x)
                        self.hpc3xhod.Fill(bpc3x,h2x)
                        self.hpc4xhod.Fill(bpc4x,h2x)

                try:
                	h2y = hodos["H2Y"]
                except KeyError:
                	pass
                else:
                        self.hpc1yhod.Fill(bpc1y,h2y)
                        self.hpc2yhod.Fill(bpc2y,h2y)
                        self.hpc3yhod.Fill(bpc3y,h2y)
                        self.hpc4yhod.Fill(bpc4y,h2y)
