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
#        for t,e in bpc.ghits:
        for t,e in bpc.hits:
	    e = e*self.step + self.shift
    	    sel.append(e)
        return sel

class PCSelector(Selector):
    tleft = 50
    tright = 70


    def Select(self,pc):
        sel = Selected(self.z)
	if len(pc.hits)>7:
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

	self.selectors["H2X"] = HSelector((2.0,-30,20840))

	self.selectors["H2Y"] = HSelector((2.0,-35,20840))
	
#	self.selectors["BPC1X"] = BPCSelector((1.084,-30,-33805.))
	self.selectors["BPC2X"] = BPCSelector((1.084,-17,-29250.))
	self.selectors["BPC3X"] = BPCSelector((1.084,-50,-25790.))
	self.selectors["BPC4X"] = BPCSelector((1.084,-67,-20685.))

	self.selectors["BPC1Y"] = BPCSelector((1.084,-90,-33755.))
	self.selectors["BPC2Y"] = BPCSelector((1.084,-70,-29200.))
	self.selectors["BPC3Y"] = BPCSelector((1.084,-81,-25840.))
	self.selectors["BPC4Y"] = BPCSelector((1.084,-68,-20735.))

#	self.selectors["PCX1"] = PCSelector((2,-610,-6802.))
	self.selectors["PCX2"] = PCSelector((2,-617,-6602.))
	self.selectors["PCX3"] = PCSelector((2,-625,-2496.))
	self.selectors["PCX4"] = PCSelector((2,-628,-2296.))

	self.selectors["PCY1"] = PCSelector(( 2,-273,-6750.))
	self.selectors["PCY2"] = PCSelector((-2, 491,-6550.))
	self.selectors["PCY3"] = PCSelector((-2, 522,-2444.))
#	self.selectors["PCY4"] = PCSelector(( 2,-330,-2244.))

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
	    self.hab = TH2F( 'hab', 'hab', 100, -0.01, 0.01, 100, -100, 100 )
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
    class HTrX:
        def __init__(self,rootdir,name1,name2,name3):
	    self.name1 = name1
	    self.name2 = name2
	    self.name3 = name3
	    self.dir = rootdir.mkdir("BeamTrX")
	    self.dir.cd()
            self.hd = [0,]*5
            self.hdd = [0,]*5
	    self.hd[0] = TH1F( 'hd0', 'hd0', 100, -50, 50 )
	    self.hd[1] = TH1F( 'hd1', 'hd1', 100, -50, 50 )
	    self.hd[2] = TH1F( 'hd2', 'hd2', 100, -50, 50 )
	    self.hdd[0] = TH2F( 'hdd0', 'hdd0', 400, -200, 200, 1000, -500, 500 )
	    self.hdd[1] = TH2F( 'hdd1', 'hdd1', 400, -200, 200, 1000, -500, 500 )
	    self.hdd[2] = TH2F( 'hdd2', 'hdd2', 400, -200, 200, 1000, -500, 500 )
	    self.hab = TH2F( 'hab', 'hab', 100, -0.01, 0.01, 100, -100, 100 )
	    self.hchi = TH1F( 'hchi', 'hchi', 100, 0, 100 )

	def Fill(self,event):
	    
	    try:
	    	sel1 = event.select[self.name1]
		sel2 = event.select[self.name2]
		sel3 = event.select[self.name3]
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
	    if tr.chi2>100:
	        return

	    self.hab.Fill(tr.A,tr.B)
	    self.hchi.Fill(tr.chi2)
	    
	    for i,d in enumerate(tr.d):
	        z = tr.hits[i][1]
                xt = tr.A*z + tr.B
	        self.hd[i].Fill(d)
	        self.hdd[i].Fill(d,xt)

	    event.select["BeamTrX"] = tr
	    
    class HTrY:
        def __init__(self,rootdir,name1,name2,name3,name4):
	    self.name1 = name1
	    self.name2 = name2
	    self.name3 = name3
	    self.name4 = name4
	    self.dir = rootdir.mkdir("BeamTrY")
	    self.dir.cd()
            self.hd = [0,]*5
            self.hdd = [0,]*5
	    self.hd[0] = TH1F( 'hd0', 'hd0', 100, -50, 50 )
	    self.hd[1] = TH1F( 'hd1', 'hd1', 100, -50, 50 )
	    self.hd[2] = TH1F( 'hd2', 'hd2', 100, -50, 50 )
	    self.hd[3] = TH1F( 'hd3', 'hd3', 100, -50, 50 )
	    self.hdd[0] = TH2F( 'hdd0', 'hdd0', 400, -200, 200, 1000, -500, 500 )
	    self.hdd[1] = TH2F( 'hdd1', 'hdd1', 400, -200, 200, 1000, -500, 500 )
	    self.hdd[2] = TH2F( 'hdd2', 'hdd2', 400, -200, 200, 1000, -500, 500 )
	    self.hdd[3] = TH2F( 'hdd3', 'hdd3', 400, -200, 200, 1000, -500, 500 )
	    self.hab = TH2F( 'hab', 'hab', 100, -0.01, 0.01, 100, -100, 100 )
	    self.hchi = TH1F( 'hchi', 'hchi', 100, 0, 100 )

	def Fill(self,event):
	    
	    try:
	    	sel1 = event.select[self.name1]
		sel2 = event.select[self.name2]
		sel3 = event.select[self.name3]
		sel4 = event.select[self.name4]
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

            btr = BestTrack((sel1,sel2,sel3,sel4))
            tr = btr.tr
	    if tr.chi2>100:
	        return

	    self.hab.Fill(tr.A,tr.B)
	    self.hchi.Fill(tr.chi2)
	    
	    for i,d in enumerate(tr.d):
	        z = tr.hits[i][1]
                xt = tr.A*z + tr.B
	        self.hd[i].Fill(d)
	        self.hdd[i].Fill(d,xt)

	    event.select["BeamTrY"] = tr

    class HTrXL:
        def __init__(self,rootdir,name1,name2,name3,name4,name5,name6):
	    self.name1 = name1
	    self.name2 = name2
	    self.name3 = name3
	    self.name4 = name4
	    self.name5 = name5
	    self.name6 = name6
	    self.dir = rootdir.mkdir("LongTrX")
	    self.dir.cd()
            self.hd = [0,]*6
            self.hdd = [0,]*6
	    self.hd[0] = TH1F( 'hd0', 'hd0', 100, -50, 50 )
	    self.hd[1] = TH1F( 'hd1', 'hd1', 100, -50, 50 )
	    self.hd[2] = TH1F( 'hd2', 'hd2', 100, -50, 50 )
	    self.hd[3] = TH1F( 'hd3', 'hd3', 100, -50, 50 )
	    self.hd[4] = TH1F( 'hd4', 'hd4', 100, -50, 50 )
	    self.hd[5] = TH1F( 'hd5', 'hd5', 100, -50, 50 )
	    self.hdd[0] = TH2F( 'hdd0', 'hdd0', 400, -200, 200, 1000, -500, 500 )
	    self.hdd[1] = TH2F( 'hdd1', 'hdd1', 400, -200, 200, 1000, -500, 500 )
	    self.hdd[2] = TH2F( 'hdd2', 'hdd2', 400, -200, 200, 1000, -500, 500 )
	    self.hdd[3] = TH2F( 'hdd3', 'hdd3', 400, -200, 200, 1000, -500, 500 )
	    self.hdd[4] = TH2F( 'hdd4', 'hdd4', 400, -200, 200, 1000, -500, 500 )
	    self.hdd[5] = TH2F( 'hdd5', 'hdd5', 400, -200, 200, 1000, -500, 500 )
	    self.hab = TH2F( 'hab', 'hab', 100, -0.01, 0.01, 100, -100, 100 )
	    self.hchi = TH1F( 'hchi', 'hchi', 100, 0, 100 )

	def Fill(self,event):
	    
	    try:
	    	sel1 = event.select[self.name1]
		sel2 = event.select[self.name2]
		sel3 = event.select[self.name3]
	    	sel4 = event.select[self.name4]
		sel5 = event.select[self.name5]
		sel6 = event.select[self.name6]
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
            if len(sel6.hits) == 0:
                return

            btr = BestTrack((sel1,sel2,sel3,sel4,sel5,sel6))
            tr = btr.tr
	    if tr.chi2>100:
	        return

	    self.hab.Fill(tr.A,tr.B)
	    self.hchi.Fill(tr.chi2)
	    
	    for i,d in enumerate(tr.d):
	        z = tr.hits[i][1]
                xt = tr.A*z + tr.B
	        self.hd[i].Fill(d)
	        self.hdd[i].Fill(d,xt)

	    event.select["LongTrX"] = tr
	    
    class HTrYL:
        def __init__(self,rootdir,name1,name2,name3,name4,name5,name6,name7):
	    self.name1 = name1
	    self.name2 = name2
	    self.name3 = name3
	    self.name4 = name4
	    self.name5 = name5
	    self.name6 = name6
	    self.name7 = name7
	    self.dir = rootdir.mkdir("LongTrY")
	    self.dir.cd()
            self.hd = [0,]*7
            self.hdd = [0,]*7
	    self.hd[0] = TH1F( 'hd0', 'hd0', 100, -50, 50 )
	    self.hd[1] = TH1F( 'hd1', 'hd1', 100, -50, 50 )
	    self.hd[2] = TH1F( 'hd2', 'hd2', 100, -50, 50 )
	    self.hd[3] = TH1F( 'hd3', 'hd3', 100, -50, 50 )
	    self.hd[4] = TH1F( 'hd4', 'hd4', 100, -50, 50 )
	    self.hd[5] = TH1F( 'hd5', 'hd5', 100, -50, 50 )
	    self.hd[6] = TH1F( 'hd6', 'hd6', 100, -50, 50 )
	    self.hdd[0] = TH2F( 'hdd0', 'hdd0', 400, -200, 200, 1000, -500, 500 )
	    self.hdd[1] = TH2F( 'hdd1', 'hdd1', 400, -200, 200, 1000, -500, 500 )
	    self.hdd[2] = TH2F( 'hdd2', 'hdd2', 400, -200, 200, 1000, -500, 500 )
	    self.hdd[3] = TH2F( 'hdd3', 'hdd3', 400, -200, 200, 1000, -500, 500 )
	    self.hdd[4] = TH2F( 'hdd4', 'hdd4', 400, -200, 200, 1000, -500, 500 )
	    self.hdd[5] = TH2F( 'hdd5', 'hdd5', 400, -200, 200, 1000, -500, 500 )
	    self.hdd[6] = TH2F( 'hdd6', 'hdd6', 400, -200, 200, 1000, -500, 500 )
	    self.hab = TH2F( 'hab', 'hab', 100, -0.01, 0.01, 100, -100, 100 )
	    self.hchi = TH1F( 'hchi', 'hchi', 100, 0, 100 )

	def Fill(self,event):
	    
	    try:
	    	sel1 = event.select[self.name1]
		sel2 = event.select[self.name2]
		sel3 = event.select[self.name3]
		sel4 = event.select[self.name4]
		sel5 = event.select[self.name5]
		sel6 = event.select[self.name6]
		sel7 = event.select[self.name7]
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
            if len(sel6.hits) == 0:
                return
            if len(sel7.hits) == 0:
                return

            btr = BestTrack((sel1,sel2,sel3,sel4,sel5,sel6,sel7))
            tr = btr.tr
	    if tr.chi2>100:
	        return

	    self.hab.Fill(tr.A,tr.B)
	    self.hchi.Fill(tr.chi2)
	    
	    for i,d in enumerate(tr.d):
	        z = tr.hits[i][1]
                xt = tr.A*z + tr.B
	        self.hd[i].Fill(d)
	        self.hdd[i].Fill(d,xt)

	    event.select["longTrY"] = tr
    class HTrXSec:
        def __init__(self,rootdir,name1,name2,name3):
	    self.name1 = name1
	    self.name2 = name2
	    self.name3 = name3
	    self.dir = rootdir.mkdir("SecTrX")
	    self.dir.cd()
            self.hd = [0,]*5
            self.hdd = [0,]*5
	    self.hd[0] = TH1F( 'hd0', 'hd0', 100, -50, 50 )
	    self.hd[1] = TH1F( 'hd1', 'hd1', 100, -50, 50 )
	    self.hd[2] = TH1F( 'hd2', 'hd2', 100, -50, 50 )
	    self.hdd[0] = TH2F( 'hdd0', 'hdd0', 400, -200, 200, 1000, -500, 500 )
	    self.hdd[1] = TH2F( 'hdd1', 'hdd1', 400, -200, 200, 1000, -500, 500 )
	    self.hdd[2] = TH2F( 'hdd2', 'hdd2', 400, -200, 200, 1000, -500, 500 )
	    self.hab = TH2F( 'hab', 'hab', 100, -0.01, 0.01, 100, -100, 100 )
	    self.hchi = TH1F( 'hchi', 'hchi', 100, 0, 100 )

	def Fill(self,event):
	    
	    try:
	    	sel1 = event.select[self.name1]
		sel2 = event.select[self.name2]
		sel3 = event.select[self.name3]
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
	    if tr.chi2>100:
	        return

	    self.hab.Fill(tr.A,tr.B)
	    self.hchi.Fill(tr.chi2)
	    
	    for i,d in enumerate(tr.d):
	        z = tr.hits[i][1]
                xt = tr.A*z + tr.B
	        self.hd[i].Fill(d)
	        self.hdd[i].Fill(d,xt)

	    event.select["SecTrX"] = tr
	    
    class HTrYSec:
        def __init__(self,rootdir,name1,name2,name3):
	    self.name1 = name1
	    self.name2 = name2
	    self.name3 = name3
	    self.dir = rootdir.mkdir("SecTrY")
	    self.dir.cd()
            self.hd = [0,]*3
            self.hdd = [0,]*3
	    self.hd[0] = TH1F( 'hd0', 'hd0', 100, -50, 50 )
	    self.hd[1] = TH1F( 'hd1', 'hd1', 100, -50, 50 )
	    self.hd[2] = TH1F( 'hd2', 'hd2', 100, -50, 50 )
	    self.hdd[0] = TH2F( 'hdd0', 'hdd0', 400, -200, 200, 1000, -500, 500 )
	    self.hdd[1] = TH2F( 'hdd1', 'hdd1', 400, -200, 200, 1000, -500, 500 )
	    self.hdd[2] = TH2F( 'hdd2', 'hdd2', 400, -200, 200, 1000, -500, 500 )
	    self.hab = TH2F( 'hab', 'hab', 100, -0.01, 0.01, 100, -100, 100 )
	    self.hchi = TH1F( 'hchi', 'hchi', 100, 0, 100 )

	def Fill(self,event):
	    
	    try:
	    	sel1 = event.select[self.name1]
		sel2 = event.select[self.name2]
		sel3 = event.select[self.name3]
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
	    if tr.chi2>100:
	        return

	    self.hab.Fill(tr.A,tr.B)
	    self.hchi.Fill(tr.chi2)
	    
	    for i,d in enumerate(tr.d):
	        z = tr.hits[i][1]
                xt = tr.A*z + tr.B
	        self.hd[i].Fill(d)
	        self.hdd[i].Fill(d,xt)

	    event.select["SecTrY"] = tr

    class HZ:
        def __init__(self,rootdir):

	    self.dir = rootdir.mkdir("Z")
	    self.dir.cd()

	    self.hdax = TH1F( 'hdax', 'dax', 100, -0.1, 0.1 )
	    self.hzx = TH1F( 'hzx', 'zx', 100, -50, 0 )
	    
	    self.hday = TH1F( 'hday', 'day', 100, -0.1, 0.1 )
	    self.hzy = TH1F( 'hzy', 'zy', 100, -50, 0 )

	    self.hda = TH1F( 'hda', 'da', 100, 0.0, 0.1 )

	def Fill(self,event):

	    OK = True
	    try:
	    	beamtrx = event.select['BeamTrX']
	    	sectrx = event.select['SecTrX']
		self.hdax.Fill(sectrx.A - beamtrx.A)
		if abs(sectrx.A - beamtrx.A)>0.002:
		    zx = -(sectrx.B - beamtrx.B)/(sectrx.A - beamtrx.A)
		    self.hzx.Fill(zx/1000.)
	    except KeyError:
	        OK = False
		
	    try:
	    	beamtry = event.select['BeamTrY']
	    	sectry = event.select['SecTrY']
		self.hday.Fill(sectry.A - beamtry.A)
		if abs(sectry.A - beamtry.A)>0.002:
		    zy = -(sectry.B - beamtry.B)/(sectry.A - beamtry.A)
		    self.hzy.Fill(zy/1000.)
	    except KeyError:
	        OK = False

	    if OK:
	    	da = ((sectrx.A - beamtrx.A)**2 + (sectry.A - beamtry.A)**2 ) **0.5
		self.hda.Fill(da)
	    
		
    class HShift:

        def __init__(self,rootdir,track,det):
	
	    self.track = track
	    self.det = det
	    self.dir = rootdir.mkdir("%s_%s"%(track,det))
	    self.dir.cd()
	    self.h = TH2F( 'h', 'h', 1000, -500, 500, 1000, -500, 500 )
	    
	    
	def Fill(self,event):
	
	    try:
	    	track = event.select[self.track]
		det = event.select[self.det]
	    except KeyError:
	        return
		
	    a = track.A
	    b = track.B
	    z = det.z
	    coor = a*z+b
	    for hit in det.hits:
	        self.h.Fill(coor,hit)
	
	
    def __init__(self,rootfile):

	self.dir = rootfile.mkdir("Shift")
	self.dir.cd()

	self.h = []

#	self.h.append(self.H2(self.dir,"BPC2X","BPC3X"))
#	self.h.append(self.H3(self.dir,"BPC3X","BPC4X","H2X"))

	self.h.append(self.HTrX(self.dir,"BPC2X","BPC3X","BPC4X"))

#	self.h.append(self.H2(self.dir,"BPC1Y","BPC2Y"))	
#	self.h.append(self.H4(self.dir,"BPC2Y","BPC3Y","BPC4Y","H2Y"))
	
	self.h.append(self.HTrY(self.dir,"BPC1Y","BPC2Y","BPC3Y","BPC4Y"))

#	self.h.append(self.HShift(self.dir,"BeamTrX","PCX1"))
	self.h.append(self.HShift(self.dir,"BeamTrX","PCX2"))
	self.h.append(self.HShift(self.dir,"BeamTrX","PCX3"))
	self.h.append(self.HShift(self.dir,"BeamTrX","PCX4"))

	self.h.append(self.HShift(self.dir,"BeamTrY","PCY1"))
	self.h.append(self.HShift(self.dir,"BeamTrY","PCY2"))
	self.h.append(self.HShift(self.dir,"BeamTrY","PCY3"))
#	self.h.append(self.HShift(self.dir,"BeamTrY","PCY4"))

	self.h.append(self.H2(self.dir,"PCX2","PCX3"))
	self.h.append(self.H2(self.dir,"PCX2","PCX4"))
	self.h.append(self.H2(self.dir,"PCX3","PCX4"))

	self.h.append(self.H2(self.dir,"PCY1","PCY2"))
	self.h.append(self.H2(self.dir,"PCY1","PCY3"))
	self.h.append(self.H2(self.dir,"PCY2","PCY3"))

	self.h.append(self.HTrXL(self.dir,"BPC2X","BPC3X","BPC4X","PCX2","PCX3","PCX4"))
	self.h.append(self.HTrYL(self.dir,"BPC1Y","BPC2Y","BPC3Y","BPC4Y","PCY1","PCY2","PCY3"))

	self.h.append(self.HTrXSec(self.dir,"PCX2","PCX3","PCX4"))
	self.h.append(self.HTrYSec(self.dir,"PCY1","PCY2","PCY3"))

	self.h.append(self.HZ(self.dir))
	
    def Execute(self,event):
	
	for h in self.h:
	    h.Fill(event)

