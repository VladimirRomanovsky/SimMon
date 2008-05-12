from ROOT import TH1F,TH2F
	
class QDC:
	" Decode QDC from OKA2006 DATA"

	
	def __init__(self,data):

		self.data = data
		self.hits = []
		self.moduls = {}
		
		k = 2
		nhit = data[0]/2-1

		if len(data)!= data[0]:
			return	
		
		for i in range(nhit):
			self.hits.append(data[k:k+2])
			k += 2

		try:
			for a,e in self.hits:
				mod = e>>7
				ent = e&0x7F
				self.moduls.setdefault(mod,[]).append((a,ent))
		except ValueError:
			pass	

class DecodeQDC:

	def __init__(self,cr):

		self.crate = cr					

	def Execute(self,event):
		
		try:
			data = event.det[self.crate]
			qdc = QDC(data)
			event.reco["QDC-%i"%self.crate]=qdc
			
		except 	KeyError:
			pass

class ViewQDC:

	class Modul:
		def __init__(self,rootdir,mod):
			self.mod = mod
			self.dir = rootdir.mkdir("Mod-%d"%mod)
			self.dir.cd()
			self.hent = TH1F( 'hent', 'hent',96, 0, 96 )
			self.hsum = TH1F( 'hsum', 'hsum',4096, 0, 4096 )
			self.hamp = TH1F( 'hamp', 'hamp',4096, 0, 4096 )
			self.hl = []
			for i in range(96):
				self.hl.append(TH1F( 'hamp-%02d'%i, 'hamp-%02d'%i, 4096, 0, 4096 ))

		def Execute(self,data):
			sum = 0.
			for a,e in data:
				if e<96:
					self.hent.Fill(e)
					sum += a
					self.hamp.Fill(a)
					self.hl[e].Fill(a)
			self.hsum.Fill(sum)
			
	def __init__(self,rootfile,cr):

		self.crate = cr
		
		self.dir = rootfile.mkdir("QDC-%1d"%cr)
		self.dir.cd()
		
		
		self.hmod = TH1F( 'hmod', 'hmod',10, 0, 10 )
		self.hamp = TH1F( 'hamp', 'hamp',4096, 0, 4096 )
		self.hsum = TH1F( 'hsum', 'hsum',4096, 0, 4096 )
		self.hml = []
		for i in range(10):
			self.hml.append(self.Modul(self.dir,i))
					
	def Execute(self,event):
		try:
			qdc = event.reco["QDC-%i"%self.crate]

			sum = 0.
			for a,e in qdc.hits:
				sum += a
				self.hamp.Fill(a)

			moduls = qdc.moduls
			for m in moduls.keys():
				self.hmod.Fill(m)
				try:
				    self.hml[m].Execute(moduls[m])
				except IndexError:
				    print "QDC:: Error in modul number: Crate %d Modul %d" %(self.crate,m)
			self.hsum.Fill(sum)
				
		except KeyError:
			pass
