import os

class SST:
	def executaSST(strFile):
		
		data = ['teste','']

		for file in data:
		
			os.system("sst train teste ./DATA/SEM_07.BI_base ./DATA/WNSS_07.TAGSET ./DATA/WSJ.TAGSET 0 number_of_epochs BIO")
			os.system("sst tag teste ./MODELS/SEM07_base_12 ./DATA/WNSS_07.TAGSET ./MODELS/WSJc_base_20 ./DATA/WSJ.TAGSET 0 BIO")
		


		
'''
os.system("./sst multitag file 0 0 DATA/GAZ/gazlistall_minussemcor ./MODELS/WSJPOSc_base_20 DATA/WSJPOSc.TAGSET ./MODELS/SEM07_base_12 ./DATA/WNSS_07.TAGSET ./MODELS/WSJc_base_20 ./DATA/WSJ.TAGSET")
			
sst multitag rowdata 2nd-order lowercase gazfile model_pos tagset_pos model_bio_1 tagset_bio_1 .. model_bio_N tagset_bio_N

sst train modelname traindata tagsetname secondorder number_of_epochs mode

sst tag modelname target_data tagsetname secondorder mode
'''

