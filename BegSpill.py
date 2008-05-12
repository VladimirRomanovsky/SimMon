from ROOT import TH1F
	
		
class BegSpill:

	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("BegSpill")
		self.dir.cd()
		
		self.hped = []
		self.hsig = []
		for i in (0,1,2,3):
			crdir = self.dir.mkdir("Crate_%i"%i)
			crdir.cd()
			hp = []
			hs = []
			for k in range(10):
				hp.append( TH1F( 'PED_modul_%i'%k, 'PED_modul_%i'%k, 96, 0, 96))
				hs.append( TH1F( 'SIG_modul_%i'%k, 'SIG_modul_%i'%k, 96, 0, 96))
			self.hped.append(hp)
			self.hsig.append(hs)

	def Execute(self,event):
		
#		print "Begin of SPILL"
		
		det = event.det
		if len(det)==0:
			return
			
		for d in det.iterkeys():
			if d not in (0,1,2,3):
				return 
			
			data = det[d]

			if len(data) != data[0]:
				return

#			print d,len(data),data[0:8]
			
				
			leng = data[0]
			crate = data[1]
			if crate != d:
				print "BegSpill: error in crate number %i: %i"%(d,crate) 
				continue

			mods = []
			for i in data[2:8]:
				w1 = i&0xFF
				w2 = (i>>8)&0xFF
				mods.append(w1) 
				mods.append(w2)

#			print mods

			firstmod = mods[1]
			
			hped = self.hped[crate]
			hsig = self.hsig[crate]
			
			k = 8
			for i in range((leng-8)/2):

				m,e = divmod(i,96)	
				m += firstmod
				
				hped[m].SetBinContent(e+1,data[k])
				hsig[m].SetBinContent(e+1,data[k+1])
				k += 2
					
#		import sys
#		sys.exit()		
