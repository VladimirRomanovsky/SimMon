

from ROOT import TH1F,TH2F

class ViewNIM84:


	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("NIM84")
		self.dir.cd()

		self.htimeR = TH1F( 'timeR', 'timeR', 1000, 0, 1000 )
		self.htime0 = TH1F( 'time0', 'time0', 1000, 0, 1000 )
		self.htime2 = TH1F( 'time2', 'time2', 1000, 0, 1000 )
		self.hdtime0 = TH1F( 'dtime0', 'dtime0', 1000, 0, 1000 )
		self.hdtime2 = TH1F( 'dtime2', 'dtime2', 1000, 0, 1000 )

		
	def Execute(self,event):
		
		try:
			le84 = event.reco["LE84"]
			
		except 	KeyError:
			return
			
		moduls = le84.moduls
		try:
			mod = moduls[5]
			
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

		self.htimeR.Fill(t0)

		t0 = 650 - t0
		
		for ch,time in tdc1:
			if ch == 0:
				self.htime0.Fill(time)
				self.hdtime0.Fill(time+t0)

			if ch == 2:
				self.htime2.Fill(time)
				self.hdtime2.Fill(time+t0)

