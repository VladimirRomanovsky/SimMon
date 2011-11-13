from ROOT import TH1F,TH2F

from numpy import resize

class ViewGDA:
	decod7 = {22:(1,1),21:(1,2),20:(1,3),19:(1,4),18:(1,5),17:(1,6),16:(1,7),15:(1,8),14:(1,9),13:(1,10),12:(1,11),
	          11:(2,1),10:(2,2),9:(2,3),8:(2,4),7:(2,5),6:(2,6),5:(2,7),4:(2,8),3:(2,9),2:(2,10),1:(2,11),
		  0:(3,1),46:(3,2),45:(3,3),44:(3,4),43:(3,5),42:(3,6),41:(3,7),40:(3,8),39:(3,9),38:(3,10),37:(3,11),
		  36:(4,1),35:(4,2),34:(4,3),33:(4,4),32:(4,5),31:(4,6),30:(4,7),29:(4,8),28:(4,9),27:(4,10),26:(4,11),
		  25:(5,1),24:(5,2),70:(5,3),69:(5,4),68:(5,5),67:(5,6),66:(5,7),65:(5,8),64:(5,9),63:(5,10),62:(5,11),
		  61:(6,1),60:(6,2),59:(6,3),58:(6,4),57:(6,5),56:(6,6),55:(6,7),54:(6,8),53:(6,9),52:(6,10),51:(6,11),
		  50:(7,1),49:(7,2),48:(7,3),94:(7,4),93:(7,5),92:(7,6),91:(7,7),90:(7,8),89:(7,9),88:(7,10),87:(7,11),
		  86:(8,1),85:(8,2),84:(8,3),83:(8,4),82:(8,5),81:(8,6),80:(8,7),79:(8,8),78:(8,9),77:(8,10),76:(8,11),
		  75:(9,1),74:(9,2),73:(9,3),72:(9,4)}
	decod8 = {22:(9,5),21:(9,6),20:(9,7),19:(9,8),18:(9,9),17:(9,10),16:(9,11),
		  15:(10,1),14:(10,2),13:(10,3),12:(10,4),11:(10,5),10:(10,6),9:(10,7),8:(10,8),7:(10,9),6:(10,10),5:(10,11),
		  4:(11,1),3:(11,2),2:(11,3),1:(11,4),0:(11,5),46:(11,6),45:(11,7),44:(11,8),43:(11,9),42:(11,10)}

	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("GDA")
		self.dir.cd()
		
		
		self.h = TH1F( 'h', 'h',200, 0, 200 )
		self.h7 = TH1F( 'h7', 'h7',96, 0, 96 )
		self.h8 = TH1F( 'h8', 'h8',96, 0, 96 )
		self.h2 = TH2F( 'h2', 'h2',13, 0, 13, 13, 0, 13 )
		self.h2a = TH2F( 'h2a', 'h2a',13, 0, 13, 13, 0, 13 )
		self.hsum = TH1F( 'hsum', 'hsum',1000, 0, 5000 )
		self.hamp = TH1F( 'hamp', 'hamp',1000, 0, 1000 )
		self.hncl = TH1F( 'hncl', 'hncl',20, 0, 20)
		self.hecl = TH1F( 'hecl', 'hecl',100, 0, 1000)
		self.hxy = TH2F( 'hxy', 'hxy',11, 1, 12,11,1,12)
		self.hkcl = TH1F( 'hkcl', 'hkcl',20, 0, 20)

		self.hmu = []
		self.hmu.append(TH1F( 'hmu1', 'h',1000, 0, 1000 ))
		self.hmu.append(TH1F( 'hmu2', 'h',1000, 0, 1000 ))
		self.hmu.append(TH1F( 'hmu3', 'h',1000, 0, 1000 ))
		self.hmu.append(TH1F( 'hmu4', 'h',1000, 0, 1000 ))

		self.hsumMu = TH1F( 'hsumMu', 'hsum',1000, 0, 5000 )
		self.hxyMu = []
		self.hxyMu.append(TH2F( 'hxyMu1', 'hxy',11, 1, 12,11,1,12))
		self.hxyMu.append(TH2F( 'hxyMu2', 'hxy',11, 1, 12,11,1,12))
		self.hxyMu.append(TH2F( 'hxyMu3', 'hxy',11, 1, 12,11,1,12))
		self.hxyMu.append(TH2F( 'hxyMu4', 'hxy',11, 1, 12,11,1,12))

                xydir = self.dir.mkdir("XY")
		xydir.cd()
		self.hixiy = []  
		for x in range(11):
			hiy = []
			for y in range(11):
				name = "h_%02d_%02d"%(x+1,y+1)
				hiy.append(TH1F( name, name,5000, 0, 5000 ))
			self.hixiy.append(hiy)

	def Execute(self,event):
		try:
			qdc = event.reco["QDC-2"]
			
		except KeyError:
			return
		try:
			m7 = qdc.moduls[7]
			
		except KeyError:
			m7 = []

		try:
			m8 = qdc.moduls[8]
			
		except KeyError:
			m8 = []
			
		gda = []
		
		for a,e in m7:
#			if e<96:
#				self.h7.Fill(e)
#				e2 = divmod(e,24)
#				enew = e2[0]*24+23-e2[1]

			if e in self.decod7.keys():
				gda.append((a,self.decod7[e]))
			
		mu = [0,0,0,0]

		for a,e in m8:
#			if e<48:
#				self.h8.Fill(e)
#				e2 = divmod(e,24)
#				enew = e2[0]*24+ 23 - e2[1] + 96

			if e in self.decod8.keys():
				gda.append((a,self.decod8[e]))

			if e == 71:
				mu[0] = a
			if e == 70:
				mu[1] = a
			if e == 69:
				mu[2] = a
			if e == 68:
				mu[3] = a

		Mu = []
		for imu in range(4):
			if mu[imu]:
				self.hmu[imu].Fill(mu[imu])
				if mu[imu]> 20:
					Mu.append(imu)
					
		event.reco["MU"] = Mu

		sum = 0

		gdam = resize(0,(13,13))

		for a,(ix,iy) in gda:
			self.h.Fill(e)
			self.hamp.Fill(a)
			gdam[ix,iy] = a				
			sum += a
			self.h2.Fill(ix,iy)
			self.h2a.Fill(ix,iy,a)
			self.hixiy[ix-1][iy-1].Fill(a)
		self.hsum.Fill(sum)
		if Mu:
			self.hsumMu.Fill(sum)
							
#		print gdam
		
		cl = []
		for ix in range(1,12):
			for iy in range(1,12):
				if gdam[ix,iy]>20 and gdam[ix-1:ix+2,iy-1:iy+2].max()==gdam[ix,iy]:
					cl.append((ix,iy))
		
#		print cl

		self.hncl.Fill(len(cl))

		for c in cl:
			ix = c[0]
			iy = c[1]
			sumcl =  gdam[ix-1:ix+1,iy-1:iy+2].sum()
			self.hecl.Fill(sumcl)			
			self.hxy.Fill(ix,iy)
			for i in Mu:
				self.hxyMu[i].Fill(ix,iy)

			kcl = 0
			for jx in range(-1,2):				
				for jy in range(-1,2):
					if gdam[ix+jx,iy+jy]>20:
						kcl += 1				
			self.hkcl.Fill(kcl)
			

class ViewGDA_LED:
	decod7 = {22:(1,1),21:(1,2),20:(1,3),19:(1,4),18:(1,5),17:(1,6),16:(1,7),15:(1,8),14:(1,9),13:(1,10),12:(1,11),
	          11:(2,1),10:(2,2),9:(2,3),8:(2,4),7:(2,5),6:(2,6),5:(2,7),4:(2,8),3:(2,9),2:(2,10),1:(2,11),
		  0:(3,1),46:(3,2),45:(3,3),44:(3,4),43:(3,5),42:(3,6),41:(3,7),40:(3,8),39:(3,9),38:(3,10),37:(3,11),
		  36:(4,1),35:(4,2),34:(4,3),33:(4,4),32:(4,5),31:(4,6),30:(4,7),29:(4,8),28:(4,9),27:(4,10),26:(4,11),
		  25:(5,1),24:(5,2),70:(5,3),69:(5,4),68:(5,5),67:(5,6),66:(5,7),65:(5,8),64:(5,9),63:(5,10),62:(5,11),
		  61:(6,1),60:(6,2),59:(6,3),58:(6,4),57:(6,5),56:(6,6),55:(6,7),54:(6,8),53:(6,9),52:(6,10),51:(6,11),
		  50:(7,1),49:(7,2),48:(7,3),94:(7,4),93:(7,5),92:(7,6),91:(7,7),90:(7,8),89:(7,9),88:(7,10),87:(7,11),
		  86:(8,1),85:(8,2),84:(8,3),83:(8,4),82:(8,5),81:(8,6),80:(8,7),79:(8,8),78:(8,9),77:(8,10),76:(8,11),
		  75:(9,1),74:(9,2),73:(9,3),72:(9,4)}
	decod8 = {22:(9,5),21:(9,6),20:(9,7),19:(9,8),18:(9,9),17:(9,10),16:(9,11),
		  15:(10,1),14:(10,2),13:(10,3),12:(10,4),11:(10,5),10:(10,6),9:(10,7),8:(10,8),7:(10,9),6:(10,10),5:(10,11),
		  4:(11,1),3:(11,2),2:(11,3),1:(11,4),0:(11,5),46:(11,6),45:(11,7),44:(11,8),43:(11,9),42:(11,10)}

	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("GDA_LED")
		self.dir.cd()
		
		
		self.h = TH1F( 'h', 'h',5000, 0, 5000 )
		self.h2 = TH2F( 'h2', 'h2',13, 0, 13, 13, 0, 13 )

		self.hxy = []  
		for x in range(11):
			hy = []
			for y in range(11):
				name = "hLED_%02d_%02d"%(x+1,y+1)
				hy.append(TH1F( name, name,5000, 0, 5000 ))
			self.hxy.append(hy)


	def Execute(self,event):
		try:
			qdc = event.reco["QDC-2"]
			
		except KeyError:
			return
		try:
			m7 = qdc.moduls[7]
			
		except KeyError:
			m7 = []

		try:
			m8 = qdc.moduls[8]
			
		except KeyError:
			m8 = []
			
		gda = []
		
		for a,e in m7:
#			if e<96:
#				self.h7.Fill(e)
#				e2 = divmod(e,24)
#				enew = e2[0]*24+23-e2[1]

			if e in self.decod7.keys():
				gda.append((a,self.decod7[e]))
			
		for a,e in m8:
#			if e<48:
#				self.h8.Fill(e)
#				e2 = divmod(e,24)
#				enew = e2[0]*24+ 23 - e2[1] + 96

			if e in self.decod8.keys():
				gda.append((a,self.decod8[e]))


		for a,(ix,iy) in gda:
			self.h.Fill(a)
			self.h2.Fill(ix,iy)
                        self.hxy[ix-1][iy-1].Fill(a)

			
		
