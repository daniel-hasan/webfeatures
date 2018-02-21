from feature.featureImpl.readability_features import *
from feature.features import Document
import unittest

class TestReadability(unittest.TestCase):
    
    def testDocumentChache(self):
        document = Document(1,"doc1","documento para teste de cache")
        cacheChar = document.obj_cache.getCacheItem(ReadabilityBasedFeature.CHARCOUNT,self)
        self.assertEqual(None, cacheChar, "A cache deveria estar vazia")
        objOwner = object()
        objValueCache = object()
        cacheChar = document.obj_cache.setCacheItem(ReadabilityBasedFeature.CHARCOUNT, objValueCache, objOwner)
        self.assertEqual(document.obj_cache.owner[ReadabilityBasedFeature.CHARCOUNT], objOwner, "O dono não esta sendo atribuído")
        self.assertEqual(document.obj_cache.cache[ReadabilityBasedFeature.CHARCOUNT], objValueCache, "O valor não está sendo atribuído")
        
        try:
            cacheWord = document.obj_cache.getCacheItem(ReadabilityBasedFeature.CHARCOUNT, self)
            cacheWord = document.obj_cache.getCacheItem(ReadabilityBasedFeature, objValueCache)
            self.assertTrue(False, "O objeto não deveria ter acesso a cache")
        
        except(NotTheOwner):
            pass
        
        cacheChar = document.obj_cache.getCacheItem(ReadabilityBasedFeature.CHARCOUNT, objOwner)
        self.assertEqual(objValueCache, cacheChar, "As permissões de dono não estão sendo atribuídas")
        
    def test(self):
        objari = ARIFeature("ARI Feature","Compute ARI metric","reference", FeatureVisibilityEnum.public,
                            FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)
        
        objcl = ColemanLiauFeature("CL Feature","Compute CL metric","reference", FeatureVisibilityEnum.public,
                            FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)
        
        objgfi = GunningFogIndexFeature("GFI Feature","Compute GFI metric","reference", FeatureVisibilityEnum.public,
                            FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)
if __name__ == "__main__":
    unittest.main()