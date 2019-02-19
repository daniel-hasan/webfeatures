import os
import tempfile

class SST:
	def executaSST(strFile):
		
		data = ['teste']

		for file in data:
		
			os.system("./sst train " + str(file) + " ./DATA/SEM_07.BI ./DATA/WNSS_07.TAGSET 0 1 BIO")
			os.system("mv /MODELS/" + str(file) + ".* /tmp/")
			os.system("./sst multitag " + str(file) + " 0 0 DATA/GAZ/gazlistall_minussemcor ./MODELS/WSJPOSc_base_20 DATA/WSJPOSc.TAGSET /tmp/" + str(file) + " ./DATA/WNSS_07.TAGSET")
		