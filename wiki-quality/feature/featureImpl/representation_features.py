'''
Created on 10 de ago de 2017
Features que fazem uma nova representação do texto (topicos, bag of words)
@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br> 
'''
from feature import TextBasedFeature

 
class BagOfTFIDFFeature(TextBasedFeature):
    
    @property
    def doc_set_preprocessing(self):
        return []
    
