import os

class SST:
	def executaSST(strFile):
		
		data = ['teste','']

		for file in data:
		
			os.system("./sst train teste ./DATA/SEM_07.BI ./DATA/WNSS_07.TAGSET 0 3 BIO")
			os.system("./sst tag ./MODELS/teste teste ./DATA/WNSS_07.TAGSET 0 BIO")
		


		
'''

./MODELS/WSJc_base_20 ./DATA/WSJ.TAGSET 

			
'''

