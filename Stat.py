from ROOT import TH1F
	
		
class Stat:

	def __init__(self,rootfile):

		self.hl = {}
		self.dir = rootfile.mkdir("DetLen")



	def Execute(self,event):
		
		det = event.det
#		print det.keys()
		for d in det.iterkeys():
#			print d,det[d]
			try:
				h = self.hl[d]
			except KeyError:
				print "New SubEquipment found",d
				name = "hl%d"%d
				self.dir.cd()
				self.hl[d] = TH1F( name, name,4096, 0, 4096 )
				h = self.hl[d]
			
			h.Fill(det[d][0])


				
