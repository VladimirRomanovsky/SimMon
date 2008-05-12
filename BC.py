from ROOT import TH1F,TH2F,TH3F

peak = {18:[40,50,60],19:[50,66,76],20:[40,47,55],21:[50,60,70],22:[37,43,50],23:[55,63,73]}


class HistModul:
	def __init__(self,mod):
		self.hm = TH1F( 'hm'+mod, 'hm'+mod, 10, 0, 10)
		self.hi = TH1F( 'hi'+mod, 'hi+mod', 64, 0, 64)
		self.ht = TH1F( 'ht'+mod, 'ht'+mod, 128, 0, 128)
		self.hit = TH2F( 'hit'+mod, 'hit'+mod, 64, 0, 64, 128, 0, 128)
		self.hdi = TH1F( 'hdi'+mod, 'hdi'+mod, 64, 0, 64)
		self.hdt = TH1F( 'hdt'+mod, 'hdt'+mod, 100, -50, 50)
		self.hdidt = TH2F( 'hdidt'+mod, 'hdidt'+mod, 128, -64, 64, 100, -50, 50)
		self.htt = TH2F( 'htt'+mod, 'htt'+mod, 128, 0, 128, 128, 0, 128)
		self.hii = TH2F( 'hii'+mod, 'hii'+mod, 64, 0, 64, 64, 0, 64)

class HistModul1:
	def __init__(self,mod):
		self.ht = TH1F( 'ht'+mod, 'ht'+mod, 128, 0, 128)

class HistModul2:
	def __init__(self,mod):
		self.ht = TH1F( 'ht'+mod, 'ht'+mod, 128, 0, 128)
		self.htt = TH2F( 'htt'+mod, 'htt'+mod, 128, 0, 128, 128, 0, 128)
		self.ht0 = TH1F( 'ht0'+mod, 'ht0'+mod, 128, 0, 128)
		self.htt0 = TH2F( 'htt0'+mod, 'htt0'+mod, 128, 0, 128, 128, 0, 128)
		self.ht1 = TH1F( 'ht1'+mod, 'ht1'+mod, 128, 0, 128)
		self.htt1 = TH2F( 'htt1'+mod, 'htt1'+mod, 128, 0, 128, 128, 0, 128)
		self.ht2 = TH1F( 'ht2'+mod, 'ht2'+mod, 128, 0, 128)
		self.htt2 = TH2F( 'htt2'+mod, 'htt2'+mod, 128, 0, 128, 128, 0, 128)
		self.ht3 = TH1F( 'ht3'+mod, 'ht3'+mod, 128, 0, 128)
		self.htt3 = TH2F( 'htt3'+mod, 'htt3'+mod, 128, 0, 128, 128, 0, 128)

class HistModul3:
	def __init__(self,mod):
		self.hi = TH1F( 'hi'+mod, 'hi+mod', 64, 0, 64)
		self.ht = TH1F( 'ht'+mod, 'ht'+mod, 128, 0, 128)
		self.hdi = TH1F( 'hdi'+mod, 'hdi'+mod, 64, 0, 64)
		self.hdt = TH1F( 'hdt'+mod, 'hdt'+mod, 100, -50, 50)
		self.hdidt = TH2F( 'hdidt'+mod, 'hdidt'+mod, 128, -64, 64, 100, -50, 50)
		self.h3 = TH3F( 'h3'+mod, 'h3'+mod, 64, 0, 64, 64, 0, 64, 64, 0, 64)
		self.ht0 = TH1F( 'ht0'+mod, 'ht0'+mod, 128, 0, 128)
		self.ht1 = TH1F( 'ht1'+mod, 'ht1'+mod, 128, 0, 128)
		self.hi0 = TH1F( 'hi0'+mod, 'hi0+mod', 64, 0, 64)

class HistModul5:
	def __init__(self,mod):
		self.ht0 = TH1F( 'ht0'+mod, 'ht0+mod', 128, 0, 128)
		self.ht1 = TH1F( 'ht1'+mod, 'ht1+mod', 128, 0, 128)
		self.ht2 = TH1F( 'ht2'+mod, 'ht2+mod', 128, 0, 128)

class HistChamber:
	def __init__(self,ch):
		self.hi = TH1F( 'hi'+ch, 'h'+ch, 192, 0, 192)
		self.hm = TH1F( 'hm'+ch, 'hm'+ch, 16, 0, 16)
		self.hit = TH2F( 'hit'+ch, 'hit'+ch, 192, 0, 192, 128, 0, 128)
	
class ViewBC:

	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("BC")
		self.dir.cd()
		
		self.hists = {}
		self.histsm = {}
		for i in range(18,24):
			self.hists[i] = HistModul("-%d"%i)
			self.histsm[i] = HistModul("-m-%d"%i)

		dirch = self.dir.mkdir("Chamber")
		dirch.cd()
		self.hch1 = HistChamber("-1")
		self.hch2 = HistChamber("-2")
		
		dir1 = self.dir.mkdir("1")
		dir1.cd()
		self.hists1 = {}
		for i in range(18,24):
			self.hists1[i] = HistModul1("-%d"%i)

		dir2 = self.dir.mkdir("2")
		dir2.cd()
		self.hists2 = {}
		for i in range(18,24):
			self.hists2[i] = HistModul2("-%d"%i)

		dir3 = self.dir.mkdir("3")
		dir3.cd()
		self.hists3 = {}
		for i in range(18,24):
			self.hists3[i] = HistModul3("-%d"%i)

		dir5 = self.dir.mkdir("5")
		dir5.cd()
		self.hists5 = {}
		for i in range(18,24):
			self.hists5[i] = HistModul5("-%d"%i)

		dircl = self.dir.mkdir("clusters")
		dircl.cd()
		self.hm1 = TH1F( 'hm1', 'hm1', 16, 0, 16)
		self.hl1 = TH1F( 'hl1', 'hl1', 16, 0, 16)
		self.hm2 = TH1F( 'hm2', 'hm2', 16, 0, 16)
		self.hl2 = TH1F( 'hl2', 'hl2', 16, 0, 16)

		self.dir.cd()
		
	def _clusters(self,chamber):

		cls = []
		for h in chamber:
			cls.append([h,])

		while len(cls)>1:
			change = None
			for i1 in range(len(cls)-1):
				cl1 = cls[i1]
				for i2 in range(i1+1,len(cls)):
					cl2 = cls[i2]
					for h1 in cl1:
						for h2 in cl2:
							if abs(h1[1]-h2[1])<=2:
								change = (i1,i2)
					
					if change:
						break 	
				if change:
					break 	
			if change:
				cl1 = cls[change[0]]
				cl2 = cls[change[1]]
				cls.remove(cl1)
				cls.remove(cl2)
				cls.append(cl1+cl2)
			else:
				break

		return cls
		
	def Execute(self,event):
	
		try:
			bc  = event.reco["LE78-10"].moduls
		except KeyError:
			return
		if not bc:
			return	

		for m in range(18,24):
			mod = bc[m]
			hists = self.hists[m]
			modnew = []
			hists.hm.Fill(len(mod))
			for t,i in mod:
				if m==22 and i==20: continue
				if m==22 and i==47: continue
				if m==23 and i==56: continue
				hists.hi.Fill(i)
				hists.ht.Fill(t)
				hists.hit.Fill(i,t)
				for t1,i1 in mod:
					if m==22 and i1==20: continue
					if m==22 and i1==47: continue
					if m==23 and i1==56: continue
					if i!=i1 or t!=t1:
						hists.hdi.Fill(abs(i-i1))	
						hists.hdt.Fill(abs(t-t1))
						hists.hdidt.Fill(i-i1,t-t1)
						hists.htt.Fill(t,t1)
						hists.hii.Fill(i,i1)
		bcm = {}
		ch1 = []
		ch2 = []
		for m in range(18,24):
			
			mod = bc[m]
			modnew = []
			for t,i in mod:
				if m==22 and i==20: continue
				if m==22 and i==47: continue
				if m==23 and i==56: continue
				k = i
				if i%2==1:
					if i<32:
						k += 31
				else:
					if i>=32:		 	
						k -= 31
				modnew.append((t,k))
				
				if m<=20:
					ch1.append((t,k+(m-18)*64))
				else:
					ch2.append((t,k+(m-21)*64)) 					

			bcm[m] = modnew
					
		for m in range(18,24):
			mod = bcm[m]
			hists = self.histsm[m]
			hists.hm.Fill(len(mod))
			for t,i in mod:
				hists.hi.Fill(i)
				hists.ht.Fill(t)
				hists.hit.Fill(i,t)
				for t1,i1 in mod:
					if i!=i1 or t!=t1:
						hists.hdi.Fill(abs(i-i1))	
						hists.hdt.Fill(abs(t-t1))
						hists.hdidt.Fill(i-i1,t-t1)
						hists.htt.Fill(t,t1)
						hists.hii.Fill(i,i1)
		hch = self.hch1
		hch.hm.Fill(len(ch1))
		for t,i in ch1:
			hch.hi.Fill(i)
			hch.hit.Fill(i,t)

		hch = self.hch2
		hch.hm.Fill(len(ch2))
		for t,i in ch2:
			hch.hi.Fill(i)
			hch.hit.Fill(i,t)


		if len(ch1)==3:
			for m in range(18,21):
				mod = bcm[m]
				if len(mod)==3:
					hists=self.hists3[m]
					hists.h3.Fill(mod[0][1],mod[1][1],mod[2][1])
					rv = []
					for t,i in mod:
						hists.hi.Fill(i)
						hists.ht.Fill(t)
						for t1,i1 in mod:
							if i!=i1 or t!=t1:
								hists.hdi.Fill(abs(i-i1))	
								hists.hdt.Fill(abs(t-t1))
								hists.hdidt.Fill(i-i1,t-t1)
						rv.append((i,t))
					rv.sort()
					if rv[2][0]-rv[0][0]==2:
						hists.hi0.Fill(rv[0][0])
						hists.ht0.Fill(rv[1][1])
						hists.ht1.Fill(rv[0][1])
						hists.ht1.Fill(rv[2][1])
		if len(ch2)==3:
			for m in range(21,24):
				mod = bcm[m]
				if len(mod)==3:
					hists=self.hists3[m]
					hists.h3.Fill(mod[0][1],mod[1][1],mod[2][1])
					rv = []
					for t,i in mod:
						hists.hi.Fill(i)
						hists.ht.Fill(t)
						for t1,i1 in mod:
							if i!=i1 or t!=t1:
								hists.hdi.Fill(abs(i-i1))	
								hists.hdt.Fill(abs(t-t1))
								hists.hdidt.Fill(i-i1,t-t1)
						rv.append((i,t))
					rv.sort()
					if rv[2][0]-rv[0][0]==2:
						hists.hi0.Fill(rv[0][0])
						hists.ht0.Fill(rv[1][1])
						hists.ht1.Fill(rv[0][1])
						hists.ht1.Fill(rv[2][1])

		cls1 = self._clusters(ch1)
		cls2 = self._clusters(ch2)
				
		self.hm1.Fill(len(cls1))
		for cl in cls1:
			self.hl1.Fill(len(cl))

		self.hm2.Fill(len(cls2))
		for cl in cls2:
			self.hl2.Fill(len(cl))
			

		for m in range(18,24):
			mod = bcm[m]
			if len(mod)==5:
				rv = []
				for t,i in mod:
					rv.append((i,t))
				rv.sort()
				if rv[2][0]-rv[0][0]==4:
					hists=self.hists5[m]
					hists.ht0.Fill(rv[2][1])
					hists.ht1.Fill(rv[1][1])
					hists.ht1.Fill(rv[3][1])
					hists.ht2.Fill(rv[0][1])
					hists.ht2.Fill(rv[4][1])
		
		for m in range(18,24):
			mod = bcm[m]
			if len(mod)==1:
				hists=self.hists1[m]
				hists.ht.Fill(mod[0][0])
		
		for m in range(18,24):
			mod = bcm[m]
			if len(mod)==2:
				hists=self.hists2[m]
				h1 = mod[0]
				h2 = mod[1]
				hists.ht.Fill(h1[0])
				hists.ht.Fill(h2[0])
		
				hists.htt.Fill(h1[0],h2[0])
				hists.htt.Fill(h2[0],h1[0])
				
				di = abs(h1[1]-h2[1])
				if di==1:
					hists.ht0.Fill(h1[0])
					hists.ht0.Fill(h2[0])
		
					hists.htt0.Fill(h1[0],h2[0])
					hists.htt0.Fill(h2[0],h1[0])
				if di==2:
					hists.ht1.Fill(h1[0])
					hists.ht1.Fill(h2[0])
		
					hists.htt1.Fill(h1[0],h2[0])
					hists.htt1.Fill(h2[0],h1[0])
				if di==3:						
					hists.ht2.Fill(h1[0])
					hists.ht2.Fill(h2[0])
		
					hists.htt2.Fill(h1[0],h2[0])
					hists.htt2.Fill(h2[0],h1[0])
				if di>3:						
					hists.ht3.Fill(h1[0])
					hists.ht3.Fill(h2[0])
		
					hists.htt3.Fill(h1[0],h2[0])
					hists.htt3.Fill(h2[0],h1[0])
