from ROOT import TH1F,TH2F

class SG:

	def __init__(self):
	
		self.ringconfig = [10,10,13,13,16,16,20,20,24,24,26] 
	
		self.ringmap = []
		for i in range(11):
			for k in range(self.ringconfig[i]):
				self.ringmap.append((i,k))

	def __getitem__(self,e):
		
		return  self.ringmap[e]
								
class ViewSG:

	class HSG:
		def __init__(self,rootfile,number,leng):
		
			self.dir = rootfile.mkdir("RING_%02i"%number)
			self.dir.cd()
			self.hn = TH1F( 'hn', 'hn',leng, 0, leng )
			self.hamp = TH1F( 'hamp', 'hamp',4096, 0, 4096 )
			self.hsum = TH1F( 'hsum', 'hsum',4096, 0, 4096 )
			self.hee = TH2F( 'hee', 'hee',leng, 0, leng, leng, 0, leng )
			self.haa = TH2F( 'haa', 'haa',1000, 0, 4000, 1000, 0, 4000 )
			self.haamu = TH2F( 'haamu', 'haamu',1000, 0, 4000, 1000, 0, 4000 )
			self.hamps = []
			for i in range(leng):
				self.hamps.append( TH1F( 'hamp_%02i'%i, 'hamp_%02i'%i,4096, 0, 4096 ))
		
		def Fill(self,data,mu):
			sum = 0
			self.hn.Fill(len(data))
			for a,e in data:
				self.hamp.Fill(a)
				self.hamps[e].Fill(a)
				sum += a
			self.hsum.Fill(sum)
			for a1,e1 in data:
				for a2, e2 in data:
					if not e1==e2:
						self.hee.Fill(e1,e2,a1*a2)
					if abs(e1-e2)==1:
						self.haa.Fill(a1,a2)
						if mu:	
							self.haamu.Fill(a1,a2)	
						
	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("SG")
		self.dir.cd()
		
		
		self.SG = SG()
				
		self.hn = TH1F( 'hn', 'hn',200, 0, 200 )
		self.hamp = TH1F( 'hamp', 'hamp',4096, 0, 4096 )
		self.hsum = TH1F( 'hsum', 'hsum',4096, 0, 4096 )
		
		self.hrr = []
		self.hrrMu = []
		for i in range(10):
			r1 = self.SG.ringconfig[i]
			r2 = self.SG.ringconfig[i+1]
			self.hrr.append(TH2F( 'hr%02dr%02d'%(i,i+1), 'hr%02dr%02d'%(i,i+1), r1, 0, r1, r2, 0, r2 ))
			self.hrrMu.append(TH2F( 'hr%02dr%02dMu'%(i,i+1), 'hr%02dr%02dMu'%(i,i+1), r1, 0, r1, r2, 0, r2 ))
	
		self.hee=TH2F( 'hee', 'hee', 1000, 0, 4000, 1000, 0, 4000 )
		self.heeMu=TH2F( 'heeMu', 'hee', 1000, 0, 4000, 1000, 0, 4000 )
		
		self.hrings = []
		for i in range(11):
			self.hrings.append(self.HSG(self.dir,i,self.SG.ringconfig[i]))

	def Execute(self,event):

		try:
			qdc = event.reco["QDC-2"]
		except KeyError:
			return
		
		try:
			mu = event.reco["MU"]
		except KeyError:
			mu = []
		
			
		sg = []
		
		for i in (5,6):
			try:
				m = qdc.moduls[i]
			except KeyError:
				continue

			for a,e in m:
				if e<96:
					x,e = divmod(e,24)
					enew = 96 *(i-5) + x*24 + (23-e)
					sg.append((a,enew))
							
		sum = 0

		rings = {}

		self.hn.Fill(len(sg))
		for a,e in sg:
			sum += a
			self.hamp.Fill(a)
			try:
				r,e = self.SG[e]
			except IndexError:
				print "ERROR:",e
				continue
			rings.setdefault(r,[]).append((a,e))
			
		self.hsum.Fill(sum)

#		print rings


		for r in rings.keys():
			self.hrings[r].Fill(rings[r],mu)
			if rings.has_key(r+1):
				for a1,e1 in rings[r]:
					for a2,e2 in rings[r+1]:
						self.hrr[r].Fill(e1,e2,a1*a2)
						if mu:
							self.hrrMu[r].Fill(e1,e2,a1*a2)
	
		if rings.has_key(8) and rings.has_key(9):
			for a1,e1 in rings[8]:
				for a2,e2 in rings[9]:
					de = e1 - e2
					if abs(de)<2 or abs(de-24)<2 or abs(de+24)<2:
						self.hee.Fill(a1,a2)
						if mu:
							self.heeMu.Fill(a1,a2)
			
