from ROOT import TH1F,TH2F

decode = []
for i in range(64):
    dx,k = divmod(i,32)
    k,dy = divmod(k,2)
    y,x = divmod(k,4)
    x = x + dx*4
    y = y + (1-dy)*4
    decode.append((x,y))

class ViewMatrix:

    def __init__(self,rootfile):
	self.dir = rootfile.mkdir("Matrix")
	self.dir.cd()
	
	self.he = TH1F( 'he', 'he', 64, 0, 64 )
	self.ht = TH1F( 'ht', 'ht', 128, 0, 128 )
	self.h2 = TH2F( 'h2', 'XY', 8, 0, 8, 8, 0, 8 )
	
    def Execute(self,event):

	try:
	    le78 = event.reco["LE78-11"]
	    mod = le78.moduls[12]
	except KeyError:
	    return

        for t,e in mod:
	
	    self.he.Fill(e)
	    self.ht.Fill(t)
	    
            x,y = decode[e]
	    self.h2.Fill(x,y)
