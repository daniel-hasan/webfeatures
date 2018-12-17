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

        doc1 = Document(1,"doc1","I do not do this thing at the right way. The alligator is in the lake.")

        objari = ARIFeature("ARI Feature","Compute ARI metric","reference", FeatureVisibilityEnum.public,
                            FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS)

        objcl = ColemanLiauFeature("CL Feature","Compute CL metric","reference", FeatureVisibilityEnum.public,
                            FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS)

        objfre = FleschReadingEaseFeature("FRE Feature","Compute FRE metric","reference", FeatureVisibilityEnum.public,
                            FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS)

        objfkf = FleschKincaidFeature("FK Feature","Compute FK metric","reference", FeatureVisibilityEnum.public,
                            FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS)

        objgfi = GunningFogIndexFeature("GFI Feature","Compute GFI metric","reference", FeatureVisibilityEnum.public,
                            FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS)

        objlbi = LasbarhetsindexFeature("LBI Feature","Compute LBI metric","reference", FeatureVisibilityEnum.public,
                            FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS)

        objsmog = SmogGradingFeature("SMOG Feature","Compute SMOG metric","reference", FeatureVisibilityEnum.public,
                            FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS)


        arr_features = []
        arr_features.append(objcl)
        arr_features.append(objsmog)
        arr_features.append(objlbi)
        arr_features.append(objgfi)
        arr_features.append(objfkf)
        arr_features.append(objfre)
        arr_features.append(objari)







        arr_result = FeatureCalculator.featureManager.computeFeatureSet(doc1, arr_features, FormatEnum.HTML)


        dictExpectedResultPerFeat = {"ARI Feature":-1.82,
                                     "CL Feature":-0.05,
                                     "FRE Feature":87.68,
                                     "FK Feature":3.02,
                                     "GFI Feature":5.7,
                                     "LBI Feature":14.25,
                                     "SMOG Feature":7}

        for i,result in enumerate(arr_result):
            strFeatName = arr_features[i].name
            self.assertAlmostEqual(result, dictExpectedResultPerFeat[strFeatName], 1)

if __name__ == "__main__":
    unittest.main()
