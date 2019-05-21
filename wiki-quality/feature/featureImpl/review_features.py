class AgeReviewRatio(ReviewBasedFeature):
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
