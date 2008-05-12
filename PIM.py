from ROOT import TH1F

class ViewPIM:

	def __init__(self,rootfile):

		self.dir = rootfile.mkdir("PIM")
		self.dir.cd()
		self.h = TH1F( 'PIM', 'PIM', 16, 0, 16)


	def Execute(self,event):
		

		try:
			data = event.det[23]
			pim = data[2]
			for i in range(15):
				b = (pim>>i)&0x1
				if b:
					self.h.Fill(i)

			self.h.Fill(15)
		except KeyError:
			pass
			
			
			
