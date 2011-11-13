from ROOT import TH1F,TH2F
					
decodeX = [ 0,32, 2,34, 4,36, 6,38, 8,40,10,42,12,44,14,46,
	   16,48,18,50,20,52,22,54,24,56,26,58,28,60,30,62,
	    1,33, 3,35, 5,37, 7,39, 9,41,11,43,13,45,15,47,
	   17,49,19,51,21,53,23,55,25,57,27,59,29,61,31,63]

decodeY = [31,63,29,61,27,59,25,57,23,55,21,53,19,51,17,49,
           15,47,13,45,11,43, 9,41, 7,39, 5,37, 3,35, 1,33,
	   30,62,28,60,26,58,24,56,22,54,20,52,18,50,16,48,
	   14,46,12,44,10,42, 8,40, 6,38, 4,36, 2,34, 0,32]

decodeY1 = [30,62,28,60,26,58,24,56,22,54,20,52,18,50,16,48,
	    14,46,12,44,10,42, 8,40, 6,38, 4,36, 2,34, 0,32,
	    31,63,29,61,27,59,25,57,23,55,21,53,19,51,17,49,
            15,47,13,45,11,43, 9,41, 7,39, 5,37, 3,35, 1,33]

tleft = 70
tright = 100

class ViewPC:


	class PC:
	

		def __init__(self,event,cr,rlist,decode):
		
			self.hits = []
			self.cls = []
		
			try:
				le78 = event.reco["LE78-%2d"%cr]
			
			except KeyError:
				return
			km = -1
			for im in rlist:
				km += 1
				try:
					m = le78.moduls[im]
				except KeyError:
					continue
			
				for t,e in m:
					ed = decode[e]
					hit = (t,ed+km*64)
					self.hits.append(hit)
					
			self.hits.sort(lambda x,y: cmp(x[1], y[1]))
			
			
			if not self.hits:
			    return
			
			cl = [self.hits[0]]
			for hit in self.hits[1:]:
			    if hit[1]-cl[-1][1]<2:
				cl.append(hit)
			    else:
			        self.cls.append(cl)
				cl = [hit]
			self.cls.append(cl)
			
#			print self.hits
#			print self.cls
			 
				

	class HPC:
		def __init__(self,rootfile,size,name):
			self.dir = rootfile.mkdir(name)
			self.dir.cd()
			self.hmult = TH1F( 'mult %s'%name, 'mult %s'%name, 32, 0, 32 )
			self.hprofile = TH1F( 'profile %s'%name, 'profile %s'%name, size, 0, size )
			self.hprofile2 = TH2F( 'profile2 %s'%name, 'profile2 %s'%name, size, 0, size ,size, 0, size )
			self.hd = TH2F( 'd %s'%name, 'd %s'%name, 10, -5, 5, size, 0, size )
			self.htime = TH1F( 'time %s'%name, 'time %s'%name, 256, 0, 256 )
			self.hprofiletime = TH2F( 'profiletime %s'%name, 'time %s'%name, size, 0, size, 256, 0, 256 )
			self.hprofilet = TH1F( 'profileT %s'%name, 'profileT %s'%name, size, 0, size )
			self.hprofilet1 = TH1F( 'profileT_even %s'%name, 'profileT1 %s'%name, size/2, 0, size/2 )
			self.hprofilet2 = TH1F( 'profileT_odd %s'%name, 'profileT2 %s'%name, size/2, 0, size/2 )
			
			self.dir.mkdir("Cluster").cd()
			self.hclmult = TH1F( 'clmult %s'%name, 'Cl mult %s'%name, 32, 0, 32 )
			self.hclleng = TH1F( 'clleng %s'%name, 'Cl leng %s'%name, 32, 0, 32 )
			self.ht30 = TH1F( 't30 %s'%name, 'Cl t30 %s'%name, 256, 0, 256 )
			self.ht31 = TH1F( 't31 %s'%name, 'Cl t31 %s'%name, 256, 0, 256 )
			self.ht32 = TH1F( 't32 %s'%name, 'Cl t32 %s'%name, 256, 0, 256 )
			
			
		def Fill(self,pc):
			self.hmult.Fill(len(pc.hits))
			for t,e in pc.hits:
				self.hprofile.Fill(e)
				self.htime.Fill(t)
				self.hprofiletime.Fill(e,t)
				if tleft<t<tright:
					self.hprofilet.Fill(e)
					ehalf,half = divmod(e,2)
					if half == 0:
						self.hprofilet1.Fill(ehalf)
					else:
						self.hprofilet2.Fill(ehalf)
			if len(pc.hits)<5:			
			    for h1 in pc.hits:
			        for h2 in pc.hits:
			            if not h1 == h2:
				        self.hprofile2.Fill(h1[1],h2[1])
					self.hd.Fill(h2[1]-h1[1],h1[1])
						
			self.hclmult.Fill(len(pc.cls))
			for cl in pc.cls:
			    self.hclleng.Fill(len(cl))
			    if len(cl)==3:
			        self.ht30.Fill(cl[0][0])
			        self.ht31.Fill(cl[1][0])
			        self.ht32.Fill(cl[2][0])
					
	class HPC2:
		def __init__(self,rootfile,size1,size2,name):
			self.dir = rootfile.mkdir(name)
			self.dir.cd()
			self.h = TH2F( '%s'%name, '%s'%name, size1, 0, size1, size2, 0, size2 )
			self.hd = TH1F( 'd %s'%name, 'd %s'%name, 100, -50, 50 )
			self.h2 = TH1F( '2 %s'%name, '2 %s'%name, 100, 0, min(size1,size2) )
		
		def Fill(self,pc1,pc2):
			for t1,e1 in pc1.hits:
			    if tleft<t1<tright:
				
			        for t2,e2 in pc2.hits:
				    if tleft<t2<tright:
					self.h.Fill(e1,e2)
					self.hd.Fill(e1-e2)
					if -30<(e1-e2)<0:
					    self.h2.Fill((e1+e2)/2)
			
								
	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("PC")
		self.dir.cd()
		
		self.hpcx2 = self.HPC(self.dir,64*10,"X2")
		self.hpcx3 = self.HPC(self.dir,64*10,"X3")
		self.hpcx4 = self.HPC(self.dir,64*10,"X4")
		self.hpcy1 = self.HPC(self.dir,64*7,"Y1")
		self.hpcy2 = self.HPC(self.dir,64*7,"Y2")
		self.hpcy3 = self.HPC(self.dir,64*7,"Y3")
		
		self.hpcx2x3 = self.HPC2(self.dir,64*10,64*10,"X2 X3")
		self.hpcx2x4 = self.HPC2(self.dir,64*10,64*10,"X2 X4")
		self.hpcx3x4 = self.HPC2(self.dir,64*10,64*10,"X3 X4")

		self.hpcy1y2 = self.HPC2(self.dir,64*7,64*7,"Y1 Y2")
		self.hpcy1y3 = self.HPC2(self.dir,64*7,64*7,"Y1 Y3")
		self.hpcy2y3 = self.HPC2(self.dir,64*7,64*7,"Y2 Y3")
		

	def Execute(self,event):
		
		pcx2 = self.PC(event,11,(14,15,16,17,18,19,20,21,22,23),decodeX)
		self.hpcx2.Fill(pcx2)	

		pcx3 = self.PC(event,13,(4,5,6,7,8,9,10,11,12,13),decodeX)
		self.hpcx3.Fill(pcx3)	

		pcx4 = self.PC(event,13,(14,15,16,17,18,19,20,21,22,23),decodeX)
		self.hpcx4.Fill(pcx4)	

		pcy1 = self.PC(event,11,(10,9,8,7,6,5,4),decodeY1)
		self.hpcy1.Fill(pcy1)	

		pcy2 = self.PC(event,10,(11,12,13,14,15,16,17),decodeY)
		self.hpcy2.Fill(pcy2)	
		
		pcy3 = self.PC(event,12,(4,5,6,7,8,9,10),decodeY)
		self.hpcy3.Fill(pcy3)	


		event.reco["PCX2"] = pcx2
		event.reco["PCX3"] = pcx3
		event.reco["PCX4"] = pcx4
		
		event.reco["PCY1"] = pcy1
		event.reco["PCY2"] = pcy2
		event.reco["PCY3"] = pcy3

		self.hpcx2x3.Fill(pcx2,pcx3)
		self.hpcx2x4.Fill(pcx2,pcx4)
		self.hpcx3x4.Fill(pcx3,pcx4)

		self.hpcy1y2.Fill(pcy1,pcy2)
		self.hpcy1y3.Fill(pcy1,pcy3)
		self.hpcy2y3.Fill(pcy2,pcy3)
		
