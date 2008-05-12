from ROOT import TH1F,TH2F

class ViewWideHead:

	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("WideHead")
		self.dir.cd()
		
		self.h =[]
		for i in range(12):
			self.h.append( TH1F( 'h%02d'%i, 'h%02d'%i, 4096, 0, 4096 ))
		self.h12 = TH2F( 'h_1_2', 'h_1_2', 1000, 0, 1000, 1000, 0, 1000 )
		self.hc11 = TH1F( 'hc11', 'hc11', 100, 0, 300 )	
		self.hc12 = TH1F( 'hc12', 'hc12', 100, 300, 600 )	
		self.hc21 = TH1F( 'hc21', 'hc21', 100, 0, 300 )	
		self.hc22 = TH1F( 'hc22', 'hc22', 100, 300, 600 )	
	def Execute(self,event):
		
		try:
			data = event.det[24]
#			print data
		
			if len(data) == 14 :
				for i in range(12):
					t = data[2+i] 
					self.h[i].Fill(t)

				self.h12.Fill(data[3],data[4])
			
				self.hc11.Fill(data[2+1]) 
				self.hc12.Fill(data[2+1]) 

				self.hc21.Fill(data[2+2]) 
				self.hc22.Fill(data[2+2]) 
			
		except 	KeyError:
			pass
