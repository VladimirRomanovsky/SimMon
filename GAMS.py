from ROOT import TH1F,TH2F

from numpy import zeros
from utils import *
from copy import deepcopy

class ViewGAMS:
	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("GAMS")
		self.dir.cd()

		self.hamp = TH1F( 'hamp', 'hamp',1000, 0, 1000 )

		self.hxy = TH2F( 'hxy', 'hxy',48, 1, 49, 48, 1, 49 )
		self.hxya = TH2F( 'hxya', 'hxya',48, 1, 49, 48, 1, 49 )

		self.hsum = TH1F( 'hsum', 'hsum',1000, 0, 4000 )
		self.hnum = TH1F( 'hnum', 'hnum',100, 0, 100 )
		self.hsn = TH2F( 'hsn', 'hsn',100, 0, 4000, 100, 0, 100 )

		self.hdxdy = TH2F( 'hdxdy', 'hdxdy',20, 0, 20, 20, 0, 20 )
		self.hdxdya = TH2F( 'hdxdya', 'hdxdya',20, 0, 20, 20, 0, 20 )

		self.hncl = TH1F( 'hncl', 'hncl',20, 0, 20 )

		self.hclnum = TH1F( 'hclnum', 'hclnum',10, 0, 10 )
		self.hclsum = TH1F( 'hclsum', 'hclsum',1000, 0, 4000 )
		self.hclxy = TH2F( 'hclxy', 'hclxy',48, 1, 49, 48, 1, 49 )
		self.hclxye = TH2F( 'hclxye', 'hclxye',48, 1, 49, 48, 1, 49 )
		self.hclsumg = TH1F( 'hclsumg', 'hclsumg',1000, 0, 4000 )
		self.hclxyg = TH2F( 'hclxyg', 'hclxyg',48, 1, 49, 48, 1, 49 )
		self.hclxyeg = TH2F( 'hclxyeg', 'hclxyeg',48, 1, 49, 48, 1, 49 )

		dirMu = self.dir.mkdir("Mu")
		dirMu.cd()
		self.hclxyMu = []
		self.hclxyMu.append(TH2F( 'hclxy1', 'hclxy',48, 1, 49, 48, 1, 49 ))
		self.hclxyMu.append(TH2F( 'hclxy2', 'hclxy',48, 1, 49, 48, 1, 49 ))
		self.hclxyMu.append(TH2F( 'hclxy3', 'hclxy',48, 1, 49, 48, 1, 49 ))
		self.hclxyMu.append(TH2F( 'hclxy4', 'hclxy',48, 1, 49, 48, 1, 49 ))
		self.hclsumMu = TH1F( 'hclsum', 'hclsum',1000, 0, 4000 )
		self.hclsumMuG = TH1F( 'hclsumG', 'hclsum',1000, 0, 4000 )

		self.bad = []
		
#		self.bad.append((ix, iy))
		self.bad.append((  5, 44))
		self.bad.append((  2, 46))
		self.bad.append(( 26, 48))
		self.bad.append(( 30,  4))
		self.bad.append(( 30,  6))
		self.bad.append(( 38, 24))
		self.bad.append(( 13, 23))
		self.bad.append(( 19, 19))
		self.bad.append(( 25, 32))
		self.bad.append(( 23, 35))
		self.bad.append(( 27, 24))
		self.bad.append(( 26, 26))

		baddir = self.dir.mkdir("BAD")
		baddir.cd()
		
		self.hbad = {}
		for b in self.bad:
		 	self.hbad[b] = TH1F( 'hbad%02i%02i'%b, 'hbad%02i%02i'%b,1000, 0, 1000 )
			
	def _QDC2GAMS(self,crate,modul,entry):
		mmin = (0,0,0)
		mmax = (9,9,3)

		if not ( crate in (0,1,2)):
			return None

		if modul<mmin[crate] or modul>mmax[crate]:
			return None		

# invert GREEN plate
		x,e = divmod(entry,24)
		entry = x*24 + (23-e)
		ix,iy = divmod(entry,48)
		iy += 1
		ix = ix + 1 + modul*2 + 20*crate
		
		if ix>48:
			return None
			
		return (ix,iy)
			
	def Execute(self,event):

		try:
			qdc = (event.reco["QDC-0"],event.reco["QDC-1"],event.reco["QDC-2"])
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
			
		gams = zeros((50,50),int) 
		gamsl = [] 

		for c in range(3):
			for m,h in qdc[c].moduls.iteritems():
				for a,e in h:
					try:
						x,y = self._QDC2GAMS(c,m,e)
					except :
                				continue
					
					if (x,y) in self.bad:
						self.hbad[(x,y)].Fill(a+3)
					else:						
						gamsl.append((x,y,a+3))
						gams[x,y]=a+3
		
		sum = 0
		for x,y,a in gamsl:
			self.hamp.Fill(a)
			self.hxy.Fill(x,y)
			self.hxya.Fill(x,y,a)
			sum += a
		self.hsum.Fill(sum)
		self.hnum.Fill(len(gamsl))
		self.hsn.Fill(sum,len(gamsl))
		
		for x1,y1,a1 in gamsl:
			for x2,y2,a2 in gamsl:
				if (x1!=x2 or y1!=y2) and a1>10 and a2>10 :
					dx = abs(x1-x2)
					dy = abs(y1-y2)
					self.hdxdy.Fill(dx,dy)
					self.hdxdya.Fill(dx,dy,a1*a2)
		
		cls = []
		for x,y,a in gamsl:
			if a>=10:
				maxv = gams[x-1:x+2,y-1:y+2].max()
				if a==maxv and maxv>10:
					sumcl = 0
					numcl = 0
					gams[x-1:x+2,y-1:y+2] = -abs(gams[x-1:x+2,y-1:y+2])
					sumcl = -gams[x-1:x+2,y-1:y+2].sum()
					numcl = (gams[x-1:x+2,y-1:y+2]!=0).sum()
					cls.append((x,y,sumcl,numcl))
					
		self.hncl.Fill(len(cls))
		for xcl,ycl,ecl,ncl in cls:
			self.hclnum.Fill(ncl)
			self.hclsum.Fill(ecl)
			self.hclxy.Fill(xcl,ycl)
			self.hclxye.Fill(xcl,ycl,ecl)
			if ncl>1:
				self.hclsumg.Fill(ecl)
				self.hclxyg.Fill(xcl,ycl)
				self.hclxyeg.Fill(xcl,ycl,ecl)

			for imu in Mu:
				self.hclxyMu[imu].Fill(xcl,ycl)				
			if Mu:
				self.hclsumMu.Fill(ecl)				
		
			if 0 in Mu and xcl>24 and ycl<=24:
				self.hclsumMuG.Fill(ecl)
			if 1 in Mu and xcl<=24 and ycl>24:
				self.hclsumMuG.Fill(ecl)
			if 2 in Mu and xcl<=24 and ycl<=24:
				self.hclsumMuG.Fill(ecl)
			if 3 in Mu and xcl>24 and ycl>24:
				self.hclsumMuG.Fill(ecl)
				
