from ROOT import TH1F, TH2F

class ViewMU:

	def __init__(self,rootfile):
		
		self.dir = rootfile.mkdir("SeMuOnOff")
		self.dir.cd()

		self.h = []
		
		self.hc1 = []
		self.hc2 = []
		self.hc3 = []
		for i in range(4):
			self.h.append(TH1F( 'h%i'%i, 'h%i'%i,200, 0, 2000 ))
			self.hc1.append(TH1F( 'hc1_%i'%i, 'hc1_%i'%i,200, 0, 2000 ))
			self.hc2.append(TH1F( 'hc2_%i'%i, 'hc2_%i'%i,200, 0, 2000 ))
			self.hc3.append(TH1F( 'hc3_%i'%i, 'hc3_%i'%i,200, 0, 2000 ))
		
		
		self.h01 = TH2F( 'h_01', 'h_01', 100, 0, 2000, 100, 0, 2000 )
		self.h02 = TH2F( 'h_02', 'h_02', 100, 0, 2000, 100, 0, 2000 )
		self.h03 = TH2F( 'h_03', 'h_03', 100, 0, 2000, 100, 0, 2000 )
		self.h12 = TH2F( 'h_12', 'h_12', 100, 0, 2000, 100, 0, 2000 )
		self.h13 = TH2F( 'h_13', 'h_13', 100, 0, 2000, 100, 0, 2000 )
		self.h23 = TH2F( 'h_23', 'h_23', 100, 0, 2000, 100, 0, 2000 )
		
		
		
		self.th = (50,50,50,50)
		
	def Execute(self,event):

		try:
			qdc = event.reco["QDC-2"]
		except KeyError:
			return
		
		mu = [0,0,0,0]
		
		try:
			m7 = qdc.moduls[7]
			for a,e in m7:
				if e == 71:
					mu[0] = a
		except:
			pass

		try:
			m8 = qdc.moduls[8]
			for a,e in m8:
				if e == 23:
					mu[1] = a
				if e == 40:
					mu[2] = a
				if e == 47:
					mu[3] = a
		except:
			pass

		flag = [False,False,False,False]

		for i in range(4):
			self.h[i].Fill(mu[i])
			if mu[i]>self.th[i]:
				flag[i] = True

		self.h01.Fill(mu[0],mu[1])
		self.h02.Fill(mu[0],mu[2])
		self.h03.Fill(mu[0],mu[3])
		self.h12.Fill(mu[1],mu[2])
		self.h13.Fill(mu[1],mu[3])
		self.h23.Fill(mu[2],mu[3])
		
		for i in range(4):
			count = 0
			for k in range(4):
				if k != i and flag[k]:
					count += 1
			if count>0:
				self.hc1[i].Fill(mu[i])
			if count>1:
				self.hc2[i].Fill(mu[i])
			if count>2:
				self.hc3[i].Fill(mu[i])

