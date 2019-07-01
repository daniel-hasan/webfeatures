import unittest
from unittest import TestCase
from feature.featureImpl.semantic_features import PartOfSpeechTaggerFeature
from feature.features import FeatureVisibilityEnum, Document, FeatureCalculator
from utils.basic_entities import FormatEnum, FeatureTimePerDocumentEnum

class TestPartOfSpeech(unittest.TestCase):

    def setUp(self):

        '''
        Implemente esse método para criar algo antes do teste
        '''
        pass


    def tearDown(self):

        '''
         Implemente esse método para eliminar algo feito no teste
        '''
        pass

    def testPOSTagger(self):

        arrFeatures = [PartOfSpeechTaggerFeature("POS Tagger", "Tagging part of speech in sentences", "",
                FeatureVisibilityEnum.public, FormatEnum.textplain, FeatureTimePerDocumentEnum.MILLISECONDS, "en"),
                PartOfSpeechTaggerFeature("POS Tagger", "Tagging part of speech in sentences",
                FeatureVisibilityEnum.public, FormatEnum.textplain, FeatureTimePerDocumentEnum.MILLISECONDS, "pt")]

        posen = arrFeatures[0].compute_feature("My name is Daniel.")
        pospt = arrFeatures[1].compute_feature("Meu nome é Daniel.")

        self.assertListEqual([('My', 'PRP$'), ('name', 'NN'), ('is', 'VBZ'), ('Daniel', 'NNP'), ('.', '.')], posen)
        self.assertListEqual([('Meu', 'PROADJ'), ('nome', 'N'), ('é', 'V'), ('Daniel', 'NPROP'), ('.', 'NPROP')], pospt)

    def testBagOfPOS(self):

        arrFeatures = [BagOfPOSFeature("Bag of POS", "Bag of part of speech in text", "",
            FeatureVisibilityEnum.public, FormatEnum.textplain, FeatureTimePerDocumentEnum.MILLISECONDS, "en"),
            BagOfPOSFeature("Bag of POS", "Bag of part of speech in text", "",
            FeatureVisibilityEnum.public, FormatEnum.textplain, FeatureTimePerDocumentEnum.MILLISECONDS, "pt")]

        bagen = arrFeatures[0].compute_feature("My name is Daniel.")
        bagpt = arrFeatures[1].compute_feature("Meu nome é Daniel.")

        self.assertEqual(bagen,{'PRP$':1,'NN':1,'VBZ':1,'NNP':1,'.':1},"O texto em inglês falhou")
        self.assertEqual(bagpt,{'PROADJ':1,'N':1,'V':1,'NPROP':2},"O texto em portugues falhou")


if __name__ == "__main__":

    unittest.main()
