from ROOT import TH1F
from ROOT import TH2F
	

class Gorin:
	" Decode gorin from OKA2006 DATA"

	
	def __init__(self,data):

		gMap = (0, 15, 1, 14, 2, 13, 3, 12, 4, 11, 5, 10, 6, 9, 7, 8)
		self.data = data
		self.x = []
		self.y = []
		n = []
		
		n.append((self.data[2]	   ) & 0x1F)
		n.append((self.data[2]  >> 5) & 0x1F)
		n.append((self.data[2]  >>10) & 0x1F)
		
		self.OK = True
		
		if(n[0]+n[1]+n[2]+3 != data[0]) :
			print "Errror %i "%data[0],n
			self.OK = False
			return
		
		i = 0
		j = 0

#		print data		
		for len3 in n:
			
			for word in range(len3):
				j += 1
		
				tm = (data[2+j]     ) & 0x03FF
				ch = (data[2+j] >>10) & 0x000F
				xy = (data[2+j] >>14) & 0x0001

#				print i,j,data[2+j],tm,ch,xy


				no = gMap[ch] + 16*i;
				
				if xy==0:
					self.x.append((no,tm))
				else:
					self.y.append((no,tm))
					
				
										
			i += 1
		
#		print len(x),len(y)
		
		
class ViewGorin:

	def __init__(self,rootfile):

		dir = rootfile.mkdir("Gorin")
		dir.cd()
		self.hl = TH1F( 'hl', 'hl',50, 0, 50 )
		self.hnx = TH1F( 'hnx', 'hnx', 32, 0, 32 )
		self.hny = TH1F( 'hny', 'hny', 32, 0, 32 )
		self.hnxny = TH2F( 'hnxny', 'hnxny', 32, 0, 32, 32, 0, 32 )
		self.hx = TH1F( 'hx', 'hx', 48, 0, 48 )
		self.hy = TH1F( 'hy', 'hy', 48, 0, 48 )
		self.htx = TH1F( 'htx', 'htx', 300, 0, 300 )
		self.hty = TH1F( 'hty', 'hty', 300, 0, 300 )
		self.hxt = TH2F( 'hxt', 'hxt', 300, 0, 300, 48, 0, 48 )
		self.hyt = TH2F( 'hyt', 'hyt', 300, 0, 300, 48, 0, 48 )

		dirxy = dir.mkdir("xy")
		dirxy.cd()
		self.hxy = TH2F( 'hxy', 'hxy', 48, 0, 48, 48, 0, 48 )
		self.htxy = TH2F( 'htxy', 'htxy', 300, 0, 300, 300, 0, 300 )
		self.hdt = TH1F( 'hdt', 'hdt', 300, -300, 300 )
		self.hxyg = TH2F( 'hxyg', 'hxyg', 48, 0, 48, 48, 0, 48 )
		self.hxyb = TH2F( 'hxyb', 'hxyb', 48, 0, 48, 48, 0, 48 )
		self.hxygg = TH2F( 'hxygg', 'hxygg', 48, 0, 48, 48, 0, 48 )

		dir2 = dir.mkdir("2")
		dir2.cd()
		self.h2x = TH1F( 'hx', 'hx', 48, 0, 48 )
		self.h2tx = TH1F( 'htx', 'htx', 300, 0, 300 )
		self.h2dx = TH1F( 'hdx', 'hdx', 48, 0, 48 )
		self.h2dtx = TH1F( 'hdtx', 'hdtx', 300, 0, 300 )
		self.h2dxg = TH1F( 'hdxg', 'hdxg', 48, 0, 48 )
		self.h2dxb = TH1F( 'hdxb', 'hdxb', 48, 0, 48 )

		self.h2y = TH1F( 'hy', 'hy', 48, 0, 48 )
		self.h2ty = TH1F( 'hty', 'hty', 300, 0, 300 )
		self.h2dy = TH1F( 'hdy', 'hdy', 48, 0, 48 )
		self.h2dty = TH1F( 'hdty', 'hdty', 300, 0, 300 )
		self.h2dyg = TH1F( 'hdyg', 'hdyg', 48, 0, 48 )
		self.h2dyb = TH1F( 'hdyb', 'hdyb', 48, 0, 48 )


	def Execute(self,event):
		
#		data = event.det[12]
		try:
			data = event.det[22]
			g = Gorin(data)
			event.reco["Gorin"] = g
			
			self.hl.Fill(data[0])
			
			nx = len(g.x)
			self.hnx.Fill(nx)
			for ix in range(nx):
				self.hx.Fill(g.x[ix][0])
				self.htx.Fill(g.x[ix][1])
				self.hxt.Fill(g.x[ix][1],g.x[ix][0])

			if nx == 2:
				x1 = g.x[0][0]
				x2 = g.x[1][0]
				t1 = g.x[0][1]
				t2 = g.x[1][1]
				dx = abs(x1-x2)
				dt = abs(t1-t2)
				self.h2x.Fill(x1)
				self.h2x.Fill(x2)
				self.h2tx.Fill(t1)
				self.h2tx.Fill(t2)
				self.h2dx.Fill(dx)
				self.h2dtx.Fill(dt)
				if dt<30:
					self.h2dxg.Fill(dx)
				else:
					self.h2dxb.Fill(dx)
					
			ny = len(g.y)
			self.hny.Fill(ny)
			for iy in range(ny):
				self.hy.Fill(g.y[iy][0])
				self.hty.Fill(g.y[iy][1])
				self.hyt.Fill(g.y[iy][1],g.y[iy][0])

			if ny == 2:
				y1 = g.y[0][0]
				y2 = g.y[1][0]
				t1 = g.y[0][1]
				t2 = g.y[1][1]
				dy = abs(y1-y2)
				dt = abs(t1-t2)
				self.h2y.Fill(y1)
				self.h2y.Fill(y2)
				self.h2ty.Fill(t1)
				self.h2ty.Fill(t2)
				self.h2dy.Fill(dy)
				self.h2dty.Fill(dt)
				if dt<30:
					self.h2dyg.Fill(dy)
				else:
					self.h2dyb.Fill(dy)
					
			self.hnxny.Fill(nx,ny)		
			
			if nx==1 & ny==1:
				self.hxy.Fill(g.x[0][0],g.y[0][0])
				self.htxy.Fill(g.x[0][1],g.y[0][1])
				self.hdt.Fill(g.x[0][1]-g.y[0][1])
				dt =  g.x[0][1]-g.y[0][1]
				if -25<dt<25:
					self.hxyg.Fill(g.x[0][0],g.y[0][0])
				if 220<g.x[0][1]<270:	
					if 220<g.y[0][1]<270:	
						self.hxygg.Fill(g.x[0][0],g.y[0][0])
				else:
					self.hxyb.Fill(g.x[0][0],g.y[0][0])

					
					
		except 	KeyError:
			pass
			
