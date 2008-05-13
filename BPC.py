		   
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


decodeBPC3X = [decode1[i]+128 for i in range(64)] + [decode1[i]+64 for i in range(64)] + list(decode1)
time3BPC3X = 64*[(55,67,80)] + 64*[(55,67,80)] + 64*[(60,70,80)]
badBPC3X = []
class BPC3X(BPC):
	def __init__(self,event):
		BPC.__init__(self,event,12,12,15,decodeBPC3X,time3BPC3X,badBPC3X)

		
decodeBPC4X = list(decode1) + [decode1[i]+64 for i in range(64)]  + [decode1[i]+128 for i in range(64)] 
time3BPC4X = 192*[(55,65,70)]
badBPC4X = [85,127]
class BPC4X(BPC):
	def __init__(self,event):
		BPC.__init__(self,event,12,15,18,decodeBPC4X,time3BPC4X,badBPC4X)


decodeBPC1Y =  [decode1[i]+128 for i in range(64)] + [decode1[i]+64 for i in range(64)] + list(decode1)
time3BPC1Y = 64*[(65,72,85)] + 64*[(60,75,85)] + 64*[(60,70,80)]
badBPC1Y = [146,152,178]
class BPC1Y(BPC):
	def __init__(self,event):
		BPC.__init__(self,event,10,18,21,decodeBPC1Y,time3BPC1Y,badBPC1Y) 


decodeBPC2Y = [decode4[i]+128 for i in range(64)] + [decode4[i]+64 for i in range(64)] + list(decode4)
time3BPC2Y = 64*[(50,65,75)] + 64*[(55,65,75)] + 64*[(55,67,80)]
badBPC2Y = []
for i,k in enumerate(decodeBPC2Y):
    if 31<k<64:
        m,l = divmod(k,2)
	decodeBPC2Y[i] = m*2+(1-l)
    if 95<k<128:
        m,l = divmod(k,2)
	decodeBPC2Y[i] = m*2+(1-l)
    if 160<k:
        m,l = divmod(k,2)
	decodeBPC2Y[i] = m*2+(1-l)
class BPC2Y(BPC):
	def __init__(self,event):
		BPC.__init__(self,event,10,21,24,decodeBPC2Y,time3BPC2Y,badBPC2Y)

decodeBPC3Y =  [decode3[i]+128 for i in range(64)] + [decode3[i]+64 for i in range(64)] + list(decode3)
time3BPC3Y = 64*[(60,70,80)] + 64*[(60,70,80)] + 64*[(57,67,80)]
badBPC3Y = []

class BPC3Y(BPC):
	def __init__(self,event):
		BPC.__init__(self,event,12,18,21,decodeBPC3Y,time3BPC3Y,badBPC3Y) 

decodeBPC4Y = [decode4[i]+128 for i in range(64)] + [decode4[i]+64 for i in range(64)] + list(decode4)
time3BPC4Y = 64*[(55,65,75)] + 64*[(55,67,77)] + 64*[(55,67,80)]
badBPC4Y = [18]
for i,k in enumerate(decodeBPC4Y):
    if 31<k<64:
        m,l = divmod(k,2)
	decodeBPC4Y[i] = m*2+(1-l)
    if 95<k<128:
        m,l = divmod(k,2)
	decodeBPC4Y[i] = m*2+(1-l)
    if 160<k:
        m,l = divmod(k,2)
	decodeBPC4Y[i] = m*2+(1-l)	
class BPC4Y(BPC):
	def __init__(self,event):
		BPC.__init__(self,event,12,21,24,decodeBPC4Y,time3BPC4Y,badBPC4Y)

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
			self.hhh = TH2F( 'hh %s'%name, 'hh %s'%name, 192, 0, 192, 192, 0, 192 )
			self.hdd = TH2F( 'dd %s'%name, 'dd %s'%name, 32, -16, 16, 192, 0, 192 )

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
			for h1 in pc.dhits:
				for h2 in pc.dhits:
					if not h1 == h2:
					        self.hhh.Fill(h1[1],h2[1])
					        self.hdd.Fill(h1[1]-h2[1],h1[1])
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
		
		self.dir = rootfile.mkdir(name)
		self.dir.cd()
			
		self.hprofile = TH2F( 'profile %s'%name, 'profile %s'%name, 192, 0, 192, 192, 0, 192 )

	    def Fill(self,pc1,pc2):
		for t1,e1 in pc1.hits:
		    for t2,e2 in pc2.hits:
			self.hprofile.Fill(e1,e2)

	class HBPCTest:
	    def __init__(self,rootfile,name):
		
		self.dir = rootfile.mkdir("BPCTest"+name)
		self.dir.cd()
		
		self.h32 = []
		for i in range(6):
		    self.h32.append(TH2F( 'h32 %d'%i, 'h32 %d'%i, 4, 0, 4, 4, 0, 4 ))

	    def Fill(self,pc):
	    
		for h1 in pc.hits:
		    for h2 in pc.hits:
		        if not h1 == h2:
			    i1,k1 = divmod(h1[1],32)
			    i2,k2 = divmod(h2[1],32)
		            if i1 == i2 and 50<h1[0]<90 and 50<h2[0]<90:
			        l1,m1 = divmod(k1,4)
			        l2,m2 = divmod(k2,4)
			        if l1 == l2:
			            self.h32[i1].Fill(m1,m2)
					
	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("BPC")
		self.dir.cd()

		self.hbpc3x = self.HBPC(self.dir, "BPC3X")
		self.hbpc4x = self.HBPC(self.dir, "BPC4X")
		self.hbpc1y = self.HBPC(self.dir, "BPC1Y")
		self.hbpc2y = self.HBPC(self.dir, "BPC2Y")
		self.hbpc3y = self.HBPC(self.dir, "BPC3Y")
		self.hbpc4y = self.HBPC(self.dir, "BPC4Y")

		self.hbpc3x4x = self.HBPC2(self.dir, "BPC3X4X")

		self.hbpc1y2y = self.HBPC2(self.dir, "BPC1Y2Y")
		self.hbpc1y3y = self.HBPC2(self.dir, "BPC1Y3Y")
		self.hbpc1y4y = self.HBPC2(self.dir, "BPC1Y4Y")
		self.hbpc2y3y = self.HBPC2(self.dir, "BPC2Y3Y")
		self.hbpc2y4y = self.HBPC2(self.dir, "BPC2Y4Y")
		self.hbpc3y4y = self.HBPC2(self.dir, "BPC3Y4Y")

		self.hbpctest1y = self.HBPCTest(self.dir, "1Y")
		self.hbpctest2y = self.HBPCTest(self.dir, "2Y")
		self.hbpctest3y = self.HBPCTest(self.dir, "3Y")
		self.hbpctest4y = self.HBPCTest(self.dir, "4Y")
		self.hbpctest3x = self.HBPCTest(self.dir, "3X")
		self.hbpctest4x = self.HBPCTest(self.dir, "4X")

	def Execute(self,event):
				
		bpc3x = BPC3X(event)
		bpc4x = BPC4X(event)
		bpc1y = BPC1Y(event)
		bpc2y = BPC2Y(event)
		bpc3y = BPC3Y(event)
		bpc4y = BPC4Y(event)

		event.reco["BPC3X"] = bpc3x
		event.reco["BPC4X"] = bpc4x
		event.reco["BPC1Y"] = bpc1y
		event.reco["BPC2Y"] = bpc2y
		event.reco["BPC3Y"] = bpc3y
		event.reco["BPC4Y"] = bpc4y

		self.hbpc3x.Fill(bpc3x)
		self.hbpc4x.Fill(bpc4x)
		self.hbpc1y.Fill(bpc1y)
		self.hbpc2y.Fill(bpc2y)
		self.hbpc3y.Fill(bpc3y)
		self.hbpc4y.Fill(bpc4y)
		
		self.hbpc3x4x.Fill(bpc3x,bpc4x)

		self.hbpc1y2y.Fill(bpc1y,bpc2y)
		self.hbpc1y3y.Fill(bpc1y,bpc3y)
		self.hbpc1y4y.Fill(bpc1y,bpc4y)
		self.hbpc2y3y.Fill(bpc2y,bpc3y)
		self.hbpc2y4y.Fill(bpc2y,bpc4y)
		self.hbpc3y4y.Fill(bpc3y,bpc4y)
		
		self.hbpctest1y.Fill(bpc1y)
		self.hbpctest2y.Fill(bpc2y)
		self.hbpctest3y.Fill(bpc3y)
		self.hbpctest4y.Fill(bpc4y)
		self.hbpctest3x.Fill(bpc3x)
		self.hbpctest4x.Fill(bpc4x)
