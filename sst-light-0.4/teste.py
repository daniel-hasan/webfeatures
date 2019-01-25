import os

class SST:
	def executaSST(strFile):
		
		data = ['teste','']

		for file in data:
		
			os.system("./sst train teste ./DATA/SEM_07.BI ./DATA/WNSS_07.TAGSET 0 3 BIO")
			os.system("./sst tag teste ./MODELS/SEM07_base_12 ./DATA/WNSS_07.TAGSET 0 BIO")
		


		
'''

./MODELS/WSJc_base_20 ./DATA/WSJ.TAGSET 

os.system("./sst multitag file 0 0 DATA/GAZ/gazlistall_minussemcor ./MODELS/WSJPOSc_base_20 DATA/WSJPOSc.TAGSET ./MODELS/SEM07_base_12 ./DATA/WNSS_07.TAGSET ./MODELS/WSJc_base_20 ./DATA/WSJ.TAGSET")
			
'''

