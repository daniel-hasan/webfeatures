from feature.features import ReviewBasedFeature
import datetime

'''class AgeReviewRatio(ReviewBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,curr_date):
        super().__init__(self,name,description,reference,visibility,text_format,feature_time_per_document,curr_date)
        self.first_review = float("inf")
        self.num_reviews = 0

    def checkReview(self,review):
        self.num_reviews += 1
        if(self.first_review > review.rev_timestamp):
            self.first_review = review.rev_timestamp

    @abstractmethod
    def compute_feature(self,last_review):
        first_review_date = datetime.datetime.fromtimestamp(self.first_review)
        age = (self.curr_date-first_review_date).days

        return age/self.num_reviews if self.num_reviews >0 else 0
'''

class ThreeMonthProportionReview(ReviewBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,curr_date):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document,curr_date)
        self.trreview = 0
        self.total_review = 0

    def checkReview(self,review):
        self.total_review += 1
        if((self.curr_date-datetime.datetime.fromtimestamp(review.rev_timestamp)).days < 90):
            self.trreview += 1

    def compute_feature(self,last_review):
        return self.trreview/self.total_review

    def finish_document(self,last_review):
        self.trreview = 0
        self.last_review = 0

class ReviewModSize(ReviewBasedFeature):

    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,curr_date):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document,curr_date)
        self.sizeref = 0

    def checkReview(self,reference):
        self.sizeref = reference.rev_size

    def compute_feature(self,last_review):
        return (self.sizeref*100)/last_review.rev_size

    def finish_document(self,last_review):
        self.sizeref = 0


class PercentReviewsPerDay(ReviewBasedFeature):

    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,curr_date):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document,curr_date)
        self.num_reviews = 0

    def checkReview(self,review):
        self.num_reviews += 1

    def compute_feature(self,reference):
        age = (self.curr_date-datetime.datetime.fromtimestamp(reference.rev_timestamp)).days
        ratio = self.num_reviews/float(age)
        return (ratio*100)/self.num_reviews

    def finish_document(self,review):
        self.num_reviews = 0

class ReviewOccasion(ReviewBasedFeature):

    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,curr_date,rev_name):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document,curr_date)
        self.rev_name = rev_name
        self.num_reviews = 0

    def checkReview(self,review):
        if(self.rev_name == review.reviewer_name):
            self.num_reviews += 1

    def compute_feature(self, last_review):
        if(self.num_reviews >= 4):
            self.num_reviews = 0

        return self.num_reviews

    def finish_document(self, review):
        self.num_reviews = 0
