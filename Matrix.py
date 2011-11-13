from ROOT import TH1F,TH2F

decode09 = []
decode10 = []
decode11 = []
decode12 = []
for i in range(64):
    ky,d = divmod(i,32)
    y0,d = divmod(d,8)
    x0,kx= divmod(d,2)
    y = y0 + (1-ky)*4
    x = x0 + (kx)*4
    decode09.append((x,y))
    decode10.append((x,y))
    y = 3-y0 + (1-ky)*4
    x = 3-x0 + (kx)*4
    decode11.append((x,y))
    decode12.append((x,y))

class ViewMatrix:

    def __init__(self,rootfile):
	self.dir = rootfile.mkdir("Matrix")
	self.dir.cd()
	
	self.ht09 = TH1F( 'ht09', 'ht', 256, 0, 256 )
	self.ht10 = TH1F( 'ht10', 'ht', 256, 0, 256 )
	self.ht11 = TH1F( 'ht11', 'ht', 256, 0, 256 )
	self.ht12 = TH1F( 'ht12', 'ht', 256, 0, 256 )
	self.ht = TH1F( 'ht', 'ht', 256, 0, 256 )
	self.h2 = TH2F( 'h2', 'XY', 16, 0, 16, 16, 0, 16 )
	self.hx = TH1F( 'hx', 'X', 16, 0, 16)
	self.hy = TH1F( 'hy', 'Y', 16, 0, 16)
	self.h2t = TH2F( 'h2t', 'XY', 16, 0, 16, 16, 0, 16 )
	self.hxt = TH1F( 'hxt', 'X', 16, 0, 16)
	self.hyt = TH1F( 'hyt', 'Y', 16, 0, 16)
	self.hn = TH1F( 'hn', 'Mult', 16, 0, 16)
	self.hnt = TH1F( 'hnt', 'Mult', 16, 0, 16)
	self.hn09 = TH1F( 'hn09', 'Mult', 16, 0, 16)
	self.hn10 = TH1F( 'hn10', 'Mult', 16, 0, 16)
	self.hn11 = TH1F( 'hn11', 'Mult', 16, 0, 16)
	self.hn12 = TH1F( 'hn12', 'Mult', 16, 0, 16)
	
    def Execute(self,event):
	hits = []
	try:
	    le78 = event.reco["LE78-14"]
	    mod09 = le78.moduls[ 9]
	    mod10 = le78.moduls[10]
	    mod11 = le78.moduls[11]
	    mod12 = le78.moduls[12]
	except KeyError:
	    return
	n = 0
	nt = 0

        for t,e in mod09:
	
	    self.ht09.Fill(t)
            t = t-70+64
	    self.ht.Fill(t)
	    
            x,y = decode09[e]
	    y = y + 8

	    self.h2.Fill(x,y)
	    self.hx.Fill(x)
	    self.hy.Fill(y)
            hits.append((x,y,t))
	    n += 1
	    if 45<t<60:
	        nt += 1
	        self.h2t.Fill(x,y)
	        self.hxt.Fill(x)
	        self.hyt.Fill(y)
	    
        for t,e in mod10:
	
	    self.ht10.Fill(t)
            t = t-69+64
	    self.ht.Fill(t)
	    
            x,y = decode10[e]

	    self.h2.Fill(x,y)
	    self.hx.Fill(x)
	    self.hy.Fill(y)
            hits.append((x,y,t))
	    n += 1
	    if 45<t<60:
	        nt += 1
	        self.h2t.Fill(x,y)
	        self.hxt.Fill(x)
	        self.hyt.Fill(y)
	    
        for t,e in mod11:
	
	    self.ht11.Fill(t)
            t = t-63+64
	    self.ht.Fill(t)
	    
            x,y = decode11[e]
	    x = x + 8
	    y = y + 8

	    self.h2.Fill(x,y)
	    self.hx.Fill(x)
	    self.hy.Fill(y)
            hits.append((x,y,t))
	    n += 1
	    if 45<t<60:
	        nt += 1
	        self.h2t.Fill(x,y)
	        self.hxt.Fill(x)
	        self.hyt.Fill(y)
	    
        for t,e in mod12:
	
	    self.ht12.Fill(t)
            t = t-64+64
	    self.ht.Fill(t)
	    
            x,y = decode12[e]
	    x = x + 8

	    self.h2.Fill(x,y)
	    self.hx.Fill(x)
	    self.hy.Fill(y)
            hits.append((x,y,t))
	    n += 1
	    if 45<t<60:
	        nt += 1
	        self.h2t.Fill(x,y)
	        self.hxt.Fill(x)
	        self.hyt.Fill(y)

	self.hn.Fill(n)
	self.hnt.Fill(nt)
	self.hn09.Fill(len(mod09))
	self.hn10.Fill(len(mod10))
	self.hn11.Fill(len(mod11))
	self.hn12.Fill(len(mod12))
	    
	event.reco["Matrix"]=hits
