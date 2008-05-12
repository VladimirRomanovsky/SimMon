from ROOT import TH2F

class ViewDT:

	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("DT")
		self.dir.cd()
		self.hx = TH2F( 'DTGorx', 'DTGorx', 32, 0, 32, 48, 0, 48)
		self.hy = TH2F( 'DTGory', 'DTGory', 32, 0, 32, 48, 0, 48)
		self.hpx = TH2F( 'DTPolx', 'DTPolx', 32, 0, 32, 16, 0, 16)
		self.hpy = TH2F( 'DTPoly', 'DTPoly', 32, 0, 32, 16, 0, 16)

		self.htx = TH2F( 'DTtGorx', 'DTtGorx', 128, 0, 1024, 48, 0, 48)
		self.hty = TH2F( 'DTtGory', 'DTtGory', 128, 0, 1024, 48, 0, 48)
		self.htpx = TH2F( 'DTtPolx', 'DTtGPolx', 128, 0, 1024, 16, 0, 16)
		self.htpy = TH2F( 'DTtPoly', 'DTtPoly', 128, 0, 1024, 16, 0, 16)

		self.h2 = TH2F( 'DT2', 'DT2', 32, 0, 32, 32, 0, 32)
		self.h2t = TH2F( 'DT2t', 'DT2t', 128, 0, 1024, 128, 0, 1024)
		self.h2t1 = TH2F( 'DT2t1', 'DT2t2', 128, 0, 1024, 128, 0, 1024)
		self.h2t2 = TH2F( 'DT2t2', 'DT2t2', 128, 0, 1024, 128, 0, 1024)


		self.hh = []
		
		for i in range(32):
			self.hh.append(TH2F( 'DThh%i'%i, 'DThh%i'%i, 128, 0, 1024, 16, 0, 16))

	def Execute(self,event):
	
		try:
			gorin = event.reco["Gorin"] 
			dt = event.reco["DT"] 
                        polx = event.reco['h2']
                        poly = event.reco['h3']

			for ch,t in dt:
				for x in gorin.x:
					self.hx.Fill(ch,x[0])
					self.htx.Fill(t,x[0])
				
				for y in gorin.y:
					self.hy.Fill(ch,y[0])
					self.hty.Fill(t,y[0])

				for xp in polx.hits:
					self.hpx.Fill(ch,xp)
					self.htpx.Fill(t,xp)

				for yp in poly.hits:
					self.hpy.Fill(ch,yp)
					self.htpy.Fill(t,yp)
					self.hh[ch].Fill(t,yp)



			for ch1,t1 in dt:
				for ch2,t2 in dt:
					if ch1!=ch2 or t1!=t2:
						self.h2.Fill(ch1,ch2)
						self.h2t.Fill(t1,t2)
						if ch1==ch2:
							self.h2t1.Fill(t1,t2)
						else:
							self.h2t2.Fill(t1,t2)
								
		except KeyError:
			pass

