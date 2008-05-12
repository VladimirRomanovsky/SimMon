from ROOT import TH1F,TH2F

from numpy import resize

class ViewGDA:

		
	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("GDA")
		self.dir.cd()
		
		
		self.h = TH1F( 'h', 'h',200, 0, 200 )
		self.h9 = TH1F( 'h9', 'h9',96, 0, 96 )
		self.h8 = TH1F( 'h8', 'h8',96, 0, 96 )
		self.h2 = TH2F( 'h2', 'h2',20, 0, 20, 20, 0, 20 )
		self.h2a = TH2F( 'h2a', 'h2a',20, 0, 20, 20, 0, 20 )
		self.hmu = TH2F( 'hmu', 'hmu',100, 0, 1000, 100, 0, 1000 )
		self.hsum = TH1F( 'hsum', 'hsum',100, 0, 5000 )
		self.hsumc = TH1F( 'hsumc', 'hsumc',100, 0, 1000 )
		self.hsumch = TH1F( 'hsumch', 'hsumch',100, 0, 1000 )
		self.hsumch1 = TH1F( 'hsumch1', 'hsumch',100, 0, 1000 )
		self.hsumch2 = TH1F( 'hsumch2', 'hsumch',100, 0, 1000 )
		self.hamp = TH1F( 'hamp', 'hamp',100, 0, 1000 )
		self.h36 = TH1F( 'h36', 'h36',100, 0, 1000 )
		self.h36g = TH1F( 'h36g', 'h36g',100, 0, 1000 )
		self.h46 = TH1F( 'h46', 'h46',100, 0, 1000 )
		self.h45 = TH1F( 'h45', 'h45',100, 0, 1000 )
		self.h45g = TH1F( 'h45g', 'h45g',100, 0, 1000 )
		self.h47 = TH1F( 'h47', 'h47',100, 0, 1000 )
		self.h47g = TH1F( 'h47g', 'h47g',100, 0, 1000 )
		self.hn20 = TH1F( 'hn20', 'hn20',20, 0, 20 )
		self.h2n20 = TH2F( 'h2n20', 'h2n20',20, 0, 20, 100, 0, 5000 )

		self.hncl = TH1F( 'hncl', 'hncl',20, 0, 20)
		self.hecl = TH1F( 'hecl', 'hecl',100, 0, 1000)
		self.hxy = TH2F( 'hxy', 'hxy',11, 1, 12,11,1,12)
		self.hkcl = TH1F( 'hkcl', 'hkcl',20, 0, 20)

		self.hncl0 = TH1F( 'hncl0', 'hncl0',20, 0, 20)
		self.hecl0 = TH1F( 'hecl0', 'hecl0',100, 0, 1000)
		self.hxy0 = TH2F( 'hxy0', 'hxy0',11, 1, 12,11,1,12)
		self.hkcl0 = TH1F( 'hkcl0', 'hkcl0',20, 0, 20)

		self.hncl1 = TH1F( 'hncl1', 'hncl1',20, 0, 20)
		self.hecl1 = TH1F( 'hecl1', 'hecl1',100, 0, 1000)
		self.hxy1 = TH2F( 'hxy1', 'hxy1',11, 1, 12,11,1,12)
		self.hkcl1 = TH1F( 'hkcl1', 'hkcl1',20, 0, 20)


		self.hxymu = TH2F( 'hxymu', 'hxymu',11, 1, 12,11,1,12)
		self.heclmu = TH1F( 'heclmu', 'heclmu',100, 0, 1000)
		self.hxyhad = TH2F( 'hxyhad', 'hxyhad',11, 1, 12,11,1,12)
		self.heclhad = TH1F( 'heclhad', 'heclhad',100, 0, 1000)
		self.hxymumu = TH2F( 'hxymumu', 'hxymumu',11, 1, 12,11,1,12)
		self.heclmumu = TH1F( 'heclmumu', 'heclmumu',100, 0, 1000)

	def Execute(self,event):
		try:
			qdc = event.reco["QDC-2"]
                        polx = event.reco['h2']
                        poly = event.reco['h3']
			
			gda = []
			
			m9 = qdc.moduls[9]
			for a,e in m9:
				if e<96:
					self.h9.Fill(e)
					e2 = divmod(e,24)
					enew = e2[0]*24+23-e2[1]
					gda.append((a,enew))
				
			m8 = qdc.moduls[8]
			for a,e in m8:
				if e<96:
					self.h8.Fill(e)
					e2 = divmod(e,24)
					enew = e2[0]*24+ 23 - e2[1] + 96
					gda.append((a,enew))
			
			sum = 0
			sumc = 0
			mu = 0
			cell = 0
			a36 = 0	
			a46 = 0	
			a45 = 0	
			a47 = 0	

			n20 = 0

			gdam = resize(0,(13,13))

			for a,e in gda:
				self.h.Fill(e)
				ix,iy = divmod(e,12)
				if ix==10:
					iy = iy + 2
					
				if 0<iy<=11 and 0<=ix<11:
					gdam[ix+1,iy] = a				
			
				self.h2.Fill(ix,iy)
				self.h2a.Fill(ix,iy,a)
				if ix == 4:
					if iy == 0:
						mu = a
					if iy == 6:
						cell = a
				if iy>0:
					sum += a
				centr = False
				if 2<ix<6:
					if 4<iy<8:
						sumc += a
						centr = True
				if not centr:
					self.hamp.Fill(a)
				if ix==3 and iy==6:
					a36 = a					
				if ix==4 and iy==6:
					a46 = a					
				if ix==4 and iy==5:
					a45 = a					
				if ix==4 and iy==7:
					a47 = a					
					
				if a>20:
					n20 += 1
					
			self.hmu.Fill(cell,mu) 
			self.hsum.Fill(sum) 
			self.hsumc.Fill(sumc)
			if len(polx.hits)>0 and len(poly.hits)>0:
				self.hsumch.Fill(sumc)
				if mu <50:
					self.hsumch1.Fill(sumc)
				else:
					self.hsumch2.Fill(sumc)
			
			
			
			if a46>0:
				self.h46.Fill(a46)
			if a36>0:
				self.h36.Fill(a36)
				if a46<10:
					self.h36g.Fill(a36)
			if a45>0:
				self.h45.Fill(a45)
				if a46<10:
					self.h45g.Fill(a45)
			if a47>0:
				self.h47.Fill(a47)
				if a46<10:
					self.h47g.Fill(a47)
			self.hn20.Fill(n20)
			self.h2n20.Fill(n20,sum)
			
#			print gdam
			
			cl = []
			for ix in range(1,12):
				for iy in range(1,12):
					if gdam[ix,iy]>20 and gdam[ix-1:ix+2,iy-1:iy+2].max()==gdam[ix,iy]:
						cl.append((ix,iy))
			
#			print cl

			self.hncl.Fill(len(cl))
			if len(polx.hits)==0 and len(poly.hits)==0:
				self.hncl0.Fill(len(cl))
			else:
				self.hncl1.Fill(len(cl))
				
			for c in cl:
				ix = c[0]
				iy = c[1]
				sumcl =  gdam[ix-1:ix+1,iy-1:iy+2].sum()
				self.hecl.Fill(sumcl)			
				self.hxy.Fill(ix,iy)

				kcl = 0
				for jx in range(-1,2):				
					for jy in range(-1,2):
						if gdam[ix+jx,iy+jy]>20:
							kcl += 1				
				self.hkcl.Fill(kcl)
				
				if len(polx.hits)==0 and len(poly.hits)==0:
					self.hecl0.Fill(sumcl)			
					self.hxy0.Fill(ix,iy)
					self.hkcl0.Fill(kcl)
				else:
					self.hecl1.Fill(sumcl)			
					self.hxy1.Fill(ix,iy)
					self.hkcl1.Fill(kcl)

				if kcl<3:
					self.hxymu.Fill(ix,iy)
					self.heclmu.Fill(sumcl)			
				else:
					self.hxyhad.Fill(ix,iy)
					self.heclhad.Fill(sumcl)			

				if mu>50:
					self.hxymumu.Fill(ix,iy)
					self.heclmumu.Fill(sumcl)			
						
				
		except KeyError:
			pass
		
