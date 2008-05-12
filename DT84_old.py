
from ROOT import TH1F,TH2F

class ViewDT84:

	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("DT84")
		self.dir.cd()

		self.hch = TH1F( 'hch', 'hch', 32, 0, 32 )

		self.htime0 = TH1F( 'htime0', 'htime0', 1000, 0, 1000 )
		self.htime = TH1F( 'htime', 'htime', 1000, 0, 1000 )
		self.htimec = TH1F( 'htimec', 'htimec', 1000, 0, 1000 )
		self.htt = TH2F( 'htt', 'htt', 100, 0, 1000, 100, 0, 1000 )
		self.hdt = TH1F( 'hdt', 'hdt', 1000, -1000, 1000 )
		self.hst = TH1F( 'hst', 'hst', 1000, 0, 1000 )
		self.hchch = TH2F( 'hchch', 'hchch', 32, 0, 32, 32, 0, 32 )
		self.hchcht = TH2F( 'hchcht', 'hchcht', 32, 0, 32, 32, 0, 32 )

		self.hpls = {}
		self.hpls[0] = TH1F( 'hpl0', 'hpl0', 8, 0, 8 )
		self.hpls[1] = TH1F( 'hpl1', 'hpl1', 8, 0, 8 )
		self.hpls[2] = TH1F( 'hpl2', 'hpl2', 8, 0, 8 )
		self.hpls[3] = TH1F( 'hpl3', 'hpl3', 8, 0, 8 )

		self.hpl1pl2 = TH2F( 'hpl1pl2', 'hpl1pl2', 8, 0, 8, 8, 0, 8 )
		self.ht1t2 = TH2F( 'ht1t2', 'ht1t2', 100, 0, 1000, 100, 0, 1000 )

	def Execute(self,event):
		
		try:
			le84 = event.reco["LE84"]
			
		except 	KeyError:
			return
			
		moduls = le84.moduls
		
		try:
			mod = moduls[9]
			
		except 	KeyError:
			return
			
		tdc1 = mod[0]
		tdc2 = mod[1]

		n0 = 0
		for ch,time in tdc2:
			if ch == 30:
				n0 += 1
				t0 = time
		
		if n0 != 1:
			return

		self.htime0.Fill(t0)
		t0 = 650 - t0
		
		chanels = {}
		
		for ch,time in tdc1:
			self.hch.Fill(ch)
			self.htime.Fill(time)
			self.htimec.Fill(time+t0)			
			
			chanels.setdefault(ch,[]).append(time+t0)
			
		for ch1 in chanels.iterkeys():
			for ch2 in chanels.iterkeys():
				if ch1 == ch2:
					continue
					
				
				for t1 in chanels[ch1]:
					for t2 in chanels[ch2]:
						self.htt.Fill(t1,t2)
						self.hchch.Fill(ch1,ch2)	
						if abs(t1-t2) <100:
							self.hchcht.Fill(ch1,ch2)
						self.hdt.Fill(t1-t2)
						self.hst.Fill((t1+t2)/2.)
		 		

		self.decode = ((4,2,5,1,6,0,7,3),(4,2,5,1,6,0,7,3),(4,2,5,1,6,0,7,3),(4,2,5,1,6,0,7,3))

		pls = {0:[],1:[],2:[],3:[]}
		for ch in chanels.iterkeys():
			g,e = divmod(ch,16)
			e,b = divmod(e,2)
			pl = g+b*2
			for t in chanels[ch]:
				pls[pl].append((t,self.decode[pl][e]))

		for pl in pls:
			for t,e in pls[pl]:
				self.hpls[pl].Fill(e)

			for t1,e1 in pls[1]:
				for t2,e2 in pls[2]:
					self.hpl1pl2.Fill(e1,e2)
					self.ht1t2.Fill(t1,t2)
