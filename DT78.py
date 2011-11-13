from ROOT import TH1F,TH2F,TH3F

decode = [ 0,16, 1,17, 2,18, 3,19, 4,20, 5,21, 6,22, 7,23,
	   8,24, 9,25,10,26,11,27,12,28,13,29,14,30,15,31,
	  32,48,33,49,34,50,35,51,36,52,37,53,38,54,39,55,
	  40,56,41,57,42,58,43,59,44,60,45,61,46,62,47,63]

dec0 = [3,4,2,5,1,6,0,7]
dec1 = [7,0,6,1,5,2,4,3]
dec4 = [0,7,1,6,2,5,3,4]
dec5 = [4,3,5,2,6,1,7,0]
dec6 = [4,3,2,5,6,1,7,0]

mapx0 = dec1+[i+8 for i in dec1]+[i+16 for i in dec1]+[i+24 for i in dec1]+[i+32 for i in dec1]+[i+40 for i in dec1]+[i+48 for i in dec1]+[i+56 for i in dec1]
mapx1 = dec4+[i+8 for i in dec0]+[i+16 for i in dec0]+[i+24 for i in dec0]+[i+32 for i in dec0]+[i+40 for i in dec0]+[i+48 for i in dec0]+[i+56 for i in dec0]
mapx2 = dec1+[i+8 for i in dec1]+[i+16 for i in dec1]+[i+24 for i in dec1]+[i+32 for i in dec1]+[i+40 for i in dec1]+[i+48 for i in dec1]+[i+56 for i in dec1]
mapy0 = dec1+[i+8 for i in dec1]+[i+16 for i in dec1]+[i+24 for i in dec6]+[i+32 for i in dec1]+[i+40 for i in dec1]+[i+48 for i in dec1]+[i+56 for i in dec1]
mapy1 = dec1+[i+8 for i in dec0]+[i+16 for i in dec0]+[i+24 for i in dec4]+[i+32 for i in dec0]+[i+40 for i in dec0]+[i+48 for i in dec0]+[i+56 for i in dec0]
mapy2 = dec1+[i+8 for i in dec1]+[i+16 for i in dec1]+[i+24 for i in dec5]+[i+32 for i in dec1]+[i+40 for i in dec1]+[i+48 for i in dec1]+[i+56 for i in dec1]

dec = {}
dec[4] = 64*[None]
dec[5] = 64*[None]
dec[6] = 64*[None]
dec[7] = 64*[None]
dec[8] = 64*[None]
dec[9] = 64*[None]

#for i in range(64):
# 	dec[4][i] =  ('X',0,(i&0xF0)+maping[i&0xF])
# 	dec[5][i] =  ('X',1,(i&0xF0)+maping[i&0xF])
# 	dec[6][i] =  ('X',2,(i&0xF0)+maping[i&0xF])
# 	dec[7][i] =  ('Y',0,(i&0xF0)+maping[i&0xF])
# 	dec[8][i] =  ('Y',1,(i&0xF0)+maping[i&0xF])
# 	dec[9][i] =  ('Y',2,(i&0xF0)+maping[i&0xF])

for i in range(64):
	k = decode[i]
 	dec[4][i] =  ('X',0,mapx0[k])
 	dec[5][i] =  ('X',1,mapx1[k])
 	dec[6][i] =  ('X',2,mapx2[k])
 	dec[7][i] =  ('Y',0,mapy0[k])
 	dec[8][i] =  ('Y',1,mapy1[k])
 	dec[9][i] =  ('Y',2,mapy2[k])

#for i in range(64):
# 	dec[4][i] =  ('X',0,i)
# 	dec[5][i] =  ('X',1,i)
# 	dec[6][i] =  ('X',2,i)
# 	dec[7][i] =  ('Y',0,i)
# 	dec[8][i] =  ('Y',1,i)
# 	dec[9][i] =  ('Y',2,i)

#for i in range(64):
# 	dec[4][i] =  ('X',0,i)
# 	dec[5][i] =  ('X',1,i)
# 	dec[6][i] =  ('X',2,i)
# 	dec[7][i] =  ('Y',0,i)
# 	dec[8][i] =  ('Y',1,i)
# 	dec[9][i] =  ('Y',2,i)

#for i in range(8):
#	dec[4][i*2   ] = ('Y',1,dec5[i]   )
#	dec[4][i*2+16] = ('Y',2,dec4[i]   )
#	dec[4][i*2+ 1] = ('Y',0,dec4[i]+ 8)
#	dec[4][i*2+17] = ('Y',1,dec5[i]+ 8)
#	dec[4][i*2+32] = ('Y',0,dec4[i]+16)
#	dec[4][i*2+48] = ('Y',1,dec5[i]+16)
#	dec[4][i*2+33] = ('Y',2,dec4[i]+16)
#	dec[4][i*2+49] = ('Y',2,dec4[i]+ 8)
#	
#	dec[5][i*2   ] = ('Y',0,dec4[i]+40)
#	dec[5][i*2+16] = ('Y',1,dec5[i]+40)
#	dec[5][i*2+ 1] = ('Y',0,dec4[i]+32)
#	dec[5][i*2+17] = ('Y',1,dec5[i]+32)
#	dec[5][i*2+32] = ('Y',2,dec4[i]+32)
#	dec[5][i*2+48] = ('Y',0,dec0[i]+24)
#	dec[5][i*2+33] = ('Y',1,dec1[i]+24)
#	dec[5][i*2+49] = ('Y',2,dec0[i]+24)
#
#	dec[6][i*2   ] = ('Y',0,dec4[i]+48)
#	dec[6][i*2+16] = ('Y',1,dec5[i]+48)
#	dec[6][i*2+ 1] = ('Y',2,dec4[i]+48)
#	dec[6][i*2+17] = ('Y',2,dec4[i]+40)
#	dec[6][i*2+32] = ('Y',2,dec4[i]   )
#	dec[6][i*2+48] = ('Y',2,dec4[i]+ 8)
#	dec[6][i*2+33] = ('Y',1,dec5[i]   )
#	dec[6][i*2+49] = ('Y',0,dec4[i]+ 8)
#	
#	dec[7][i*2   ] = ('X',2,dec4[i]+32)
#	dec[7][i*2+16] = ('X',2,dec4[i]+24)
#	dec[7][i*2+ 1] = ('X',1,dec5[i]+24)
#	dec[7][i*2+17] = ('X',0,dec4[i]+24)
#	dec[7][i*2+32] = ('X',0,dec4[i]+16)
#	dec[7][i*2+48] = ('X',1,dec5[i]+16)
#	dec[7][i*2+33] = ('X',2,dec4[i]+16)
#	dec[7][i*2+49] = ('X',1,dec5[i]+ 8)
#
#	dec[8][i*2   ] = ('X',1,dec5[i]+40)
#	dec[8][i*2+16] = ('X',0,dec4[i]+40)
#	dec[8][i*2+ 1] = ('X',1,dec5[i]+40)
#	dec[8][i*2+17] = ('X',0,dec4[i]+48)
#	dec[8][i*2+32] = ('X',2,dec4[i]+48)
#	dec[8][i*2+48] = ('X',2,dec4[i]+40)
#	dec[8][i*2+33] = ('X',1,dec5[i]+32)
#	dec[8][i*2+49] = ('X',0,dec4[i]+32)
#
#	dec[9][i*2   ] = ('X',1,dec5[i]+40)
#	dec[9][i*2+16] = ('X',0,dec4[i]+40)
#	dec[9][i*2+ 1] = ('X',1,dec5[i]+40)
#	dec[9][i*2+17] = ('X',0,dec4[i]+48)
#	dec[9][i*2+32] = ('X',2,dec4[i]+48)
#	dec[9][i*2+48] = ('X',2,dec4[i]+40)
#	dec[9][i*2+33] = ('X',1,dec5[i]+32)
#	dec[9][i*2+49] = ('X',0,dec4[i]+32)


class DT78:
	def __init__(self,event):
	
		self.dt = {"X":([],[],[]),"Y":([],[],[])}
		
		try:
		    le78 = event.reco["LE78-10"]
		except KeyError:
		    return

		for modul in (4,5,6,7,8,9):
		    try:
			mod = le78.moduls[modul]
		    except KeyError:
			continue
		
		    for t,e in mod:
			xy,i,k = dec[modul][e]
			self.dt[xy][i].append((t,k))

#		print self.dt


class ViewDT78:


	class HDT78:

		def __init__(self,rootfile,xy):
		
			self.dir = rootfile.mkdir('DT'+xy)
			self.dir.cd()
			self.he=[]
			self.ht=[]
			self.hn=[]

			for k in range(3):
				self.he.append(TH1F( 'he%d'%k, 'he', 56,  0, 56 ))
				self.ht.append(TH1F( 'ht%d'%k, 'he', 256, 0, 256 ))
				self.hn.append(TH1F( 'hn%d'%k, 'hn', 16,  0, 16 ))
			self.htt01 =  TH2F( 'htt01', 'htt', 256, 0, 256, 256, 0, 256)
			self.htt02 =  TH2F( 'htt02', 'htt', 256, 0, 256, 256, 0, 256)
			self.htt12 =  TH2F( 'htt12', 'htt', 256, 0, 256, 256, 0, 256)
			self.hee01 =  TH2F( 'hee01', 'hee', 56, 0, 56, 56, 0, 56)
			self.hee02 =  TH2F( 'hee02', 'hee', 56, 0, 56, 56, 0, 56)
			self.hee12 =  TH2F( 'hee12', 'hee', 56, 0, 56, 56, 0, 56)
			self.hee01t =  TH2F( 'hee01t', 'heet', 56, 0, 56, 56, 0, 56)
			self.hee02t =  TH2F( 'hee02t', 'heet', 56, 0, 56, 56, 0, 56)
			self.hee12t =  TH2F( 'hee12t', 'heet', 56, 0, 56, 56, 0, 56)
			self.htt01e =  TH2F( 'htt01e', 'htte', 256, 0, 256, 256, 0, 256)
			self.htt02e =  TH2F( 'htt02e', 'htte', 256, 0, 256, 256, 0, 256)
			self.htt12e =  TH2F( 'htt12e', 'htte', 256, 0, 256, 256, 0, 256)
			
			self.hdt01 = TH1F( 'hdt01', 'hdt01', 256,  -128, 128 )	
			self.hdt02 = TH1F( 'hdt02', 'hdt02', 256,  -128, 128 )	
			self.hdt12 = TH1F( 'hdt12', 'hdt12', 256,  -128, 128 )	
			self.hst01 = TH1F( 'hst01', 'hst01', 512,  0, 512 )	
			self.hst02 = TH1F( 'hst02', 'hst02', 512,  0, 512 )	
			self.hst12 = TH1F( 'hst12', 'hst12', 512,  0, 512 )	

		def Fill(self,dt):
		
			for i in range(3):
				self.hn[i].Fill(len(dt[i]))	
				for t,e in dt[i]:
					self.he[i].Fill(e)
					self.ht[i].Fill(t)
				
			for t1,e1 in dt[0]:
				for t2,e2 in dt[1]:
					self.htt01.Fill(t1,t2)
					self.hee01.Fill(e1,e2)
					self.hdt01.Fill(t1-t2)
					self.hst01.Fill(t1+t2)
					
					if 150<t1+t2<220:
						self.hee01t.Fill(e1,e2)
					if abs(e1-e2)<=1:
						self.htt01e.Fill(t1,t2)
			for t1,e1 in dt[0]:
				for t2,e2 in dt[2]:
					self.htt02.Fill(t1,t2)				
					self.hee02.Fill(e1,e2)				
					self.hdt02.Fill(t1-t2)
					self.hst02.Fill(t1+t2)	
					if -20<t1-t2<20:
						self.hee02t.Fill(e1,e2)	
					if abs(e1-e2)<1:
						self.htt02e.Fill(t1,t2)
			for t1,e1 in dt[1]:
				for t2,e2 in dt[2]:
					self.htt12.Fill(t1,t2)				
					self.hee12.Fill(e1,e2)				
					self.hdt12.Fill(t1-t2)
					self.hst12.Fill(t1+t2)	
					if 150<t1+t2<220:
						self.hee12t.Fill(e1,e2)	
					if abs(e1-e2)<=1:
						self.htt12e.Fill(t1,t2)
			        
	def __init__(self,rootfile):

		
		self.dir = rootfile.mkdir("DT78")
		self.dir.cd()
		
		self.hdtx = self.HDT78(self.dir,"X")
		self.hdty = self.HDT78(self.dir,"Y")
		
	def Execute(self,event):

		dt = DT78(event)
		self.hdtx.Fill(dt.dt["X"])		
		self.hdty.Fill(dt.dt["Y"])		
		event.reco["DT"] = dt
