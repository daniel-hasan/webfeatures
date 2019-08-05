import math

'''Conta o numero de revisões de um artigo'''
class ReviewCount(ReviewBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,curr_date):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document)
        self.reviews = 0

    def checkReview(self,review):
        self.reviews +=1

    @abstractmethod
    def compute_feature(self):
        return self.reviews

'''Conta o numero de revisões feita por usuarios anonimos'''
class AnonymousReviewCount(Review):
    def __init__(self,int_rev_id,rev_timestamp,rev_size):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document)
        self.id_reviewer = int("inf")
        self.id_reviews = 0

    def checkReview(self, review):
        #checar por uma regexp se o name_reviewer é igual a um ip ou filtrar pelo review.int_rev_user_id (se for none, anonimo)
        if(type(sef.str_reviewer_name) != type(review.int_rev_id)):
            self.num_reviews +=1

    @abstractmethod
    def compute_feature(self):
        return self.num_reviews

''' Conta o numero de revisões feitas por usuarios registrados '''
class RegisteredReviewCount(Review):
    def __init__(self,int_rev_id,rev_timestamp,rev_size):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document)
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
        self.dict_rev_per_user = {};

    def checkReview(self, review):
        if(review.str_reviewer_name not in self.dict_rev_per_user):
            self.dict_rev_per_user[review.str_reviewer_name] = 0
        self.dict_rev_per_user[review.name_reviewer] += 1

    def compute_feature(self):
        devation = num_reviews_user**num_reviews_user
        devation = devation/num_reviews_user
        devation = math.sqrt(devation)
        return devation
