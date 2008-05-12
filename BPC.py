		   
decode1 = (63,31,61,29,59,27,57,25,55,23,53,21,51,19,49,17,
           47,15,45,13,43,11,41, 9,39, 7,37, 5,35, 3,33, 1,
		   62,30,60,28,58,26,56,24,54,22,52,20,50,18,48,16,
		   46,14,44,12,42,10,40, 8,38, 6,36, 4,34, 2,32, 0)
		   
decode3 = (48,17,50,19,52,21,54,23,56,25,58,27,60,29,62,31,
           32, 1,34, 3,36, 5,38, 7,40, 9,42,11,44,13,46,15,
		   47,16,49,18,51,20,53,22,55,24,57,26,59,28,61,30,
		   31, 0,33, 2,35, 4,37, 6,39, 8,41,10,43,12,45,14)

decode4 = (49,16,51,18,53,20,55,22,57,24,59,26,61,28,63,30,
           33, 0,35, 2,37, 4,39, 6,41, 8,43,10,45,12,47,14,
		   46,17,48,19,50,21,52,23,54,25,56,27,58,29,60,31,
		   30, 1,32, 3,34, 5,36, 7,38, 9,40,11,42,13,44,15)

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
decodeBPC1 = list(decode1) + [decode1[i]+64 for i in range(64)]  + [decode1[i]+128 for i in range(64)] 
time3BPC1 = 64*[(40,53,63)] + 64*[(40,73,83)] + 64*[(40,53,63)]
badBPC1 = [15,184,190,191]

class BPC1(BPC):
	def __init__(self,event):
		BPC.__init__(self,event,12,12,15,decodeBPC1,time3BPC1,badBPC1) #3X
		
decodeBPC2 = list(decode1) + [decode1[i]+64 for i in range(64)]  + [decode1[i]+128 for i in range(64)] 
time3BPC2 = 192*[(10,50,80)]
badBPC2 = [146,150,158,160]

class BPC2(BPC):
	def __init__(self,event):
		BPC.__init__(self,event,12,15,18,decodeBPC2,time3BPC2,badBPC2) #4X

decodeBPC3 = list(decode3) + [decode3[i]+64 for i in range(64)]  + [decode3[i]+128 for i in range(64)] 
time3BPC3 = 64*[(55,65,75)] + 64*[(70,85,95)] + 64*[(50,60,70)]
badBPC3 = [1,45,167,190]

class BPC3(BPC):
	def __init__(self,event):
		BPC.__init__(self,event,12,18,21,decodeBPC3,time3BPC3,badBPC3) # 3Y

decodeBPC4 = list(decode4) + [decode4[i]+64 for i in range(64)]  + [decode4[i]+128 for i in range(64)] 
time3BPC4 = 64*[(65,75,90)] + 64*[(45,55,85)] + 64*[(70,80,95)]
badBPC4 = []

class BPC4(BPC):
	def __init__(self,event):
		BPC.__init__(self,event,12,21,24,decodeBPC4,time3BPC4,badBPC4) # 4Y

from ROOT import TH1F,TH2F

class ViewBPC:



	class HBPC:
		def __init__(self,rootfile,name):
		
			self.dir = rootfile.mkdir(name)
			self.dir.cd()
			
			self.hprofile = TH1F( 'profile %s'%name, 'profile %s'%name, 192, 0, 192 )
			self.htime = TH2F( 'time %s'%name, 'time %s'%name, 192, 0, 192, 128, 0, 128 )
			self.htimem = {}
			self.htimem[0] = TH1F( 'time0m %s'%name, 'time0m %s'%name, 128, 0, 128 )
			self.htimem[1] = TH1F( 'time1m %s'%name, 'time0m %s'%name, 128, 0, 128 )
			self.htimem[2] = TH1F( 'time2m %s'%name, 'time0m %s'%name, 128, 0, 128 )

			self.hgprofile = TH1F( 'good profile %s'%name, 'good profile %s'%name, 192, 0, 192 )
			self.hbprofile = TH1F( 'bad profile %s'%name, 'bad profile %s'%name, 192, 0, 192 )
			self.hdprofile = TH1F( 'double profile %s'%name, 'double profile %s'%name, 192, 0, 192 )

			self.hgmul = TH1F( 'good mult %s'%name, 'good mult %s'%name, 16, 0, 16 )
			self.hbmul = TH1F( 'bad mult %s'%name, 'bad mult %s'%name, 16, 0, 16 )
			self.hdmul = TH1F( 'double mult %s'%name, 'double mult %s'%name, 16, 0, 16 )


			cldir = self.dir.mkdir("CL")
			cldir.cd()

			self.hclmul = TH1F( 'cluster mult %s'%name, 'cluster mult %s'%name, 16, 0, 16 )
			self.hcllen = TH1F( 'cluster leng %s'%name, 'cluster leng %s'%name, 16, 0, 16 )

			self.hgtimem = {}
			self.hgtimem[0] = TH1F( 'gtime0m %s'%name, 'gtime0m %s'%name, 128, 0, 128 )
			self.hgtimem[1] = TH1F( 'gtime1m %s'%name, 'gtime0m %s'%name, 128, 0, 128 )
			self.hgtimem[2] = TH1F( 'gtime2m %s'%name, 'gtime0m %s'%name, 128, 0, 128 )

			self.hbtimem = {}
			self.hbtimem[0] = TH1F( 'btime0m %s'%name, 'btime0m %s'%name, 128, 0, 128 )
			self.hbtimem[1] = TH1F( 'btime1m %s'%name, 'btime0m %s'%name, 128, 0, 128 )
			self.hbtimem[2] = TH1F( 'btime2m %s'%name, 'btime0m %s'%name, 128, 0, 128 )

			hoddir = self.dir.mkdir("HOD")
			hoddir.cd()

			self.hhodx = TH2F( 'hodx %s'%name, 'hodx %s'%name, 16, 0, 16, 192, 0, 192  )
			self.hhody = TH2F( 'hody %s'%name, 'hody %s'%name, 16, 0, 16, 192, 0, 192  )
			
		def Fill(self,pc):
			for t,e in pc.hits:
				self.hprofile.Fill(e)
				self.htime.Fill(e,t)
				self.htimem[e/64].Fill(t)
				
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
			
					
	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("BPC")
		self.dir.cd()

		self.hpc1 = self.HBPC(self.dir, "BPC1X")
		self.hpc2 = self.HBPC(self.dir, "BPC2_")
		self.hpc3 = self.HBPC(self.dir, "BPC3Y")
		self.hpc4 = self.HBPC(self.dir, "BPC4Y")


	def Execute(self,event):
				
		bpc1 = BPC1(event)
		bpc2 = BPC2(event)
		bpc3 = BPC3(event)
		bpc4 = BPC4(event)
		
		self.hpc1.Fill(bpc1)
		self.hpc2.Fill(bpc2)
		self.hpc3.Fill(bpc3)
		self.hpc4.Fill(bpc4)
		
