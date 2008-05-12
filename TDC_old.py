from ROOT import TH1F,TH2F

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
			self.hdt0.append( TH1F( 'hdt-%d-0'%i, 'hdt-0%d-0'%i,1024, -1024, 1024 ))
			self.hdt1.append( TH1F( 'hdt-%d-1'%i, 'hdt-1%d-1'%i,1024, -1024, 1024 ))
			self.hdt2.append( TH1F( 'hdt-%d-2'%i, 'hdt-2%d-2'%i,1024, -1024, 1024 ))
			self.hdt3.append( TH1F( 'hdt-%d-3'%i, 'hdt-3%d-3'%i,1024, -1024, 1024 ))
			
		self.hc1 = TH1F( 'hc1', 'hc1', 2, 50, 550 )	
		self.hc2 = TH1F( 'hc2', 'hc2', 2, 50, 550 )	
		self.hc12 = TH2F( 'hc12', 'hc12', 2, 50, 550, 2, 50, 550 )	

		self.h12 = TH2F( 'h12', 'h12', 1024, 0, 1024, 1024, 0, 1024 )	
		self.h1d2 = TH2F( 'h1d2', 'h1d2', 1024, 0, 1024, 1024, -1024, 1024 )	

		self.hcc0 = [] 
		self.hcc1 = [] 
		self.hccd = [] 
		for i in range(9):
			self.hcc0.append( TH1F( 'ht0c%d'%i, 'ht0c%d'%i,1024, 0, 1024 ))
			self.hcc1.append( TH1F( 'ht1c%d'%i, 'ht1c%d'%i,1024, 0, 1024 ))
			self.hccd.append( TH1F( 'htdc%d'%i, 'htdc%d'%i,1024, -1024, 1024 ))

	def Execute(self,event):
		
		try:
			data = event.det[20]
#			print data

			if len(data)<6:
				return
				
				
			for i in range(4):
				t = data[2+i] 
				self.h[i].Fill(t)				
				if t>0 and t<511:
					if data[2+0]>0 and data[2+0]<511:
						self.hdt0[i].Fill(t-data[2+0])
					if data[2+1]>0 and data[2+1]<511:
						self.hdt1[i].Fill(t-data[2+1])
					if data[2+2]>0 and data[2+2]<511:
						self.hdt2[i].Fill(t-data[2+2])
					if data[2+3]>0 and data[2+3]<511:
						self.hdt3[i].Fill(t-data[2+3])

			self.hc1.Fill(data[2+2])
			self.hc2.Fill(data[2+3])
			self.hc12.Fill(data[2+2],data[2+3])

			self.h12.Fill(data[2+0],data[2+1])
			self.h1d2.Fill(data[2+0],data[2+1]-data[2+0])
			
			n1 = 0
			if 50<data[2+2]<300:
				n1 = 1
			if 300<data[2+2]<550:
				n1 = 2
			n2 = 0
			if 50<data[2+3]<300:
				n2 = 1
			if 300<data[2+3]<550:
				n2 = 2
				
			self.hcc0[n1+n2*3].Fill(data[2+0])
			self.hcc1[n1+n2*3].Fill(data[2+1])
			self.hccd[n1+n2*3].Fill(data[2+1] - data[2+0])
			
		except 	KeyError,IndexError:
			pass
