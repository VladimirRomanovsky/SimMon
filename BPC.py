
decode1 = ( 0,32, 2,34, 4,36, 6,38, 8,40,10,42,12,44,14,46,
           16,48,18,50,20,52,22,54,24,56,26,58,28,60,30,62,
	    1,33, 3,35, 5,37, 7,39, 9,41,11,43,13,45,15,47,
	   17,49,19,51,21,53,23,55,25,57,27,59,29,61,31,63)
	   
decode3 = (15,46,13,44,11,42, 9,40, 7,38, 5,36, 3,34, 1,32,
           31,62,29,60,27,58,25,56,23,54,21,52,19,50,17,48,
	   16,47,14,45,12,43,10,41, 8,39, 6,37, 4,35, 2,33,
	   32,63,30,61,28,59,26,57,24,55,22,53,20,51,18,49)
	   
decode4 = (14,47,12,45,10,43, 8,41, 6,39, 4,37, 2,35, 0,33,
           30,63,28,61,26,59,24,57,22,55,20,53,18,51,16,49,
	   17,46,15,44,13,42,11,40, 9,38, 7,36, 5,34, 3,32,
	   33,62,31,60,29,58,27,56,25,54,23,52,21,50,19,48)

#dg = (3,0,1,2,1,2,3,0)
#d1 = (0,0,0,0,1,1,1,1)
#decode5 = []
#for i in range(32):
#	l,m = divmod(i,8)
#	k = dg[l]*16+2*m+d1[l]
#	l,m = divmod(k,16)
#	k = l*16+15-m 
#	decode5.append(k)	
#	l,m = divmod(i+32,8)
#	k = dg[l]*16+2*m+d1[l]
#	l,m = divmod(k,16)
#	k = l*16+15-m 
#	decode5.append(k)

decode5 = (63,30,61,28,59,26,57,24,55,22,53,20,51,18,49,16,
           15,46,13,44,11,42, 9,40, 7,38, 5,36, 3,34, 1,32,
		   31,62,29,60,27,58,25,56,23,54,21,52,19,50,17,48,
		   47,14,45,12,43,10,41, 8,39, 6,37, 4,35, 2,33, 0)
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
			
			
decodeBPC1 = [decode1[i]+128 for i in range(64)] + [decode1[i]+64 for i in range(64)]  + [decode1[i]+0 for i in range(64)] 
time3BPC1 =  64*[(40,73,83)] + 64*[(40,53,63)] + 64*[(40,53,63)] 
badBPC1 = [0,1,2,4,7,15,184,190,191]

class BPC1(BPC):
	def __init__(self,event):
		BPC.__init__(self,event,12,12,15,decodeBPC1,time3BPC1,badBPC1)
		
decodeBPC2 = [decode1[i]+128 for i in range(64)] + [decode1[i]+64 for i in range(64)]  + [decode1[i]+0 for i in range(64)] 
time3BPC2 = 192*[(10,50,80)]
badBPC2 = [146,150,158,160]

class BPC2(BPC):
	def __init__(self,event):
		BPC.__init__(self,event,12,15,18,decodeBPC2,time3BPC2,badBPC2)

decodeBPC3 = [decode3[i]+128 for i in range(64)] + [decode3[i]+64 for i in range(64)]  + [decode3[i]+0 for i in range(64)] 
time3BPC3 =  64*[(40,73,83)] + 64*[(40,50,60)] + 64*[(45,55,65)] 
badBPC3 = [1,45,146,167,190,191]

class BPC3(BPC):
	def __init__(self,event):
		BPC.__init__(self,event,12,18,21,decodeBPC3,time3BPC3,badBPC3)

decodeBPC4 = [decode4[i]+128 for i in range(64)] + [decode4[i]+64 for i in range(64)]  + [decode4[i]+0 for i in range(64)] 
time3BPC4 = 64*[(37,47,57)] + 64*[(50,67,80)] + 64*[(10,50,80)]
badBPC4 = [137]

class BPC4(BPC):
	def __init__(self,event):
		BPC.__init__(self,event,12,21,24,decodeBPC4,time3BPC4,badBPC4)

decodeBPC5 = [decode5[i]+128 for i in range(64)] + [decode5[i]+64 for i in range(64)]  + [decode5[i]+0 for i in range(64)] 

#	Akimenko !!!

for i in range(192):
	k = decodeBPC5[i]
	if 112<=k<176:
		decodeBPC5[i] = k + 16
	if 176<k:
		decodeBPC5[i] = k - 64

time3BPC5 = 64*[(60,80,100)] + 64*[(65,70,85)] + 64*[(60,70,90)]
badBPC5 = []

class BPC5(BPC):
	def __init__(self,event):
		BPC.__init__(self,event,10,21,24,decodeBPC5,time3BPC5,badBPC5)

from ROOT import TH1F,TH2F,TH3F

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

			self.hhodx1 = TH2F( 'hodx1 %s'%name, 'hodx1 %s'%name, 16, 0, 16, 192, 0, 192  )
			self.hhody1 = TH2F( 'hody1 %s'%name, 'hody1 %s'%name, 16, 0, 16, 192, 0, 192  )

			self.hhodx2 = TH2F( 'hodx2 %s'%name, 'hodx2 %s'%name, 48, 0, 48, 192, 0, 192  )
			self.hhody2 = TH2F( 'hody2 %s'%name, 'hody2 %s'%name, 48, 0, 48, 192, 0, 192  )
			
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
						self.hhodx1.Fill(h,e)
			
			try:
				h1y = hodos["H1Y"]
			except KeyError:
				pass
			else:
				for h in h1y.hits:
					for t,e in pc.dhits:
						self.hhody1.Fill(h,e)
			
			try:
				h2x = hodos["H2X"]
			except KeyError:
				pass
			else:
				for h in h2x.hits:
					for t,e in pc.dhits:
						self.hhodx2.Fill(h,e)
			
			try:
				h2y = hodos["H2Y"]
			except KeyError:
				pass
			else:
				for h in h2y.hits:
					for t,e in pc.dhits:
						self.hhody2.Fill(h,e)
			
					
	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("BPC")
		self.dir.cd()

		self.h2Y3Y = TH2F( '2Y3Y', '2Y3Y', 192, 0, 192, 192, 0, 192  )
		self.h2Y4Y = TH2F( '2Y4Y', '2Y4Y', 192, 0, 192, 192, 0, 192  )
		self.h3Y4Y = TH2F( '3Y4Y', '3Y4Y', 192, 0, 192, 192, 0, 192  )
#		self.h2Y3Y4Y = TH3F( '2Y3Y4Y', '2Y3Y4Y', 192, 0, 192, 192, 0, 192, 192, 0, 192 )
		
		self.hpc1 = self.HBPC(self.dir, "BPC3X")
		self.hpc2 = self.HBPC(self.dir, "BPC4X")
		self.hpc3 = self.HBPC(self.dir, "BPC3Y")
		self.hpc4 = self.HBPC(self.dir, "BPC4Y")
		self.hpc5 = self.HBPC(self.dir, "BPC2Y")

		
	def Execute(self,event):
				
		bpc1 = BPC1(event)
		bpc2 = BPC2(event)
		bpc3 = BPC3(event)
		bpc4 = BPC4(event)
		bpc5 = BPC5(event)
		
		self.hpc1.Fill(bpc1)
		self.hpc2.Fill(bpc2)
		self.hpc3.Fill(bpc3)
		self.hpc4.Fill(bpc4)
		self.hpc5.Fill(bpc5)
		
		for t1,e1 in bpc5.hits:
			for t2,e2 in bpc3.hits:
				self.h2Y3Y.Fill(e1,e2)
				
		for t1,e1 in bpc5.hits:
			for t2,e2 in bpc4.hits:
				self.h2Y4Y.Fill(e1,e2)
		
		for t1,e1 in bpc3.hits:
			for t2,e2 in bpc4.hits:
				self.h3Y4Y.Fill(e1,e2)

#		for t1,e1 in bpc5.hits:
#			for t2,e2 in bpc3.hits:
#				for t3,e3 in bpc4.hits:
#					self.h2Y3Y4Y.Fill(e1,e2,e3)
