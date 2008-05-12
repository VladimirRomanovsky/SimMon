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
			self.hamps = []
			for i in range(leng):
				self.hamps.append( TH1F( 'hamp_%i'%i, 'hamp_%i'%i,4096, 0, 4096 ))
			self.hamp2 = TH2F( 'hamp2', 'hamp2',leng,0,leng,leng,0,leng)
			self.hsumn = TH2F( 'hsumn', 'hsumn',4096,0,4096,leng,0,leng)
			
		def Fill(self,data):
			sum = 0
			self.hn.Fill(len(data))
			for a,e in data:
				self.hamp.Fill(a)
				self.hamps[e].Fill(a)
				sum += a
				for a2,e2 in data:
					if e != e2 and a>50 and a2>50:
						self.hamp2.Fill(e,e2)
			self.hsum.Fill(sum)
			self.hsumn.Fill(sum,len(data))

	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("SG")
		self.dir.cd()
		
		
		self.SG = SG()
				
		self.hn = TH1F( 'hn', 'hn',200, 0, 200 )
		self.hamp = TH1F( 'hamp', 'hamp',4096, 0, 4096 )
		self.hsum = TH1F( 'hsum', 'hsum',4096, 0, 4096 )
		self.hrings = []
		for i in range(11):
			self.hrings.append(self.HSG(self.dir,i,self.SG.ringconfig[i]))

	def Execute(self,event):

		try:
			qdc = event.reco["QDC-2"]
		except KeyError:
			return
			
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
			self.hrings[r].Fill(rings[r])
	
