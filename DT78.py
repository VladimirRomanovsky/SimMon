from ROOT import TH1F,TH2F,TH3F

DT78_decode = ((4,2,5,1,6,0,7,3),(3,7,0,6,1,5,2,4),(4,2,5,1,6,0,7,3),(3,7,0,6,1,5,2,4))

class DT78:
	def __init__(self,event,modul):
		
		self.event = event	
		self.pls = {0:[],1:[],2:[],3:[]}
		
		try:
			le78 = event.reco["LE78-10"]
		except KeyError:
			return
		try:
			mod = le78.moduls[modul]
		except KeyError:
			return
		
		for t,e in mod:
			k2,k16 = divmod(e,16)
			
			e8,k1 = divmod(k16,2)
			g = (1-k2) + k1*2
			
			if g not in (0,1,2,3):
				continue
			
			self.pls[g].append( (t,DT78_decode[g][e8]))


class ViewDT78:

	class HDT78:

		def __init__(self,rootfile,name):
		
			self.dir = rootfile.mkdir(name)
			self.dir.cd()
			
			self.h = []
			self.ht = []
			self.hn = []
			
			for i in range(4):
				self.h.append(TH1F( 'h_%i'%i, 'h_%i'%i,8, 0, 8 ))
				self.ht.append(TH1F( 'h_t%i'%i, 'ht%i'%i,128, 0, 128 ))
				self.hn.append(TH1F( 'h_n%i'%i, 'hn%i'%i, 8, 0,  8 ))

			self.htt = TH2F( 'htt', 'htt',128, 0, 128 ,128, 0, 128 )
			self.hdt = TH1F( 'hdt', 'hdt',256, -128, 128 )
			self.hst = TH1F( 'hst', 'hst',128, 0, 128 )

			self.ht0t1 = TH2F( 'ht0t1', 'ht0t1',128, 0, 128 ,128, 0, 128 )
			self.ht0t2 = TH2F( 'ht0t2', 'ht0t2',128, 0, 128 ,128, 0, 128 )
			self.ht0t3 = TH2F( 'ht0t3', 'ht0t3',128, 0, 128 ,128, 0, 128 )
			self.ht1t2 = TH2F( 'ht1t2', 'ht1t2',128, 0, 128 ,128, 0, 128 )
			self.ht1t3 = TH2F( 'ht1t3', 'ht1t3',128, 0, 128 ,128, 0, 128 )
			self.ht2t3 = TH2F( 'ht2t3', 'ht2t3',128, 0, 128 ,128, 0, 128 )

			self.h01 = TH2F( 'h01', 'h01', 8, 0, 8 , 8, 0, 8 )
			self.h02 = TH2F( 'h02', 'h02', 8, 0, 8 , 8, 0, 8 )
			self.h03 = TH2F( 'h03', 'h03', 8, 0, 8 , 8, 0, 8 )
			self.h12 = TH2F( 'h12', 'h12', 8, 0, 8 , 8, 0, 8 )
			self.h13 = TH2F( 'h13', 'h13', 8, 0, 8 , 8, 0, 8 )
			self.h23 = TH2F( 'h23', 'h23', 8, 0, 8 , 8, 0, 8 )

			self.hdt02 = TH1F( 'hdt02', 'hdt02',256, -128, 128 )
			self.hst01 = TH1F( 'hst01', 'hst01',128, 0, 128 )
			self.hst12 = TH1F( 'hst12', 'hst12',128, 0, 128 )

			self.hwt = {}
			self.hwn = {}

			for i in range(4):
				tdir = self.dir.mkdir("w%i"%i)
				tdir.cd()
			
				hwt = []
				hwn = []
				for k in range(8):
					hwt.append(TH1F( 'h_wdt%i'%k, 'hwt%i'%k,128, 0, 128 ))
					hwn.append(TH1F( 'h_wn%i'%k, 'hwn%i'%k, 8, 0,  8 ))
				
				self.hwt[i] = hwt
				self.hwn[i] = hwn

			tdir = self.dir.mkdir("HOD")
			tdir.cd()
			
			self.hX = []
			self.hY = []
			for i in range(4):
				self.hX.append(TH2F( 'hX_%i'%i, 'h_%i'%i,8, 0, 8, 48, 0, 48 ))
				self.hY.append(TH2F( 'hY_%i'%i, 'h_%i'%i,8, 0, 8, 48, 0, 48 ))


		def Fill(self,dt):
		
			for i in dt.pls:
				self.hn[i].Fill(len(dt.pls[i]))
				for t,e in dt.pls[i]:
					self.h[i].Fill(e)
					self.ht[i].Fill(t)
			
			for i1 in dt.pls:
				for i2 in dt.pls:
					if i1 == i2:
						continue
						
					for t1,e1 in dt.pls[i1]:
						for t2,e2 in dt.pls[i2]:
							self.htt.Fill(t1,t2)
							self.hdt.Fill(t1-t2)
							self.hst.Fill((t1+t2)/2)


			for t1,e1 in dt.pls[0]:
				for t2,e2 in dt.pls[1]:
					self.ht0t1.Fill(t1,t2)
					self.h01.Fill(e1,e2)
			for t1,e1 in dt.pls[0]:
				for t2,e2 in dt.pls[2]:
					self.ht0t2.Fill(t1,t2)
					self.h02.Fill(e1,e2)
			for t1,e1 in dt.pls[0]:
				for t2,e2 in dt.pls[3]:
					self.ht0t3.Fill(t1,t2)
					self.h03.Fill(e1,e2)
			for t1,e1 in dt.pls[1]:
				for t2,e2 in dt.pls[2]:
					self.ht1t2.Fill(t1,t2)
					self.h12.Fill(e1,e2)
			for t1,e1 in dt.pls[1]:
				for t2,e2 in dt.pls[3]:
					self.ht1t3.Fill(t1,t2)
					self.h13.Fill(e1,e2)
			for t1,e1 in dt.pls[2]:
				for t2,e2 in dt.pls[3]:
					self.ht2t3.Fill(t1,t2)
					self.h23.Fill(e1,e2)

			for t1,e1 in dt.pls[0]:
				for t2,e2 in dt.pls[2]:
					self.hdt02.Fill(t1-t2)

			for t1,e1 in dt.pls[0]:
				for t2,e2 in dt.pls[1]:
					self.hst01.Fill((t1+t2)/2)

			for t1,e1 in dt.pls[1]:
				for t2,e2 in dt.pls[2]:
					self.hst12.Fill((t1+t2)/2)

			for i in dt.pls:
				ws = {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[]}
				for t,e in dt.pls[i]:
					ws[e].append(t)
				for k in ws.iterkeys():
					self.hwn[i][k].Fill(len(ws[k]))
					if len(ws[k]) >1:
						for l in range(1,len(ws[k])):
							self.hwt[i][k].Fill(ws[k][l]-ws[k][l-1])        	       


			try:
				hodos = dt.event.reco["HODOS"]

			except  KeyError:
				return
					
			try:
				h1x = hodos["H2X"]
			except KeyError:
				pass
			else:
				for h in h1x.hits:
					for i in dt.pls:
						for t,e in dt.pls[i]:
							self.hX[i].Fill(e,h)
			
			try:
				h1y = hodos["H2Y"]
			except KeyError:
				pass
			else:
				for h in h1y.hits:
					for i in dt.pls:
						for t,e in dt.pls[i]:
							self.hY[i].Fill(e,h)
			

			
	def __init__(self,rootfile):

		
		self.dir = rootfile.mkdir("DT78")
		self.dir.cd()
		
		self.hdtx = self.HDT78(self.dir,"DTX")
		self.hdty = self.HDT78(self.dir,"DTY")
		
	def Execute(self,event):

		dtx = DT78(event,8)
		dty = DT78(event,7)
		

		self.hdtx.Fill(dtx)
		self.hdty.Fill(dty)
		
		
		
