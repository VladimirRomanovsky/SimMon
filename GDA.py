from ROOT import TH1F,TH2F

from numpy import zeros

class GDA:

	def __init__(self):
	
		conf = file("config_gda.dat")

		self.decodem7 = {}
		self.decodem8 = {}
		for string in conf:
			ss = string.split()
			x = int(ss[0])
			y = int(ss[1])
			m = int(ss[2])
			e = int(ss[3])
			if m == 7:
				self.decodem7[e] = (x,y)
			if m == 8:
				self.decodem8[e] = (x,y)
	
	def Decode(self,event):

		self.hits = []
		 
		try:
			qdc = event.reco["QDC-2"]

		except KeyError:
			return

		try:
			data = qdc.moduls[7]
		except:
			pass
		else:
			for a,e in data:
				if e<96:
					try:
						x,y = self.decodem7[e]
					except KeyError:
						pass
					else:
						self.hits.append((x,y,a+3))
		try:
			data = qdc.moduls[8]
		except:
			pass
		else:
			for a,e in data:
				if e<96:
					try:
						x,y = self.decodem8[e]
					except KeyError:
						pass
					else:
						self.hits.append((x,y,a+3))
		
	def __str__(self):
		res =  "GDA:\n"
		for h in  self.hits:
			res += "(%i %i %i)"%h
		return res

gda = GDA()
		

class ViewLedGDA:

        class HModQDC:
                def __init__(self,rootfile,name):

                        self.dir = rootfile.mkdir(name)
                        self.dir.cd()
			
			self.hl = []
			for i in range(96):
				self.hl.append(TH1F( 'hamp-%02d'%i, 'hamp-%02d'%i, 4096, 0, 4096 ))
			self.h = TH1F( 'h', 'h', 96, 0, 96 )

		def Fill(self,data):
			for a,e in data:
				if e<96:
					self.hl[e].Fill(a)
					self.h.Fill(e)

	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("GDA_LED")
		self.dir.cd()
		
		self.hm7 = self.HModQDC(self.dir,"Modul7")
		self.hm8 = self.HModQDC(self.dir,"Modul8")
		
		ampdir = self.dir.mkdir("AMP")
		ampdir.cd()

		self.hamps=[]
		for x in range(1,12):
			hists = []
			for y in range(1,12):
				hists.append(TH1F( 'hamp_%i_%i'%(x,y), 'hamp_%i_%i'%(x,y),500, 0, 5000 ))
			self.hamps.append(hists)

	def Execute(self,event):
		try:
			qdc = event.reco["QDC-2"]

		except KeyError:
			return

		try:
			m7 = qdc.moduls[7]
		except:
			pass
		else:
			self.hm7.Fill(m7)

		try:
			m8 = qdc.moduls[8]
		except:
			pass
		else:
			self.hm8.Fill(m8)

		gda.Decode(event)
		for x,y,a in gda.hits:
			self.hamps[x-1][y-1].Fill(a) 

class ViewGDA:

	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("GDA")
		self.dir.cd()

		self.hamp= TH1F( 'hamp', 'hamp',1000, 0, 1000 )
		self.hsum= TH1F( 'hsum', 'hsum',1000, 0, 10000 )
		self.hsumn= TH2F( 'hsumn', 'hsumn',1000, 0, 10000 ,150, 0, 150)
		self.hxy = TH2F( 'hxy', 'hxy',11, 1, 12, 11, 1, 12 )
		self.hxyth = TH2F( 'hxyth', 'hxyth',11, 1, 12, 11, 1, 12 )
		self.hxymu = TH2F( 'hxymu', 'hxymu',11, 1, 12, 11, 1, 12 )

		
		ampdir = self.dir.mkdir("AMP")
		ampdir.cd()

		self.hamps=[]
		for x in range(1,12):
			hists = []
			for y in range(1,12):
				hists.append(TH1F( 'hamp_%i_%i'%(x,y), 'hamp_%i_%i'%(x,y),1000, 0, 1000 ))
			self.hamps.append(hists)
					
		
	def Execute(self,event):
		
		gda.Decode(event)
#		print gda
		sum = 0
		for x,y,a in gda.hits:
			self.hamps[x-1][y-1].Fill(a) 
			self.hamp.Fill(a) 
			self.hxy.Fill(x,y)
			if a>50:
				self.hxyth.Fill(x,y)
			sum += a
		self.hsum.Fill(sum)
		self.hsumn.Fill(sum,len(gda.hits))

		try:
			mu = event.reco["MU"]

		except KeyError:
			return
		
		for amp in mu:
			if amp<50:
				return
				
		for x,y,a in gda.hits:			
			if a>50:
				self.hxymu.Fill(x,y)
		
