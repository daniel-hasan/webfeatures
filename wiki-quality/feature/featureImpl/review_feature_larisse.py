
'''Conta o numero de revisões de um artigo'''
class ReviewCount(ReviewBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,curr_date):
        super().__init__(self,name,description,reference,visibility,text_format,feature_time_per_document)
        self.reviews = 0

    def checkReview(self,review):
        self.reviews +=1

    @abstractmethod
    def compute_feature(self):
        return self.reviews

'''Conta o numero de revisões feita por usuarios anonimos'''
class AnonymousReviewCount(ConfigurableParam):
    def __init__(self,int_rev_id,rev_timestamp,rev_size):
        self.name_reviewer = int("inf")
        self.num_reviews = 0

    def checkReview(self, review):
        if(sef.name_reviewer != review.int_rev_id):
            self.num_reviews +=1

    @abstractmethod
    def compute_feature(self):
        return self.num_reviews

''' Conta o numero de revisões feitas por usuarios registrados '''
class RegisteredReviewCount(Review):
    def __init__(self,int_rev_id,rev_timestamp,rev_size):
        self.name_reviewer = int("inf")
        self.num_reviews = 0

    def checkReview(self, review):
        if(self.name_reviewer == review.int_rev_id):
            self.num_reviews +=1

    @abstractmethod
    def compute_feature(self):
        return self.num_reviews
