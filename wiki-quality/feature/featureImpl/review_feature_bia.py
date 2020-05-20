#TODO: Nas classes que não tivererm, colocar no inicio de cada classe sua descrição
#.....exemplo; ReviewCount
#ao inves de ser ThreeMonthProportionReview ser: RecentRateReview
class ThreeMonthProportionReview(ReviewBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,curr_date):
        super().__init__(self,name,description,reference,visibility,text_format,feature_time_per_document,curr_date)
        #variavel com nome estranho, substituir por "period_review"
        self.trreview = 0
        self.total_review = 0
        #TODO: Parece que tem algo errado com esse código abaixo (age deveria ser um aatributo)
        self.age = curr_date.days

    def checkReview(self,review):
        self.total_review += 1
        #TODO: O 90 deveria ser uma constante
        if((self.age-review.rev_timestamp.days) < 90):
            self.trreview += 1

    def compute_feature(self,last_review):
        return self.trreview/self.total_review

    def finish_document(self,last_review):
        self.trreview = 0
        self.last_review = 0
#TODO: Trodar por RiviewModificationsize
class ReviewModSize(ReviewBasedFeature):

    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,curr_date):
        super().__init__(self,name,description,reference,visibility,text_format,feature_time_per_document,curr_date)
        self.sizeref = 0

    def checkReview(self,reference):
        self.sizeref = reference.rev_size

    def compute_feature(self,last_review):
        return (self.sizeref*100)/last_review.rev_size

    def finish_document(self,last_review):
        self.sizeref = 0


class PercentReviewsPerDay(ReviewBasedFeature):

    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,curr_date):
        super().__init__(self,name,description,reference,visibility,text_format,feature_time_per_document,curr_date)
        self.num_reviews = 0

    def checkReview(self,review):
        self.num_reviews += 1

    def compute_feature(self,review):
        age = (self.curr_date).days
        ratio = self.num_reviews/age
        return (ratio*100)/self.num_reviews

    def finish_document(self,review):
        self.num_reviews = 0

#TODO: Substituir por occasionalReviews
class ReviewOccasion(ReviewBasedFeature):

    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,curr_date,rev_name):
        super().__init__(self,name,description,reference,visibility,text_format,feature_time_per_document,curr_date)
        self.rev_name = rev_name
        self.num_reviews = 0

    def checkReview(self,review):
        if(self.rev_name == review.reviewer_name):
            self.num_reviews += 1

    def compute_feature(self, review):
        if(self.num_reviews >= 4):
            self.num_reviews = 0

        return self.num_reviews

    def finish_document(self, review):
        self.num_reviews = 0


import math


class ReviewCount(ReviewBasedFeature):
    '''Conta o numero de revisões de um artigo'''
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,curr_date):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document)
        self.reviews = 0

    def checkReview(self,review):
        self.reviews +=1

    @abstractmethod
    def compute_feature(self):
        return self.reviews

class AnonymousReviewCount(Review):
    '''Conta o numero de revisões feita por usuarios anonimos'''
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


class RegisteredReviewCount(Review):
    ''' Conta o numero de revisões feitas por usuarios registrados '''
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
