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
		for i in range(1,data[0]/2):
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
				return			
			if d[1]!=i:
				return
			if nev:
				if nev!=(d[-1]&0x3FFF):
					return
			else:
				nev = (d[-1]&0x3FFF)
			if d[-1]>>14 != 1:
				return
			 
			hits=[]
			if d[0]>2:
				for k in d[2:-1]:
					if k>>14 != 0:
						return
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
			self.h1[i] = TH1F( name, name, 128, 0, 128 )
			name = "profile-%02d"%i
			self.h2[i] = TH1F( name, name, 64, 0, 64 )
			name = "profile-%02d_T"%i
			self.h3[i] = TH1F( name, name, 64, 0, 64 )
			name = "Leng-%02d"%i
			self.hlen[i] = TH1F( name, name, 100, 0, 100 )
		self.hmod = {}
		for i in range(4,24):
			di = dir.mkdir("MOD-%02d"%i)
			di.cd()
			hlist = []
			for k in range(64):
				hlist.append(TH1F( "Time%02d"%k, "Time%02d"%k, 128, 0, 128 ))
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
					if 50<t<100:
						self.h3[i].Fill(e)
					hl[e].Fill(t)
					
decode = ( 0,32, 2,34, 4,36, 6,38, 8,40,10,42,12,44,14,46,
	  16,48,18,50,20,52,22,54,24,56,26,58,28,60,30,62,
	   1,33, 3,35, 5,37, 7,39, 9,41,11,43,13,45,15,47,
	  17,49,19,51,21,53,23,55,25,57,27,59,29,61,31,63)

class ViewPC:


	class PC:
	

		def __init__(self,event,cr,rfirst,rlast):
		
			self.hits = []
		
			try:
				le78 = event.reco["LE78-%2d"%cr]
			
			except KeyError:
				return

			for im in range(rfirst,rlast):
				try:
					m = le78.moduls[im]
				except KeyError:
					continue
			
				for t,e in m:
					ed = decode[e]
					hit = (t,ed+(im-rfirst)*64)
					self.hits.append(hit)
	class HPC:
		def __init__(self,rootfile,size,name):
			self.dir = rootfile.mkdir(name)
			self.dir.cd()
			self.hprofile = TH1F( 'profile %s'%name, 'profile %s'%name, size, 0, size )
			self.htime = TH1F( 'time %s'%name, 'time %s'%name, 128, 0, 128 )
			self.hprofilet = TH1F( 'profileT %s'%name, 'profileT %s'%name, size, 0, size )
			self.hprofilet1 = TH1F( 'profileT1 %s'%name, 'profileT1 %s'%name, size/2, 0, size/2 )
			self.hprofilet2 = TH1F( 'profileT2 %s'%name, 'profileT2 %s'%name, size/2, 0, size/2 )
			
		def Fill(self,pc):
			for t,e in pc.hits:
				self.hprofile.Fill(e)
				self.htime.Fill(t)
				if 60<t<80:
					self.hprofilet.Fill(e)
					ehalf,half = divmod(e,2)
					if half == 0:
						self.hprofilet1.Fill(ehalf)
					else:
						self.hprofilet2.Fill(ehalf)
					
					
								
	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("PC")
		self.dir.cd()
		
		self.hpcy2 = self.HPC(self.dir,64*7,"Y2")
		self.hpcx3 = self.HPC(self.dir,64*10,"X3")
		self.hpcx2 = self.HPC(self.dir,64*10,"X2")

	def Execute(self,event):
		
		pcy2 = self.PC(event,12,4,11)
		self.hpcy2.Fill(pcy2)	
		
		pcx3 = self.PC(event,13,4,14)
		self.hpcx3.Fill(pcx3)	
		
		pcx2 = self.PC(event,13,14,24)
		self.hpcx2.Fill(pcx2)	
