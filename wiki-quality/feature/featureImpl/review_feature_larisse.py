import math

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
class AnonymousReviewCount(Review):
    def __init__(self,int_rev_id,rev_timestamp,rev_size):
        self.id_reviewer = int("inf")
        self.id_reviews = 0

    def checkReview(self, review):
        if(type(sef.name_reviewer) != type(review.int_rev_id)):
            self.num_reviews +=1

    @abstractmethod
    def compute_feature(self):
        return self.num_reviews

''' Conta o numero de revisões feitas por usuarios registrados '''
class RegisteredReviewCount(Review):
    def __init__(self,int_rev_id,rev_timestamp,rev_size):
        self.id_reviewer = int("inf")
        self.num_reviews = 0

    def checkReview(self, review):
        if(type(self.id_reviewer) == type(review.int_rev_id)):
            self.num_reviews +=1

    @abstractmethod
    def compute_feature(self):
        return self.num_reviews

'''Desvio padrão da média de revisões feitas por usuários'''
class ReviewsPerUser(Review):
    def __init__(self,int_rev_id,rev_timestamp,rev_size):
        self.num_reviews_user = 0;

    def checkReview(self, review):
        self.num_reviews_user +=1

    def compute_feature(self):
        devation = num_reviews_user**num_reviews_user
        devation = devation/num_reviews_user
        devation = math.sqrt(devation)
        return devation
