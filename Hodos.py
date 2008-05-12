from ROOT import TH1F
from ROOT import TH2F

class Hod:
	" Decode hodoscop from OKA2006 DATA"
	
	def __init__(self,data):

		self.data = data
		self.bins = []
		self.hits = []
		
		for i in range(16):
			k = (data>>i)&0x1
			self.bins.append(k)
			if k:
				self.hits.append(i)

class ViewHodos:

	def __init__(self,rootfile):

		dir = rootfile.mkdir("Hod")
		dir.cd()
		self.hn = []
		self.h = []
		for i in range(4):
			self.hn.append( TH1F( 'hn%02d'%i, 'hn%02d'%i,16, 0, 16 ))
			self.h.append( TH1F( 'h%02d'%i, 'h%02d'%i,16, 0, 16 ))

	def Execute(self,event):
		
		try:
			data = event.det[25]
#			print data
			
			if len(data) == 6:

				for i in range(4):
					h = Hod(data[i+2])
					event.reco["h%d"%i] = h
					self.hn[i].Fill(len(h.hits))
					for k in range(len(h.hits)):
						self.h[i].Fill(h.hits[k])
			
		except 	KeyError,IndexError:
			pass
