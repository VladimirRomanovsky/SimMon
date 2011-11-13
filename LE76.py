from ROOT import TH1F,TH2F,TH3F

class LE76:
	def __init__(self,data):
	
		self.data = data
		
		if len(data)!=data[0]:
			print "LE76:: Error in leng: %i %i "%(len(data),data[0])
			return
			
		self.reg = {}
#		k = 62 #Added 20 words for 1 Scaler
#		k = 2 + 3*20 + 2*6
		k = 2 + 3*68 + 2*6
#                print "LE76:",
#		for pp in data[k:]:
#			print "%04x"%pp,
#		print " "
		while k+8<=data[0]:
                        
			n = 0
			for e in range(4):
				na = data[k+2*e+1]

				if n==0:
					n = na>>6
					r = []
#					print n
				if na>>6 != n:
					print "LE76 ERROR"
					break
				
				d = data[k+2*e]
				r.append(d)			
				
			if len(r)==4:
				self.reg[n] = r
			else:
				print "LE76 ERROR leng "		
			k += 8
#		print self.reg

class DecodeLE76:
	" Decode LE76 from OKA2007 DATA"

	
	def __init__(self):
		self.cr = 8
		
	def Execute(self,event):

		try:
			data = event.det[self.cr]         # Detector Number 
			
		except 	KeyError:
			return
		
		event.reco["LE76"] = LE76(data)
		
						
class HODOSCOPE:
	" Create Hodoscope from LE76"

	def __init__(self,decode,data):
		self.decode = decode
		
		self.hits = []

		for j,d in enumerate(data):
			for i in range(16):
				k = (d>>i)&0x1
				if k:
					self.hits.append(self.decode[j*16+i])

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

A_decode = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)

class HSTRIP(HODOSCOPE):
	def __init__(self,data):
		HODOSCOPE.__init__(self, A_decode, data)

S_decode = (1,0,3,2,5,4,7,6,9,8,11,10,13,12,15,14)

class H1X(HODOSCOPE):
	def __init__(self,data):
		HODOSCOPE.__init__(self, S_decode, data)

class H1Y(HODOSCOPE):
	def __init__(self,data):
		HODOSCOPE.__init__(self, S_decode, data)

decode3 = range(15,-1,-1) + range(31,15,-1)
class H3Y(HODOSCOPE):
	def __init__(self,data):
		HODOSCOPE.__init__(self, decode3, data)
class H3X(HODOSCOPE):
	def __init__(self,data):
		HODOSCOPE.__init__(self, decode3, data)

G_decode = (0,15,1,14,2,13,3,12,4,11,5,10,6,9,7,8)
G_decode_x2 = (0,1,15,14,2,13,3,12,4,11,5,10,6,9,7,8)
G_decode_per = (0,15,1,4,2,13,3,12,14,11,5,10,6,9,7,8)
decode2x = [i+32 for i in G_decode] + [i+16 for i in G_decode] + [i for i in G_decode]
decode2y = [i for i in G_decode] + [i+16 for i in G_decode] + [i+32 for i in G_decode]

class H2X(HODOSCOPE):
	def __init__(self,data):
		HODOSCOPE.__init__(self, decode2x,data)

class H2Y(HODOSCOPE):
	def __init__(self,data):
		HODOSCOPE.__init__(self, decode2y,data)
		
decode64 = [i for i in A_decode] + [i+16 for i in A_decode] + [i+32 for i in A_decode] + [i+48 for i in A_decode]
class H64(HODOSCOPE):
	def __init__(self,data):
		HODOSCOPE.__init__(self, decode64,data)

class ViewHodos:
	class HodosHist:

		def __init__(self,rootfile,name,length):
			self.dir = rootfile.mkdir("%s"%name)
			self.dir.cd()
			self.hmul = TH1F( '%s mul'%name, '%s mul'%name,16, 0, 16 )
			self.hpro = TH1F( '%s profile'%name, '%s profile'%name, length, 0, length )
			self.h2pro = TH2F( '%s 2profile'%name, '%s 2profile'%name, length, 0, length, length, 0, length )
			self.hdpro = TH1F( '%s delta x'%name, '%s delta'%name, 32, 0, 32 )

			self.hclmul = TH1F( '%s mul cl '%name, '%s mul cl'%name, 16, 0, 16 )
			self.hclpro = TH1F( '%s profile cl '%name, '%s profile cl'%name, 2*length, 0, 2*length )
			self.hcllen = TH1F( '%s len cl '%name, '%s mul cl'%name, 16, 0, 16 )

		def Fill(self,h):	
			self.hmul.Fill(len(h.hits))
			for i in h.hits:
				self.hpro.Fill(i)

			if len(h.hits)==2:
				self.h2pro.Fill(min(h.hits[0],h.hits[1]),max(h.hits[0],h.hits[1]))
				self.hdpro.Fill(abs(h.hits[0]-h.hits[1]))
			
			self.hclmul.Fill(len(h.cls))
			for i in h.cls:
				self.hclpro.Fill(i[0])
				self.hcllen.Fill(i[1])
				
	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("Hodos")
		self.dir.cd()

		self.hr = TH1F( 'LE76', 'LE76',32, 0, 32 )

		self.hists = {}
		self.hists["H1"] = self.HodosHist(self.dir,"H1",16)
		self.hists["H2"] = self.HodosHist(self.dir,"H2",16)
		self.hists["H2X"] = self.HodosHist(self.dir,"H3",48)
		self.hists["H4"] = self.HodosHist(self.dir,"H4",16)
		self.hists["H5"] = self.HodosHist(self.dir,"H5",16)
		self.hists["H2Y"] = self.HodosHist(self.dir,"H6",48)

	def Execute(self,event):
		
		hodos = {}
		
		try:
			le76 = event.reco["LE76"]
			
		except 	KeyError:
			return
		
		self.hr.Fill(0)
		for i in le76.reg.keys():
			self.hr.Fill(i)
		
		try:
			reg = le76.reg[1]
		except KeyError:
			pass
		else:
			hodos["H1"] = H64(reg[0:4])

		try:
			reg = le76.reg[2]
		except KeyError:
			pass
		else:
			hodos["H2"] = H64(reg[0:4])

		try:
			reg = le76.reg[3]
		except KeyError:
			pass
		else:
			hodos["H2X"] = H2X(reg[0:3])
			event.reco["H2X"] = hodos["H2X"]

		try:
			reg = le76.reg[4]
		except KeyError:
			pass
		else:
			hodos["H4"] = H64(reg[0:4])

		try:
			reg = le76.reg[5]
		except KeyError:
			pass
		else:
			hodos["H5"] = H64(reg[0:4])

		try:
			reg = le76.reg[6]
		except KeyError:
			pass
		else:
			hodos["H2Y"] = H2Y(reg[0:3])
			event.reco["H2Y"] = hodos["H2Y"]

		
		
		# Fill Histos
		
                for h in hodos.keys():
                        self.hists[h].Fill(hodos[h])

		event.reco["HODOS"] = hodos


		
