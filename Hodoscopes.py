from ROOT import TH2F,TH3F

class ViewHodoscopes:

	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("Hodoscopes")
		self.dir.cd()
		self.hx1 = TH2F( 'XGorXHal', 'XGorXHal', 48, 0, 48, 16, 0, 16)
		self.hy1 = TH2F( 'YGorYHal', 'YGorYHal', 48, 0, 48, 16, 0, 16)
		self.hx2 = TH2F( 'XGorXPol', 'XGorXPol', 48, 0, 48, 16, 0, 16)
		self.hy2 = TH2F( 'YGorYPol', 'YGorYPol', 48, 0, 48, 16, 0, 16)
		self.hx3 = TH2F( 'XSemXPol', 'XSemXPol', 16, 0, 16, 16, 0, 16)
		self.hy3 = TH2F( 'YSemYPol', 'YSemYPol', 16, 0, 16, 16, 0, 16)

		self.hx = TH3F( 'X3', 'X3', 16, 0, 16, 16, 0, 16, 48, 0, 48)
		self.hy = TH3F( 'Y3', 'Y3', 16, 0, 16, 16, 0, 16, 48, 0, 48)

	def Execute(self,event):
	
		try:
			gorin = event.reco["Gorin"] 
			semx = event.reco['HSemx']
			semy = event.reco['HSemy']

			for g in gorin.x:
				xg = g[0]
				for xs in semx.hits:
					self.hx1.Fill(xg,xs)

			for g in gorin.y:
				yg = g[0]
				for ys in semy.hits:
					self.hy1.Fill(yg,ys)
					
		except KeyError:
			pass

		try:
			gorin = event.reco["Gorin"] 
			polx = event.reco['h3']
			poly = event.reco['h2']

			for g in gorin.x:
				xg = g[0]
				for xp in polx.hits:
					self.hx2.Fill(xg,xp)

			for g in gorin.y:
				yg = g[0]
				for yp in poly.hits:
					self.hy2.Fill(yg,yp)

		except KeyError:
			pass

		
		try:
			semx = event.reco['HSemx']
			semy = event.reco['HSemy']
			polx = event.reco['h3']
			poly = event.reco['h2']

			for xs in semx.hits:
				for xp in polx.hits:
					self.hx3.Fill(xs,xp)

			for ys in semy.hits:
				for yp in poly.hits:
					self.hy3.Fill(ys,yp)


		except KeyError:
			pass
		
		try:
			semx = event.reco['HSemx']
			semy = event.reco['HSemy']
			polx = event.reco['h3']
			poly = event.reco['h2']
			gorin = event.reco["Gorin"] 

			for xs in semx.hits:
				for xp in polx.hits:
					for g in gorin.x:
						self.hx.Fill(xs,xp,g[0])

			for ys in semy.hits:
				for yp in poly.hits:
					for g in gorin.y:
						self.hy.Fill(ys,yp,g[0])


		except KeyError:
			pass
		
