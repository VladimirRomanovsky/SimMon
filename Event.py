class Event:

	def __init__(self,buf):
		self.data = buf[0:buf[0]/2]
		self.det = {}
		self.eq = 0
		self.reco = {}
		
	def Type(self):
		return self.data[4]
		
	def _decode_eq(self,buf):
#		print buf
		size = len(buf)
		k = 0
		
		while k+1<size: 		# Possible added 0 at end for parity
			l = buf[k]
			if l == 0:
			    break
			d = buf[k+1]
			d = d&0xFF
			if self.eq == 128:
				d = d | 0x8
#			print l,d

			self.det[d] = buf[k:k+l]
			k += l
			   
	def _decode_host(self,buf):
		size = len(buf)
		k = 0
		while k+6<size:
#			print buf[k:k+6]
			eqsize = buf[k+4]/2
			self.eq = buf[3]
			self._decode_eq(buf[k+6:k+6+eqsize])
			k+=6+eqsize
			
	def _decode(self,buf):
		try:
			nL = buf[18]
		except IndexError:
			return
			
#		print "_decode",nL
		k = 40
		
		if nL == 0:
#			print buf[0:40]
#			print buf[20]
			self._decode_host(buf[40:])
		else:
			while k<len(buf):
				size = buf[k]/2
				self._decode(buf[k:k+size])
				k += size
			
	def Decode(self):
		self._decode(self.data)
	
	
		   
