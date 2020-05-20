import unittest
from feature.featureImpl.review_features import *
from feature.features import Review, FeatureVisibilityEnum
from utils.basic_entities import CheckTime
import datetime
from utils.basic_entities import FormatEnum, FeatureTimePerDocumentEnum

class TestsReview(unittest.TestCase):

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

    def testReview(self):

        last_review = Review(10103,1562672369,3500,"bia_souza")
        #09/07/2019
        third_review = Review(10103,1560598769,3536,"rubio")
        #15/06/2019
        second_review = Review(10102,1560639029,3000,"bia_souza")
        #15/06/2019
        first_review = Review(10101,1550616629,2500,"larisse")
        #19/02/2019
        reference = Review(10100,1549839029,2000,"bia_souza")
        #10/02/2019

        curr_date = 1562767134
        objTMP = ThreeMonthProportionReview("r-3month","Proportion of r-rcount in last 3 months","review feature",
                FeatureVisibilityEnum.public,FormatEnum.HTML,FeatureTimePerDocumentEnum.MILLISECONDS,curr_date)
        objRMS = ReviewModSize("r-modsize","Percentage of size of curr. version != from reference","review feature",
                FeatureVisibilityEnum.public,FormatEnum.HTML,FeatureTimePerDocumentEnum.MILLISECONDS,curr_date)
        objRO = ReviewOccasion("r-occasion","Reviews by reviewers with less than 4 edits","review feature",
                FeatureVisibilityEnum.public,FormatEnum.HTML,FeatureTimePerDocumentEnum.MILLISECONDS,curr_date,"bia_souza")
        objPRP = PercentReviewsPerDay("r-revpday","Percentage of reviews per day","review feature",FeatureVisibilityEnum.public,
                FormatEnum.HTML,FeatureTimePerDocumentEnum.MILLISECONDS,curr_date)

        objTMP.checkReview(last_review)
        objTMP.checkReview(third_review)
        objTMP.checkReview(second_review)
        objTMP.checkReview(first_review)
        objTMP.checkReview(reference)

        fl = 3/5
        int_result = objTMP.compute_feature(last_review)
        self.assertEqual(int_result, fl, "O teste ThreeMonthProportionReview falhou")

        objRMS.checkReview(reference)

        fl = (2000*100)/3500
        int_result = objRMS.compute_feature(last_review)
        self.assertEqual(int_result, fl, "O teste ReviewModSize falhou")

        objRO.checkReview(last_review)
        objRO.checkReview(third_review)
        objRO.checkReview(second_review)
        objRO.checkReview(first_review)
        objRO.checkReview(reference)

        int_result = objRO.compute_feature(last_review)
        self.assertEqual(int_result, 3, "O teste ReviewOccasion falhou")

        objPRP.checkReview(last_review)
        objPRP.checkReview(third_review)
        objPRP.checkReview(second_review)
        objPRP.checkReview(first_review)
        objPRP.checkReview(reference)

        r = 5/149
        fl = (r*100)/5
        int_result = objPRP.compute_feature(reference)
        self.assertEqual(int_result, fl, "O teste PercentReviewsPerDay falhou")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'TestFeatureCalculator.testName']
    unittest.main()
