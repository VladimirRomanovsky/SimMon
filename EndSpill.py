from ROOT import TH1F
	
		
class EndSpill:

	def __init__(self,rootfile):

		pass

	def Execute(self,event):
		
		print "End of SPILL"
		
		det = event.det
		
		for d in det.iterkeys():
			print d,len(det[d])


				
