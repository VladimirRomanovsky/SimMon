from ROOT import TH1F,TH2F,TTree

from array import array

class DecodeTDC:
	def __init__(self):
		pass

	def Execute(self,event):
		
		try:
			data = event.det[20]
			if len(data)==6:
				event.reco["TDC"]=data[2:6]
		except 	KeyError:
			pass
class ViewTDC:

	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("TDC")
		self.dir.cd()
		
		self.h =[]
		self.hdt0 =[]
		self.hdt1 =[]
		self.hdt2 =[]
		self.hdt3 =[]
		for i in range(4):
			self.h.append( TH1F( 'h%02d'%i, 'h%02d'%i,1024, 0, 1024 ))
			self.hdt0.append( TH1F( 'hdt_%d-0'%i, 'hdt_0%d-0'%i,1024, -1024, 1024 ))
			self.hdt1.append( TH1F( 'hdt_%d-1'%i, 'hdt_1%d-1'%i,1024, -1024, 1024 ))
			self.hdt2.append( TH1F( 'hdt_%d-2'%i, 'hdt_2%d-2'%i,1024, -1024, 1024 ))
			self.hdt3.append( TH1F( 'hdt_%d-3'%i, 'hdt_3%d-3'%i,1024, -1024, 1024 ))
			

	def Execute(self,event):
		
		try:
			data = event.reco["TDC"]
#			print data

			for i in range(4):
				t = data[i] 
				self.h[i].Fill(t)				
				self.hdt0[i].Fill(t-data[0])			
				self.hdt1[i].Fill(t-data[1])			
				self.hdt2[i].Fill(t-data[2])			
				self.hdt3[i].Fill(t-data[3])			
		except 	(KeyError,IndexError):
			pass
class TreeTDC:

	
	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("TDC_Tree")
		self.dir.cd()
		self.t = TTree( 'TDC', 'tree with TDC' )
		self.array = array('i',4*[0])
		self.t.Branch( 'tdc', self.array, 'tdc1/I:tdc2:tdc3:tdc4' )

	def Execute(self,event):
		try:
			data = event.reco["TDC"]

			for i in range(4):
				self.array[i] = data[i] 
			self.t.Fill()
			
		except 	KeyError:
			pass
