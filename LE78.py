from ROOT import TH1F,TH2F
	
class LE78Error(Exception):

	def __init__(self, value, mod):
		self.value = value
		self.mod = mod

	def __str__(self):
		return repr(self.value)

class LE78:
	def __init__(self,data):
	
		self.data = data
		self.rawmoduls = None
		self.moduls = {}
		self.error=None
		
		
		def _dataprint(data,text=''):
			print "LE76:",text
			for d in data:
				print "0x%4X"%d,
			print 
		
		if len(data)!=data[0]:
			print "LE78:: Error in leng: %i %i "%(len(data),data[0])
			return
			
		rawmoduls = {}
		for i in range(1+3,data[0]/2): # Skip 6 words
			info = data[i*2]
			modul = data[i*2+1]>>6

			if rawmoduls.has_key(modul):
				if modul==curentmodul:
					rawmoduls[modul].append(info)
				else:
					self.error = {"crate":"WrongModulOder"}
					return			
			else:
				curentmodul = modul
				rawmoduls[modul]=[info]

		self.rawmoduls = rawmoduls
#		print "Raw moduls:\n",rawmoduls
				
		nev = None
		fDebug = None
		for i in self.rawmoduls.iterkeys():
			d = self.rawmoduls[i]
			mod = None
			if len(d)!=d[0]+1:
				continue			
			if len(d)<2 or d[1]!=i:
				continue
			if nev:
				if nev!=(d[-1]&0x3FFF):
					print "Error in NEV:",data[1],i,nev,d[-1]&0x3FFF,"%x"%(nev-d[-1]&0x3FFF)
					continue
			else:
				nev = (d[-1]&0x3FFF)
			if d[-1]>>14 != 1:
				continue
			 
			hits=[]
			if d[0]>2:
				for k in d[2:-1]:
					if k>>14 != 0:
						continue
					hits.append((k&0xFF,(k>>8)&0x3F))

#					if (k&0xFF) == i and ((k>>8)&0x3F) == 0:
#						fDebug = i

#			self.moduls[i]=hits
			k = i
			if k>=32:
				k = (k - 32) | 16
			self.moduls[k]=hits
#		print "Moduls:\n",self.moduls

		if fDebug:
			print "ERRor in Modul %d"%fDebug
			for i in self.rawmoduls.iterkeys():
				print "Modul %i"%i
				d = self.rawmoduls[i]
				for k in d:
					print "0x%04X"%k


class DecodeLE78:
	" Decode LE78 from OKA2006 DATA"

	
	def __init__(self,cr):
		self.cr = cr
		
	def Execute(self,event):

		try:
			data = event.det[self.cr]         # Detector Number 
			
		except 	KeyError:
			return
		
		event.reco["LE78-%d"%self.cr] = LE78(data)
		
						
class ViewLE78:

	def __init__(self,rootfile,cr):

		self.cr = cr
		
		dir = rootfile.mkdir("LE78-%d"%cr)
		dir.cd()
		self.hl = TH1F( 'len', 'len',1024, 0, 2048 )
		self.hm = TH1F( 'moduls', 'moduls', 32, 0, 32 )
		self.h1={}
		self.h2={}
		self.h3={}
		self.hlen={}
		for i in range(4,24):
			name = "time-%02d"%i
			self.h1[i] = TH1F( name, name, 256, 0, 256 )
			name = "profile-%02d"%i
			self.h2[i] = TH1F( name, name, 64, 0, 64 )
			name = "profile-time-%02d"%i
			self.h3[i] = TH2F( name, name, 256, 0, 256, 64, 0, 64 )
			name = "Leng-%02d"%i
			self.hlen[i] = TH1F( name, name, 100, 0, 100 )
		self.hmod = {}
		for i in range(4,24):
			di = dir.mkdir("MOD-%02d"%i)
			di.cd()
			hlist = []
			for k in range(64):
				hlist.append(TH1F( "Time%02d"%k, "Time%02d"%k, 256, 0, 256 ))
			self.hmod[i] = hlist
			

	def Execute(self,event):
		
		try:
			le78 = event.reco["LE78-%d"%self.cr]
			
		except KeyError:
			return
			
		if le78.moduls == None:
			return

		self.hl.Fill(len(le78.data))

		if le78.moduls:
			moduls = le78.moduls							
			for i in moduls.iterkeys():

				self.hm.Fill(i)
#				print i,le78.moduls[i]

				if i not in range(4,24):
					continue

				m = moduls[i]
				self.hlen[i].Fill(len(m))
				hl = self.hmod[i]
				for t,e in m:
					self.h1[i].Fill(t)
					self.h2[i].Fill(e)
					self.h3[i].Fill(t,e)
					hl[e].Fill(t)
					
