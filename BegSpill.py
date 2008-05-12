from ROOT import TH1F, TH2F

from BGD import gbgd	
from SG import gsg	
		
class BegSpill:

	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("BegSpill")
		self.dir.cd()
		
		self.hmean = TH2F( "BGD_PED_mean", "BGD_PED_mean" ,39, 1, 40, 32, 1, 33) 
		self.hsigma = TH2F( "BGD_PED_sigma", "BGD_PED_sigma" ,39, 1, 40, 32, 1, 33) 

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
			
		self.sgfile = open("sg.ped","w")


	def Execute(self,event):
		
#		print "Begin of SPILL"
		
		det = event.det
		if len(det)==0:
			return
		sg = {}
			
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

				mean,sigma = data[k:k+2]
				hped[m].SetBinContent(e+1,mean)
				hsig[m].SetBinContent(e+1,sigma)
				k += 2
				
				if d == 2 and m in (5,6) and e<96:
					x,e1 = divmod(e,24)
					enew = 96 *(m-5) + x*24 + (23-e1)
					sg[enew]=(mean,sigma)


				try:
					x,y = gbgd.QDC2BGD(d,m,e)
				except KeyError:
					continue
				
				self.hmean.SetBinContent(x,y,mean)
				self.hsigma.SetBinContent(x,y,sigma)

		for i in sg.keys():
#			print i,sg[i][0],sg[i][1]	
			self.sgfile.write("%i %i %i\n"%(i,sg[i][0],sg[i][1]))
		self.sgfile.flush()
