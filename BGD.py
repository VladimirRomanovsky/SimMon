from ROOT import TH1F,TH2F

from numpy import zeros

class BGD:
    
	def __init__(self):
	
		conf = file("/".join(__file__.split("/")[:-1])+"/config_bgd.dat")
		self.qdc2plain = zeros((4,10,96),int) 
		
		for string in conf:
			ss = string.split()
			c = int(ss[1])
			n = int(ss[2])
			a = int(ss[3])
			e = int(ss[6])
		
			self.qdc2plain[c,n,a] = e

		self.plain2xy = {}
		
		for x in range(1,40):
			for y in range(1,33):
				self.plain2xy[x+(32-y)*39] = (x,y)


	def QDC2BGD(self,c,n,a):

		e = self.qdc2plain[c,n,a]
		return self.plain2xy[e]

gbgd = BGD()


class ViewBGD:
	bad = ((5,21),(13,1),(19,1),(34,14),(8,24),(13,25))
	def __init__(self,rootfile):

		
		self.dir = rootfile.mkdir("BGD")
		self.dir.cd()
		
		self.hamp = TH1F( 'hamp', 'hamp',1000, 0, 1000 )

		self.hxy = TH2F( 'hxy', 'hxy',39, 1, 40, 32, 1, 33 )
		self.hxya = TH2F( 'hxya', 'hxya',39, 1, 40, 32, 1, 33 )
		self.hxy_th = TH2F( 'hxy_th', 'hxy_th',39, 1, 40, 32, 1, 33 )
		self.hxya_th = TH2F( 'hxya_th', 'hxya_th',39, 1, 40, 32, 1, 33 )
		
		self.hsum = TH1F( 'hsum', 'hsum',1000, 0, 4000 )
		self.hnum = TH1F( 'hnum', 'hnum',100, 0, 100 )
		self.hsn = TH2F( 'hsn', 'hsn',100, 0, 4000, 100, 0, 100 )

		cl_dir = self.dir.mkdir("Cluster")
		cl_dir.cd()

		self.hncl = TH1F( 'hncl', 'hncl',20, 0, 20 )

		self.hclnum = TH1F( 'hclnum', 'hclnum',10, 0, 10 )
		self.hclsum = TH1F( 'hclsum', 'hclsum',1000, 0, 4000 )
		self.hclxy = TH2F( 'hclxy', 'hclxy',39, 1, 40, 32, 1, 33 )
		self.hclxye = TH2F( 'hclxye', 'hclxye',39, 1, 40, 32, 1, 33 )
		
		self.hclsumg = TH1F( 'hclsumg', 'hclsumg',1000, 0, 4000 )
		self.hclxyg = TH2F( 'hclxyg', 'hclxyg',39, 1, 40, 32, 1, 33 )
		self.hclxyge = TH2F( 'hclxyge', 'hclxyge',39, 1, 40, 32, 1, 33 )

		self.hclsum1 = TH1F( 'hclsum1', 'hclsum1',1000, 0, 4000 )
		self.hclxy1 = TH2F( 'hclxy1', 'hclxy1',39, 1, 40, 32, 1, 33 )
		self.hclxy1e = TH2F( 'hclxy1e', 'hclxy1e',39, 1, 40, 32, 1, 33 )

		mu_dir = self.dir.mkdir("Mu")
		mu_dir.cd()

		self.hclnumMu = TH1F( 'hclnum', 'hclnum',10, 0, 10 )
		self.hclsumMu = TH1F( 'hclsum', 'hclsum',1000, 0, 4000 )
		self.hclsumMuG = TH1F( 'hclsumG', 'hclsumG',1000, 0, 4000 )
		self.hclxyMu = TH2F( 'hclxy', 'hclxy',39, 1, 40, 32, 1, 33 )
		self.hclxyeMu = TH2F( 'hclxye', 'hclxye',39, 1, 40, 32, 1, 33 )
		self.hclxyMu1 = TH2F( 'hclxy1', 'hclxy',39, 1, 40, 32, 1, 33 )
		self.hclxyMu2 = TH2F( 'hclxy2', 'hclxy',39, 1, 40, 32, 1, 33 )
		self.hclxyMu3 = TH2F( 'hclxy3', 'hclxy',39, 1, 40, 32, 1, 33 )
		self.hclxyMu4 = TH2F( 'hclxy4', 'hclxy',39, 1, 40, 32, 1, 33 )

		baddir = self.dir.mkdir("BAD")
		baddir.cd()
		
		self.hbad = {}
		for b in self.bad:
		 	self.hbad[b] = TH1F( 'hbad%02i%02i'%b, 'hbad%02i%02i'%b,1000, 0, 1000 )


	def Execute(self,event):

		try:
			qdc = (0,0,event.reco["QDC-2"],event.reco["QDC-3"])
		except KeyError:
			return
		try:
			m8 = qdc[2].moduls[8]
			Mu = []
			for a,e in m8:
				if e == 71 and a>20:
					Mu.append(0)
				if e == 70 and a>20:
					Mu.append(1)
				if e == 69 and a>20:
					Mu.append(2)
				if e == 68 and a>20:
					Mu.append(3)
			
		except KeyError:
			Mu = []
		
		bgd = zeros((41,34),int) 
		bgdl = [] 
		
		for c in range(2,4):
			for m,h in qdc[c].moduls.iteritems():
				for a,e in h:
					try:
						x,y = gbgd.QDC2BGD(c,m,e)
					except:
						continue
					if (x,y) in self.bad:
						self.hbad[(x,y)].Fill(a+3)
						continue
					bgdl.append((x,y,a+3))
					bgd[x,y]=a+3

		sum = 0
		
		for x,y,a in bgdl:
			self.hamp.Fill(a)
			self.hxy.Fill(x,y)
			self.hxya.Fill(x,y,a)
			if a>10:
				self.hxy_th.Fill(x,y)
				self.hxya_th.Fill(x,y,a)
			sum += a
		self.hsum.Fill(sum)
		self.hnum.Fill(len(bgdl))
		self.hsn.Fill(sum,len(bgdl))

		
		cls = []
		bgdl.sort(cmp=lambda x,y: cmp(x[2], y[2]))

		for x,y,a in bgdl:
			if a>=10:
				maxv = bgd[x-1:x+2,y-1:y+2].max()
				if a==maxv and maxv>5:
					sumcl = 0
					numcl = 0
					bgd[x-1:x+2,y-1:y+2] = -abs(bgd[x-1:x+2,y-1:y+2])
					sumcl = -bgd[x-1:x+2,y-1:y+2].sum()
					numcl = (bgd[x-1:x+2,y-1:y+2]!=0).sum()
					cls.append((x,y,sumcl,numcl))
					
		self.hncl.Fill(len(cls))
		for xcl,ycl,ecl,ncl in cls:
			self.hclnum.Fill(ncl)
			self.hclsum.Fill(ecl)
			self.hclxy.Fill(xcl,ycl)
			self.hclxye.Fill(xcl,ycl,ecl)
			if ncl>4:
				self.hclsumg.Fill(ecl)
				self.hclxyg.Fill(xcl,ycl)
				self.hclxyge.Fill(xcl,ycl,ecl)
			if Mu:
				self.hclnumMu.Fill(ncl)
				self.hclsumMu.Fill(ecl)
				self.hclxyMu.Fill(xcl,ycl)
				self.hclxyeMu.Fill(xcl,ycl,ecl)
				if 0 in Mu:
					self.hclxyMu1.Fill(xcl,ycl)
					if xcl>20 and ycl<=16:
						self.hclsumMuG.Fill(ecl)
				if 1 in Mu:
					self.hclxyMu2.Fill(xcl,ycl)
					if xcl<=20 and ycl>16:
						self.hclsumMuG.Fill(ecl)
				if 2 in Mu:
					self.hclxyMu3.Fill(xcl,ycl)
					if xcl<=20 and ycl<=16:
						self.hclsumMuG.Fill(ecl)
				if 3 in Mu:
					self.hclxyMu4.Fill(xcl,ycl)
					if xcl>20 and ycl>16:
						self.hclsumMuG.Fill(ecl)
					

		if len(cls)>0:
			xcl,ycl,ecl,ncl = cls[0]
			self.hclsum1.Fill(ecl)
			self.hclxy1.Fill(xcl,ycl)
			self.hclxy1e.Fill(xcl,ycl,ecl)
			

class ViewBGD_LED:

	def __init__(self,rootfile):
        
#		self.BGD = BGD()
		
		self.dir = rootfile.mkdir("BGD_LED")
		self.dir.cd()
		
		self.hxy = []  
		for x in range(39):
			hy = []
			for y in range(32):
				name = "hLED_%02d_%02d"%(x+1,y+1)
				hy.append(TH1F( name, name,5000, 0, 5000 ))
			self.hxy.append(hy)

	def Execute(self,event):

		try:
			qdc = (0,0,event.reco["QDC-2"],event.reco["QDC-3"])
		except KeyError:
			return
		
		for c in range(2,4):
			for m,h in qdc[c].moduls.iteritems():
				for a,e in h:
					try:
						x,y = gbgd.QDC2BGD(c,m,e)
					except:
						continue

					self.hxy[x-1][y-1].Fill(a)

