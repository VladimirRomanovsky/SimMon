from ROOT import TH1F,TH2F

class HSem:
	def __init__(self,data):

		self.data = data
		self.bins = []
		self.hits = []
		for i in range(16):
			j = i
			if i%2==0:
				j = j+1
			else:
				j = j-1
				
			k = (data>>i)&0x1
#			self.bins.append(k)
			if k:
				self.hits.append(j)

		self.hits.sort()

		self.cls = []
		
		cl = []
		for h in self.hits:
			if len(cl)==0:
				cl.append(h)
			else:
				if cl[-1]+1 == h:
					cl.append(h)
				else:
					self.cls.append([cl[0]+cl[-1],len(cl)])
					cl = []
		if len(cl)>0:
			self.cls.append([cl[0]+cl[-1],len(cl)])
		
#		print self.hits
#		print self.cls
		
class HGor:
	def __init__(self,data):

		self.data = data
		self.bins = []
		self.hits = []
		j = 0
		for d in data:
			for i in range(16):
				k = (d>>i)&0x1
				self.bins.append(k)
				j += 1
				if k:
					self.hits.append(j)
	
class ViewHodoMISS:

	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("HodoMISS")
		self.dir.cd()
		
		self.hSmulx = TH1F( 'S mul x', 'S mul x',16, 0, 16 )
		self.hSprox = TH1F( 'S profile x', 'S profile x', 16, 0, 16 )
		self.hS2prox = TH2F( 'S 2profile x', 'S 2profile x', 16, 0, 16, 16, 0, 16 )
		self.hSdprox = TH1F( 'S delta x', 'S delta x', 16, 0, 16 )

		self.hSclmulx = TH1F( 'S mul cl x', 'S mul cl x',16, 0, 16 )
		self.hSclprox = TH1F( 'S profile cl x', 'S profile cl x', 32, 0, 32 )
		self.hScllenx = TH1F( 'S len cl x', 'S mul cl x',16, 0, 16 )


		self.hSmuly = TH1F( 'S mul y', 'S mul y',16, 0, 16 )		
		self.hSproy = TH1F( 'S profile y', 'S profile y', 16, 0, 16 )		
		self.hS2proy = TH2F( 'S 2profile y', 'S 2profile y', 16, 0, 16, 16, 0, 16 )		
		self.hSdproy = TH1F( 'S delta y', 'S delta y', 16, 0, 16 )		

		self.hSclmuly = TH1F( 'S mul cl y', 'S mul cl y',16, 0, 16 )
		self.hSclproy = TH1F( 'S profile cl y', 'S profile cl y', 32, 0, 32 )
		self.hSclleny = TH1F( 'S len cl y', 'S mul cl y',16, 0, 16 )


		self.hGmul = TH1F( 'G mul', 'G mul',16, 0, 16 )
		self.hGpro = TH1F( 'G profile', 'G profile', 32, 0, 32 )
		self.hG2pro = TH2F( 'G 2profile', 'G 2profile', 32, 0, 32, 32, 0, 32 )
		self.hGdpro = TH1F( 'G delta x', 'G delta', 32, 0, 32 )
		
		
			
	def Execute(self,event):
		
		try:
			data = event.det[8]

			if len(data) != data[0]:
				print " HodoMISS: Error leng"
				return

			if data[0]==2: # DATA Empty 
				return
				
#			print data
#			return
			
			k = 2

			self.reg = {}
			
			while k+8<=data[0]:

				n = 0
				for e in range(4):
					na = data[k+2*e+1]

					if n==0:
						n = na>>6
						r = []
					if na>>6 != n:
						break
					
					d = data[k+2*e]
					r.append(d)			
					
				self.reg[n] = r					
				k += 8
				
#			print self.reg
			
			if self.reg[6]:
			
				reg6 = self.reg[6]

				hx = HSem(reg6[0])
				
				event.reco['HSemx'] = hx
				
				self.hSmulx.Fill(len(hx.hits))
				for i in hx.hits:
					self.hSprox.Fill(i)

				if len(hx.hits)==2:
					self.hS2prox.Fill(min(hx.hits[0],hx.hits[1]),max(hx.hits[0],hx.hits[1]))
					self.hSdprox.Fill(abs(hx.hits[0]-hx.hits[1]))

				self.hSclmulx.Fill(len(hx.cls))
				for i in hx.cls:
					self.hSclprox.Fill(i[0])
					self.hScllenx.Fill(i[1])



				hy = HSem(reg6[1])

				event.reco['HSemy'] = hy

				self.hSmuly.Fill(len(hy.hits))
				for i in hy.hits:
					self.hSproy.Fill(i)

				if len(hy.hits)==2:
					self.hS2proy.Fill(min(hy.hits[0],hy.hits[1]),max(hy.hits[0],hy.hits[1]))
					self.hSdproy.Fill(abs(hy.hits[0]-hy.hits[1]))

				self.hSclmuly.Fill(len(hy.cls))
				for i in hy.cls:
					self.hSclproy.Fill(i[0])
					self.hSclleny.Fill(i[1])


			if self.reg[3]:

				reg3 = self.reg[3]
				
				hg = HGor(reg3[0:2])
				self.hGmul.Fill(len(hg.hits))
				for i in hg.hits:
					self.hGpro.Fill(i)

				if len(hg.hits)==2:
					self.hG2pro.Fill(min(hg.hits[0],hg.hits[1]),max(hg.hits[0],hg.hits[1]))
					self.hGdpro.Fill(abs(hg.hits[0]-hg.hits[1]))

									
		except 	KeyError:
			pass
