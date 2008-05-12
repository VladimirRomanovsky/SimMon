from ROOT import TH1F,TH2F,TH3F

DT78_decode = (7,15,0,8, 6,14,1,9, 5,13,2,10, 4,12,3,11,)
bad = {6:(16,18,22,)}

def _decode(e):
	k,k16 = divmod(e,16)
	e = k*16 + DT78_decode[k16]
	
	return e		    


class DT78:
	def __init__(self,event):
	
		dtx = []
		dty = []
		
		try:
		    le78 = event.reco["LE78-10"]
		except KeyError:
		    self.dtx = dtx
		    self.dty = dty
		    return

		for modul in (6,7,8,9,10):
		    try:
			mod = le78.moduls[modul]
		    except KeyError:
			continue
		
		    for t,e in mod:
		    
		  	if modul in bad.keys():
			    if e in bad[modul]:
			        continue
			      
		        k,k32 = divmod(e,32)
			cabel = (modul-6)*2+k
			k32 = _decode(k32)
			if cabel<5:
				dtx.append((cabel*32+k32,t))
			else:
				dty.append(((cabel-5)*32+k32,t))

#		print "DTX:",dtx
#		print "DTY:",dty

		self.dtx = dtx 
		self.dty = dty

class ViewDTDecode:

    def __init__(self,rootfile):
	self.dir = rootfile.mkdir("DTDecode")
	self.dir.cd()

	self.h = {}
	self.hd = {}
	self.h2 = {}
	for m in range(6,11):	
	    self.h[m] = TH1F( 'hc%02d'%m, 'hc', 64, 0, 64 )
	    self.hd[m] = TH1F( 'hcd%02d'%m, 'hcd', 64, 0, 64 )
	    self.h2[m] = TH2F( 'h2%02d'%m, 'h2', 64, 0, 64, 64, 0, 64 )
	self.h8 = TH2F( 'h8', 'h8', 40, 0, 40, 40, 0, 40 )

    def Execute(self,event):

	try:
	    le78 = event.reco["LE78-10"]
	except KeyError:
	    return
	
	
	n8 = 40*[0,]
	    
	for m in range(6,11):
	    try:
		mod = le78.moduls[m]
	    except KeyError:
		continue
	    modd = []
	    for t,e in mod:
	    
	        self.h[m].Fill(e)
		
		ed = _decode(e)  
	        self.hd[m].Fill(ed)
                modd.append((t,ed))
		
		k8 = ed/8 + (m-6)*8
		n8[k8] += 1
		
	    for t1,e1 in modd:
	        for t2,e2 in modd:
		    if not e1==e2:
		        self.h2[m].Fill(e1,e2)
			
			
			
	    for i1 in range(40):
	        for i2 in range(40):
		    if not i1==i2:
		        self.h8.Fill(i1,i2,n8[i1]*n8[i2])
        
class ViewDT78:

	class HDT78:

		def __init__(self,rootfile,name):
		
			self.dir = rootfile.mkdir(name)
			self.dir.cd()
			self.name = name 
			
			self.hte = TH2F( 'hte', 'hte',128, 0, 128 ,160, 0, 160 )
			self.ht = TH1F( 'ht', 'ht',128, 0, 128 )
			self.hdt = TH1F( 'hdt', 'hdt',128, -128, 128 )
			self.hst = TH1F( 'hst', 'hst',128, 0, 256 )
			self.he = TH1F( 'he', 'he',160, 0, 160 )
			self.htt = TH2F( 'htt', 'htt',128, 0, 128 ,128, 0, 128 )
			self.hee = TH2F( 'hee', 'hee',160, 0, 160 ,160, 0, 160 )
			self.heed = TH2F( 'heed', 'heed',160, 0, 160 ,160, 0, 160 )
			self.hees = TH2F( 'hees', 'hees',160, 0, 160 ,160, 0, 160 )

			if self.name =="DTX":
			    self.htt_01_05 = TH2F( 'htt-01-05', 'htt',128, 0, 128 ,128, 0, 128 )
			    self.htt_02_03 = TH2F( 'htt-02-03', 'htt',128, 0, 128 ,128, 0, 128 )
			    self.htt_06_08 = TH2F( 'htt-06-08', 'htt',128, 0, 128 ,128, 0, 128 )
			    self.htt_12_13 = TH2F( 'htt-12-13', 'htt',128, 0, 128 ,128, 0, 128 )
			    self.htt_14_18 = TH2F( 'htt-14-18', 'htt',128, 0, 128 ,128, 0, 128 )
			if self.name =="DTY":
			    self.htt_00_04 = TH2F( 'htt-00-04', 'htt',128, 0, 128 ,128, 0, 128 )
			    self.htt_00_06 = TH2F( 'htt-00-06', 'htt',128, 0, 128 ,128, 0, 128 )
			    self.htt_04_06 = TH2F( 'htt-04-06', 'htt',128, 0, 128 ,128, 0, 128 )
			    self.htt_05_07 = TH2F( 'htt-05-07', 'htt',128, 0, 128 ,128, 0, 128 )
			    self.htt_05_11 = TH2F( 'htt-05-11', 'htt',128, 0, 128 ,128, 0, 128 )
			    self.htt_07_11 = TH2F( 'htt-07-11', 'htt',128, 0, 128 ,128, 0, 128 )
			    self.htt_13_19 = TH2F( 'htt-13-19', 'htt',128, 0, 128 ,128, 0, 128 )


		def Fill(self,dt):

                    for e,t in dt:
		        self.hte.Fill(t,e)
		        self.ht.Fill(t)
		        self.he.Fill(e)
			
			
			
		    for e1,t1 in dt:
		        for e2,t2 in dt:
			    if not e1==e2:
			        self.htt.Fill(t1,t2) 
			        self.hee.Fill(e1,e2)
			        self.hdt.Fill(t1-t2)
			        self.hst.Fill(t1+t2)
			        if abs(t1-t2)<10:
				    self.heed.Fill(e1,e2)
			        if abs(t1+t2)<150:
				    self.hees.Fill(e1,e2)
				    
				k8_1 = e1/8
				k8_2 = e2/8
				if self.name =="DTX":
				    if k8_1 == 1 and k8_2 == 5:
				         self.htt_01_05.Fill(t1,t2)
				    if k8_1 == 2 and k8_2 == 3:
				         self.htt_02_03.Fill(t1,t2)
				    if k8_1 == 6 and k8_2 == 8:
				         self.htt_06_08.Fill(t1,t2)
				    if k8_1 ==12 and k8_2 ==13:
				         self.htt_12_13.Fill(t1,t2)
				    if k8_1 ==14 and k8_2 ==18:
				         self.htt_14_18.Fill(t1,t2)
					
				if self.name =="DTY":
				    if k8_1 == 0 and k8_2 == 4:
				         self.htt_00_04.Fill(t1,t2)
				    if k8_1 == 0 and k8_2 == 6:
				         self.htt_00_06.Fill(t1,t2)
				    if k8_1 == 4 and k8_2 == 6:
				         self.htt_04_06.Fill(t1,t2)
				    if k8_1 == 5 and k8_2 == 7:
				         self.htt_05_07.Fill(t1,t2)
				    if k8_1 == 5 and k8_2 ==11:
				         self.htt_05_11.Fill(t1,t2)
				    if k8_1 == 7 and k8_2 ==11:
				         self.htt_07_11.Fill(t1,t2)
				    if k8_1 ==13 and k8_2 ==19:
				         self.htt_13_19.Fill(t1,t2)
		        	       
	def __init__(self,rootfile):

		
		self.dir = rootfile.mkdir("DT78")
		self.dir.cd()
		
		self.hdtx = self.HDT78(self.dir,"DTX")
		self.hdty = self.HDT78(self.dir,"DTY")
		
	def Execute(self,event):

		dt = DT78(event)

		self.hdtx.Fill(dt.dtx)		
		self.hdty.Fill(dt.dty)		
		
		
		
