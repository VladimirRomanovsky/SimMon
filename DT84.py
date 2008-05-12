
class DT84:

	def __init__(self,event,modul):

		self.decode = ((4,2,5,1,6,0,7,3),(3,7,0,6,1,5,2,4),(4,2,5,1,6,0,7,3),(4,2,5,1,6,0,7,3))
		self.chanels = {}
		self.pls = {0:[],1:[],2:[],3:[]}
		
		try:
			le84 = event.reco["LE84"]
			
		except 	KeyError:
			return
			
		moduls = le84.moduls
		
		try:
			mod = moduls[modul]
			
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

		t0 = 650 - t0
		
		for ch,time in tdc1:
			self.chanels.setdefault(ch,[]).append(time+t0)


		for ch in self.chanels.iterkeys():
			g,e = divmod(ch,16)
			e,b = divmod(e,2)
			pl = g+b*2
			for t in self.chanels[ch]:
				self.pls[pl].append((t,self.decode[pl][e]))
			

from ROOT import TH1F,TH2F

class ViewDT84:

	class HDT:
		def __init__(self,rootfile,name):

			self.dir = rootfile.mkdir(name)
			self.dir.cd()

			self.hch = TH1F( 'ch %s'%name, 'ch %s'%name, 32, 0, 32 )
			self.htime = TH1F( 'time %s'%name, 'time %s'%name, 1000, 0, 1000 )
			
			self.hpls = []
			self.hpls.append(TH1F( 'pl0', 'pl0', 8, 0, 8 ))
			self.hpls.append(TH1F( 'pl1', 'pl1', 8, 0, 8 ))
			self.hpls.append(TH1F( 'pl2', 'pl2', 8, 0, 8 ))
			self.hpls.append(TH1F( 'pl3', 'pl3', 8, 0, 8 ))

			self.hplst = []
			self.hplst.append(TH1F( 'plt0', 'plt0', 1000, 0, 1000 ))
			self.hplst.append(TH1F( 'plt1', 'plt1', 1000, 0, 1000 ))
			self.hplst.append(TH1F( 'plt2', 'plt2', 1000, 0, 1000 ))
			self.hplst.append(TH1F( 'plt3', 'plt3', 1000, 0, 1000 ))

			self.htt = TH2F( 'tt', 'tt', 100, 0, 1000, 100, 0, 1000 )

			self.hchch = TH2F( 'chch', 'chch', 32, 0, 32, 32, 0, 32 )

			self.ht0t1 = TH2F( 't0t1', 't0t1', 100, 0, 1000, 100, 0, 1000 )
			self.ht0t2 = TH2F( 't0t2', 't0t2', 100, 0, 1000, 100, 0, 1000 )
			self.ht0t3 = TH2F( 't0t3', 't0t3', 100, 0, 1000, 100, 0, 1000 )
			self.ht1t2 = TH2F( 't1t2', 't1t2', 100, 0, 1000, 100, 0, 1000 )
			self.ht1t3 = TH2F( 't1t3', 't1t3', 100, 0, 1000, 100, 0, 1000 )
			self.ht2t3 = TH2F( 't2t3', 't2t3', 100, 0, 1000, 100, 0, 1000 )

			self.he0e1 = TH2F( 'e0e1', 'e0e1', 8, 0, 8, 8, 0, 8 )
			self.he0e2 = TH2F( 'e0e2', 'e0e2', 8, 0, 8, 8, 0, 8 )
			self.he0e3 = TH2F( 'e0e3', 'e0e3', 8, 0, 8, 8, 0, 8 )
			self.he1e2 = TH2F( 'e1e2', 'e1e2', 8, 0, 8, 8, 0, 8 )
			self.he1e3 = TH2F( 'e1e3', 'e1e3', 8, 0, 8, 8, 0, 8 )
			self.he2e3 = TH2F( 'e2e3', 'e2e3', 8, 0, 8, 8, 0, 8 )

		def Fill(self,dt):
			
			for ch in dt.chanels:
				self.hch.Fill(ch)
				for t in dt.chanels[ch]:
					self.htime.Fill(t)

			for ch1 in dt.chanels:
				for ch2 in dt.chanels:
					if ch1 == ch2:
						continue
						
					for t1 in dt.chanels[ch1]:
						for t2 in dt.chanels[ch2]:
							self.htt.Fill(t1,t2)
							self.hchch.Fill(ch1,ch2)
			

			for pl in dt.pls:
				for t,e in dt.pls[pl]:
					self.hpls[pl].Fill(e)
					self.hplst[pl].Fill(t)
				
			for t1,e1 in dt.pls[0]:
				for t2,e2 in dt.pls[1]:
					self.he0e1.Fill(e1,e2)
					self.ht0t1.Fill(t1,t2)

			for t1,e1 in dt.pls[0]:
				for t2,e2 in dt.pls[2]:
					self.he0e2.Fill(e1,e2)
					self.ht0t2.Fill(t1,t2)
					
			for t1,e1 in dt.pls[0]:
				for t2,e2 in dt.pls[3]:
					self.he0e3.Fill(e1,e2)
					self.ht0t3.Fill(t1,t2)

			for t1,e1 in dt.pls[1]:
				for t2,e2 in dt.pls[2]:
					self.he1e2.Fill(e1,e2)
					self.ht1t2.Fill(t1,t2)

			for t1,e1 in dt.pls[1]:
				for t2,e2 in dt.pls[3]:
					self.he1e3.Fill(e1,e2)
					self.ht1t3.Fill(t1,t2)

			for t1,e1 in dt.pls[2]:
				for t2,e2 in dt.pls[3]:
					self.he2e3.Fill(e1,e2)
					self.ht2t3.Fill(t1,t2)

	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("DT84")
		self.dir.cd()

		self.hdtx = self.HDT(self.dir,"DTX")
		self.hdty = self.HDT(self.dir,"DTY")
		
	def Execute(self,event):
		
		dtx = DT84(event,11)
		dty = DT84(event,10)

		self.hdtx.Fill(dtx)	
		self.hdty.Fill(dty)	
