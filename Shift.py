class Selected:

    def __init__(self,z):
        self.z = z
	self.hits = []
	
    def append(self,hit):
        self.hits.append(hit)

class Selector:

    def __init__(self,geom):
        self.step = geom[0]
        self.shift = geom[1]
        self.z = geom[2]

class BPCSelector(Selector):

    def Select(self,bpc):

        sel = Selected(self.z)
        for t,e in bpc.ghits:
	    e = e*self.step + self.shift
    	    sel.append(e)
        return sel

class PCSelector(Selector):
    tleft = 50
    tright = 70


    def Select(self,pc):
        sel = Selected(self.z)
	if len(pc.hits)>5:
	    return sel
        for t,e in pc.hits:
    	    if self.tleft<t<self.tright:
    	        e = e*self.step + self.shift
	        sel.append(e)
        return sel

class HSelector(Selector):

    def Select(self,hod):
        sel = Selected(self.z)
	
        for e in hod.hits:
    	        e = e*self.step + self.shift
	        sel.append(e)
        return sel

class Select:

    def __init__(self):

	self.selectors = {}

#	self.selectors["H2Y"] = HSelector((2.0,-30,1500))

	self.selectors["H2Y"] = HSelector((2.02,-35,2532))
	
#	self.selectors["BPC1Y"] = BPCSelector((-1,100,-5000.5))
#	self.selectors["BPC2Y"] = BPCSelector((-1,100,-1598.5))
#	self.selectors["BPC3Y"] = BPCSelector((-1,120,2633.5))
#	self.selectors["BPC4Y"] = BPCSelector((-1,120,6083.5))

	self.selectors["BPC1Y"] = BPCSelector((-1.084,110,-5000.5))
	self.selectors["BPC2Y"] = BPCSelector((-1.084,90,-1598.5))
	self.selectors["BPC3Y"] = BPCSelector((-1.084,120,2769.5))
	self.selectors["BPC4Y"] = BPCSelector((-1.084,120,6102.5))

	self.selectors["PCY2"] = PCSelector((2,-410,20840.))
	self.selectors["PCY3"] = PCSelector((2,-430,26040.))

    def Execute(self,event):
    	
	for name in self.selectors.keys():
	    try:
	        reco = event.reco[name]
	    except KeyError:
	        continue
	    else:
	        event.select[name]=self.selectors[name].Select(reco)

class Track:
    def __init__(self,hits):
        
	self.hits = hits
	
	s1  = 0.
	sz  = 0.
	sz2 = 0.
	sx  = 0.
	sxz = 0.
        
        for x,z in hits:
	    s1  += 1
	    sz  += z
	    sz2 += z*z
	    sx  += x
	    sxz += x*z
	    
        Dis = sz2*s1 - sz*sz
        DisA = sxz*s1 -sz*sx
        DisB = sz2*sx -sz*sxz

        self.A = DisA/Dis
        self.B = DisB/Dis
	
	self.d = []
	self.chi2 = 0.
	for x,z in hits:
	    dx = x - (self.A*z +self.B)
	    self.d.append(dx)
	    self.chi2 += dx*dx

    def __repr__(self):
        return ",".join(("A:%f"%self.A,"B:%f"%self.B,"chi2:%f"%self.chi2))
	
def generator(listlist):

    index = [0,]*len(listlist)
    while True:
        li = []
        for i in range(len(index)):
            li.append(listlist[i][index[i]])
        yield li
    
        for k in range(len(index)):
            index[k] += 1
	    if index[k] < len(listlist[k]):
	        break
	    else:
	        index[k] = 0
        else:
	    raise StopIteration
    

class BestTrack:
    def __init__(self,sellist):
        self.tr = None
	lhits = []
	zs = []
	for s in sellist:
	    lhits.append(s.hits)
	    zs.append(s.z)

        chi2min = 1000000.
	for hs in generator(lhits):
	    tr = Track(zip(hs,zs))
            if tr.chi2 < chi2min:
	        chi2min = tr.chi2
		self.tr = tr
		
		
from ROOT import TH1F,TH2F,TH3F
class Shift:

    class H2:
        def __init__(self,rootdir,name1,name2):
	    self.name1 = name1
	    self.name2 = name2
	    self.dir = rootdir.mkdir(name1+name2)
	    self.dir.cd()

	    self.h = TH2F( 'h', 'h', 1000, -500, 500, 1000, -500, 500 )

	def Fill(self,event):
	    
	    try:
	    	sel1 = event.select[self.name1]
		sel2 = event.select[self.name2]
	    except KeyError:
	        return
		
	    for hit1 in sel1.hits:
	        for hit2 in sel2.hits:
		    self.h.Fill(hit1,hit2)
		    	

    class H3:
        def __init__(self,rootdir,name1,name2,name):
	    self.name1 = name1
	    self.name2 = name2
	    self.name = name
	    self.dir = rootdir.mkdir(name1+name2+name)
	    self.dir.cd()

	    self.h = TH2F( 'h', 'h', 1000, -500, 500, 1000, -500, 500 )
	    self.hd = TH1F( 'hd', 'hd', 100, -50, 50 )
	    self.hdd = TH2F( 'hdd', 'hdd', 400, -200, 200, 1000, -500, 500 )
	    self.hab = TH2F( 'hab', 'hab', 100, -0.01, 0.01, 100, -50, 50 )
	    self.hd1 = TH1F( 'hd1', 'hd1', 100, -100, 100 )
	    self.hd2 = TH1F( 'hd2', 'hd2', 100, -100, 100 )
	    self.hd3 = TH1F( 'hd3', 'hd3', 100, -100, 100 )
	    self.hhi2 = TH1F( 'hhi2', 'hhi2', 100, 0, 100 )
	    self.habmin = TH2F( 'habmin', 'hab', 100, -0.01, 0.01, 100, -50, 50 )
	    self.hd1min = TH1F( 'hd1min', 'hd1min', 100, -100, 100 )
	    self.hd2min = TH1F( 'hd2min', 'hd2min', 100, -100, 100 )
	    self.hd3min = TH1F( 'hd3min', 'hd3min', 100, -100, 100 )

	def Fill(self,event):
	    
	    try:
	    	sel1 = event.select[self.name1]
		sel2 = event.select[self.name2]
		sel = event.select[self.name]
	    except KeyError:
	        return
		

	    z1 = sel1.z
	    z2 = sel2.z
	    z = sel.z
	    
	    chi2min = 10000000.
	    for x1 in sel1.hits:
	        for x2 in sel2.hits:
		    h2 = ((x1,z1),(x2,z2))
		    tr2 = Track(h2)
		    xt = tr2.A*z + tr2.B
		    for x in sel.hits:
		        self.h.Fill(x,xt)
		        self.hd.Fill(x-xt)
		        self.hdd.Fill(x-xt,xt)

			h3 = h2 + ((x,z),)
			tr3 = Track(h3)
			self.hab.Fill(tr3.A,tr3.B)
			d = tr3.d
			self.hd1.Fill(d[0])
			self.hd2.Fill(d[1])
			self.hd3.Fill(d[2])

			if tr3.chi2 < chi2min:
                            trmin = tr3
			    chi2min = tr3.chi2			    
	    self.hhi2.Fill(chi2min)	    
	    if chi2min <100:
		self.habmin.Fill(trmin.A,trmin.B)
		d = trmin.d
	    	self.hd1min.Fill(d[0])	    
	    	self.hd2min.Fill(d[1])	    
	    	self.hd3min.Fill(d[2])
		
		
    class H4:
        def __init__(self,rootdir,name1,name2,name3,name):
	    self.name1 = name1
	    self.name2 = name2
	    self.name3 = name3
	    self.name = name
	    self.dir = rootdir.mkdir("H4"+name)
	    self.dir.cd()

	    self.h = TH2F( 'h', 'h', 1000, -500, 500, 1000, -500, 500 )
	    self.hd = TH1F( 'hd', 'hd', 100, -50, 50 )
	    self.hdd = TH2F( 'hdd', 'hdd', 100, -50, 50, 1000, -500, 500 )
	    self.hab = TH2F( 'hab', 'hab', 100, -0.01, 0.01, 100, -50, 50 )

	def Fill(self,event):
	    
	    try:
	    	sel1 = event.select[self.name1]
		sel2 = event.select[self.name2]
		sel3 = event.select[self.name3]
		sel = event.select[self.name]
	    except KeyError:
	        return
		
            if len(sel1.hits) == 0:
                return
            if len(sel2.hits) == 0:
                return
            if len(sel3.hits) == 0:
                return

            btr = BestTrack((sel1,sel2,sel3))
            tr = btr.tr
	    if tr.chi2>10:
	        return

	    z = sel.z
            xt = tr.A*z + tr.B
	    self.hab.Fill(tr.A,tr.B)
	    
	    for x in sel.hits:
	        self.h.Fill(x,xt)
	        self.hd.Fill(x-xt)
	        self.hdd.Fill(x-xt,xt)
    class HTr:
        def __init__(self,rootdir,name1,name2,name3,name4,name5):
	    self.name1 = name1
	    self.name2 = name2
	    self.name3 = name3
	    self.name4 = name4
	    self.name5 = name5
	    self.dir = rootdir.mkdir("Tr")
	    self.dir.cd()
            self.hd = [0,]*5
            self.hdd = [0,]*5
	    self.hd[0] = TH1F( 'hd0', 'hd0', 100, -50, 50 )
	    self.hd[1] = TH1F( 'hd1', 'hd1', 100, -50, 50 )
	    self.hd[2] = TH1F( 'hd2', 'hd2', 100, -50, 50 )
	    self.hd[3] = TH1F( 'hd3', 'hd3', 100, -50, 50 )
	    self.hd[4] = TH1F( 'hd4', 'hd4', 100, -50, 50 )
	    self.hdd[0] = TH2F( 'hdd0', 'hdd0', 400, -200, 200, 1000, -500, 500 )
	    self.hdd[1] = TH2F( 'hdd1', 'hdd1', 400, -200, 200, 1000, -500, 500 )
	    self.hdd[2] = TH2F( 'hdd2', 'hdd2', 400, -200, 200, 1000, -500, 500 )
	    self.hdd[3] = TH2F( 'hdd3', 'hdd3', 400, -200, 200, 1000, -500, 500 )
	    self.hdd[4] = TH2F( 'hdd4', 'hdd4', 400, -200, 200, 1000, -500, 500 )
	    self.hab = TH2F( 'hab', 'hab', 100, -0.01, 0.01, 100, -50, 50 )

	def Fill(self,event):
	    
	    try:
	    	sel1 = event.select[self.name1]
		sel2 = event.select[self.name2]
		sel3 = event.select[self.name3]
		sel4 = event.select[self.name4]
		sel5 = event.select[self.name5]
	    except KeyError:
	        return
		
            if len(sel1.hits) == 0:
                return
            if len(sel2.hits) == 0:
                return
            if len(sel3.hits) == 0:
                return
            if len(sel4.hits) == 0:
                return
            if len(sel5.hits) == 0:
                return

            btr = BestTrack((sel1,sel2,sel3,sel4,sel5))
            tr = btr.tr
	    if tr.chi2>100:
	        return

	    self.hab.Fill(tr.A,tr.B)
	    
	    for i,d in enumerate(tr.d):
	        z = tr.hits[i][1]
                xt = tr.A*z + tr.B
	        self.hd[i].Fill(d)
	        self.hdd[i].Fill(d,xt)

	    
    def __init__(self,rootfile):

	self.dir = rootfile.mkdir("Shift")
	self.dir.cd()

	self.h = []
	self.h.append(self.H2(self.dir,"BPC1Y","BPC2Y"))
	self.h.append(self.H2(self.dir,"BPC3Y","BPC4Y"))
	self.h.append(self.H2(self.dir,"PCY2","PCY3"))
	self.h.append(self.H2(self.dir,"PCY2","BPC3Y"))
	self.h.append(self.H2(self.dir,"PCY2","BPC4Y"))
	self.h.append(self.H2(self.dir,"PCY3","BPC3Y"))
	self.h.append(self.H2(self.dir,"PCY3","BPC4Y"))

	self.h.append(self.H2(self.dir,"BPC3Y","H2Y"))
	self.h.append(self.H2(self.dir,"BPC4Y","H2Y"))

	self.h.append(self.H3(self.dir,"BPC1Y","BPC2Y","H2Y"))
	self.h.append(self.H3(self.dir,"BPC3Y","BPC4Y","H2Y"))
	self.h.append(self.H3(self.dir,"BPC3Y","BPC4Y","BPC1Y"))
	self.h.append(self.H3(self.dir,"BPC3Y","BPC4Y","BPC2Y"))
	self.h.append(self.H3(self.dir,"BPC3Y","BPC4Y","PCY2"))
	self.h.append(self.H3(self.dir,"BPC3Y","BPC4Y","PCY3"))

	self.h.append(self.H4(self.dir,"BPC3Y","BPC4Y","H2Y","PCY2"))
	self.h.append(self.H4(self.dir,"BPC3Y","BPC4Y","H2Y","PCY3"))
	self.h.append(self.H4(self.dir,"BPC3Y","BPC4Y","H2Y","BPC1Y"))
	self.h.append(self.H4(self.dir,"BPC3Y","BPC4Y","H2Y","BPC2Y"))

	self.h.append(self.HTr(self.dir,"BPC3Y","BPC4Y","H2Y","PCY2","PCY3"))
#	self.h.append(self.HTr(self.dir,"BPC3Y","BPC4Y","H2Y","BPC1Y","BPC2Y"))
	
    def Execute(self,event):
	
	for h in self.h:
	    h.Fill(event)

